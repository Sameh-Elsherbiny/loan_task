from rest_framework import serializers
from .models import Loan, LoanPlan, LoanRequest , MonthlyRepayment
from users.models import CustomUser, LoanCustomer, LoanProvider 
from .validators import validate_loan_constraints


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "loan_customer",
            "loan_provider",
            "loan_amount",
            "loan_status",
            "created_at",
            "updated_at",
            "interest_rate",
            "loan_duration",
            "total_repayment",
            "monthly_repayment",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "status": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "interest_rate": {"read_only": True},
            "duration": {"read_only": True},
            "total_repayment": {"read_only": True},
            "monthly_repayment": {"read_only": True},
            "loan_provider": {"read_only": True},
            "loan_customer": {"read_only": True},
            "loan_status": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        customer = LoanCustomer.objects.get(user=user)
        loan = Loan.objects.create(loan_customer=customer, **validated_data)
        return loan

    def update(self, instance, validated_data):
        instance.loan_status = validated_data.get("loan_status", instance.loan_status)
        instance.save()
        return instance


class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ["id", "loan", "provider", "created_at", "updated_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "provider": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


    def create(self, validated_data):
        user = self.context["request"].user
        provider = LoanProvider.objects.get(user=user)
        loan_request = LoanRequest.objects.create(provider=provider, **validated_data)
        return loan_request


class AcceptLoanRequestSerializer(serializers.Serializer):
    loan_request_id = serializers.IntegerField()

    class Meta:
        fields = ["loan_request_id"]

    def validate(self, data):
        loan_request_id = data.get("loan_request_id")
        if loan_request_id:
            loan_request = LoanRequest.objects.filter(id=loan_request_id).first()
            if not loan_request:
                raise serializers.ValidationError("Invalid loan request id")
        else:
            raise serializers.ValidationError("Loan request id is required")

        loan = loan_request.loan
        if loan.loan_provider is not None:
            raise serializers.ValidationError("Loan request already accepted")
        loan.loan_provider = loan_request.provider
        loan.loan_status = "P"
        loan.save()
        data["loan"] = LoanSerializer(loan).data
        return data
    
class ApproveLoanSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField()

    class Meta:
        fields = ["loan_id"]

    def validate_loan_id(self, value):
        if not Loan.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid loan id")
        
        return value
    def validate(self, attrs):
        if Loan.objects.filter(id=attrs["loan_id"],loan_status__in = ['A','RQ','PD','R']).exists():
            raise serializers.ValidationError("Loan already approved")
        
        return attrs


class LoanPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPlan
        fields = [
            "id",
            "name",
            "interest_rate",
            "min_loan_amount",  
            "max_loan_amount",  
            "min_loan_duration",  
            "max_loan_duration",  
            "penalty_amount",
            "allowness",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        loan_plan = LoanPlan.objects.create(**validated_data)
        return loan_plan
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)  # Correct super() call



class ApproveLoanRequestSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField()

    class Meta:
        fields = ["loan_id"]

    def validate_loan_id(self, value):
        if not Loan.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid loan id")
        return value
    
class PayMonthlyRepaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = MonthlyRepayment
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.paid = True
        instance.loan.loan_customer.user.account.balance -= instance.amount
        instance.loan.loan_customer.user.account.save()
        instance.save()
        return instance
