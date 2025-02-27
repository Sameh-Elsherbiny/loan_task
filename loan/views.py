from django.shortcuts import render
from rest_framework import viewsets , generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from .models import Loan, LoanRequest, MonthlyRepayment
from .serializers import (
    LoanSerializer,
    LoanRequestSerializer,
    AcceptLoanRequestSerializer,
    ApproveLoanSerializer,
    PayMonthlyRepaymentSerializer,
    LoanPlanSerializer,
)
from .utils import approve_loan , create_monthly_repayments
from .services import LoanService
from users.permissions import ProviderPermission, CustomerPermission, BankPermission
# Create your views here.


class LoanViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [CustomerPermission]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "retrieve":
            self.permission_classes = [BankPermission]
        elif self.action == "update":
            self.permission_classes = [BankPermission | CustomerPermission]
        elif self.action == "destroy":
            self.permission_classes = [BankPermission | CustomerPermission]
        return super().get_permissions()
    
    def get_queryset(self):
        return LoanService.get_loans_for_user(self.request.user).prefetch_related('loan_provider')


class LoanRequestViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [ProviderPermission]


class AcceptLoanRequest(APIView):
    permission_classes = [CustomerPermission]
    serializer_class = AcceptLoanRequestSerializer

    def post(self, request):
        loan_request = LoanRequest.objects.get(id=self.request.data.get("loan_request_id"))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            data={
                "loan": serializer.validated_data,
                "message": "Loan request accepted",
            },
            status=status.HTTP_200_OK,
        )

class ApproveLoanView(APIView):
    permission_classes = [BankPermission]
    serializer_class = ApproveLoanSerializer

    def post(self, request):
        loan = Loan.objects.get(id=self.request.data.get("loan_id"))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        approve_loan(loan)
        create_monthly_repayments(loan)

        return Response(
            data={
                "loan": serializer.validated_data,
                "message": "Loan request accepted",
            },
            status=status.HTTP_200_OK,
        )
    
class PayMonthlyRepaymentView(generics.UpdateAPIView):
    permission_classes = [CustomerPermission]
    serializer_class = PayMonthlyRepaymentSerializer
    queryset = MonthlyRepayment.objects.all()

class LoanPlanViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = LoanPlanSerializer
    permission_classes = [BankPermission]

    def get_queryset(self):
        return LoanService.get_loan_plans_for_user(self.request.user)
    
class MonthlyRepaymentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = MonthlyRepayment.objects.all()
    serializer_class = PayMonthlyRepaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(loan__loan_customer__user=self.request.user)
    
