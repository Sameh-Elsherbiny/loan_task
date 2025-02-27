from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .models import MonthlyRepayment, LoanPlan
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import (
    F,
    OuterRef,
    Subquery,
    IntegerField,
    ExpressionWrapper,
    DurationField,
    DateField,
)
from users.models import LoanCustomer


@shared_task
def Penalty_check():
    print("Penalty check started")

    repayments = MonthlyRepayment.objects.annotate(
        adjusted_date=ExpressionWrapper(
            F("date")
            + ExpressionWrapper(
                F("loan__loan_customer__plan__allowness") * timedelta(days=1),
                output_field=DurationField(),
            ),
            output_field=DateField(),
        )
    ).filter(paid=False, adjusted_date__lte=timezone.now().date())

    repayments_to_update = []
    users = []
    for repayment in repayments:
        penalty_amount = repayment.loan.loan_customer.plan.penalty_amount
        repayment.penalty = penalty_amount
        repayment.amount += penalty_amount
        repayment.over_due = True
        repayments_to_update.append(repayment)
        users.append(repayment.loan.loan_customer.user)
    user_emails = [user.email for user in users]
    send_email.delay("overdue", user_emails)

    MonthlyRepayment.objects.bulk_update(
        repayments_to_update, ["penalty", "amount", "over_due"]
    )


@shared_task
def notify_user():
    users = MonthlyRepayment.objects.filter(
        over_due=False, paid=False, date=timezone().now().date() - timedelta(days=1)
    ).values("loan__loan_customer__user__email")
    user_emails = [user['loan__loan_customer__user__email'] for user in users]
    send_email.delay("repayment", user_emails)


@shared_task
def send_email(action: str, users: list):
    email_map = {
        "overdue": "You have an overdue",
        "repayment": "You have a repayment due",
        }
    for email in users:
        email_data = {
            "email_subject": "Loan Notification",
            "to_email": email,
            "email_body": email_map[action],
        }

        email = EmailMessage(
            subject=email_data["email_subject"],
            body=email_data["email_body"],
            to=[email_data["to_email"]],
            from_email=settings.EMAIL_HOST_USER,
        )
        email.send()
