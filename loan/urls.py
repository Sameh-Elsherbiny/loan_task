from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet, LoanRequestViewSet, AcceptLoanRequest , ApproveLoanView , PayMonthlyRepaymentView , LoanPlanViewSet , MonthlyRepaymentViewSet

router = DefaultRouter()
router.register("loans", LoanViewSet, basename="loan")
router.register("loan-requests", LoanRequestViewSet, basename="loan-request")
router.register("loan-plans", LoanPlanViewSet, basename="loan-plan")
router.register("monthly-repayments", MonthlyRepaymentViewSet, basename="monthly-repayment")

urlpatterns = router.urls + [
    path("accept-loan/", AcceptLoanRequest.as_view(), name="accept-loan-request"),
    path("approve-loan/", ApproveLoanView.as_view(), name="approve-loan"),
    path("pay-repayment/<int:pk>/", PayMonthlyRepaymentView.as_view(), name="pay-repayment"),
]