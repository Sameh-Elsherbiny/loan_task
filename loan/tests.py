from django.test import TestCase
from loan.models import LoanPlan
from loan.serializers import LoanPlanSerializer
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from loan.models import Loan
from users.models import LoanCustomer, LoanProvider , CustomUser , Bank

class LoanPlanSerializerTestCase(TestCase):

    def setUp(self):
        """Set up test data before each test."""
        self.loan_plan_data = {
            "name": "Standard Plan",
            "interest_rate": 5.5,
            "min_loan_amount": 1000.00,
            "max_loan_amount": 50000.00,
            "min_loan_duration": 6,
            "max_loan_duration": 24,
            "penalty_amount": "50.00",
            "allowness": 10
        }
        self.loan_plan = LoanPlan.objects.create(**self.loan_plan_data)

    def test_valid_loan_plan_serialization(self):
        """Test LoanPlan serialization."""
        serializer = LoanPlanSerializer(instance=self.loan_plan)
        self.assertEqual(serializer.data["name"], self.loan_plan_data["name"])
        self.assertEqual(Decimal(serializer.data["interest_rate"]), Decimal(self.loan_plan_data["interest_rate"]))
        self.assertEqual(serializer.data["penalty_amount"], str(self.loan_plan_data["penalty_amount"]))
        self.assertEqual(serializer.data["allowness"], self.loan_plan_data["allowness"])

    def test_valid_loan_plan_creation(self):
        """Test LoanPlan creation via serializer."""
        serializer = LoanPlanSerializer(data=self.loan_plan_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        loan_plan = serializer.save()
        self.assertEqual(loan_plan.name, self.loan_plan_data["name"])

    def test_invalid_loan_plan_missing_fields(self):
        """Test LoanPlan validation with missing fields."""
        invalid_data = self.loan_plan_data.copy()
        del invalid_data["name"]  # Removing required field

        serializer = LoanPlanSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_loan_plan_update(self):
        """Test LoanPlan update via serializer."""
        update_data = {"name": "Updated Plan", "interest_rate": 6.5}
        serializer = LoanPlanSerializer(instance=self.loan_plan, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_loan_plan = serializer.save()

        self.assertEqual(updated_loan_plan.name, update_data["name"])
        self.assertEqual(updated_loan_plan.interest_rate, update_data["interest_rate"])



from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import LoanCustomer, LoanProvider, Bank
from users.serializers import UserSerializer, LoanCustomerSerializer, LoanProviderSerializer, BankSerializer

User = get_user_model()


class UserSerializerTestCase(APITestCase):
    """Tests for UserSerializer with Loan Provider, Loan Customer, and Bank"""

    def setUp(self):
        """Setup test data"""
        self.user_data = {
            "username": "bank",
            "password": "bank",
            "user_type": "BK"  # This should be ignored since serializer sets it
        }

    def test_create_bank(self):
        """Ensure Bank (BK) is created correctly"""
        bank_data = {"user": self.user_data}
        serializer = BankSerializer(data=bank_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        bank = serializer.save()

        self.assertEqual(bank.user.username, self.user_data["username"])
        self.assertEqual(bank.user.user_type, "BK")  # user_type is set inside serializer
        self.assertNotEqual(bank.user.password, self.user_data["password"])  # Ensure password is hashed

    def test_create_loan_provider(self):
        """Ensure Loan Provider (LP) is created correctly"""
        provider_data = {"user": {**self.user_data, "user_type": "LP"}}  # user_type should be ignored
        serializer = LoanProviderSerializer(data=provider_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        provider = serializer.save()

        self.assertEqual(provider.user.username, self.user_data["username"])
        self.assertEqual(provider.user.user_type, "LP")  # Serializer enforces this
        self.assertNotEqual(provider.user.password, self.user_data["password"])  # Ensure password is hashed

    def test_create_loan_customer(self):
        """Ensure Loan Customer (LC) is created correctly"""
        self.plan = LoanPlan.objects.create(name="Gold", interest_rate=5.5, min_loan_amount=1000.00, max_loan_amount=50000.00, min_loan_duration=6, max_loan_duration=24, penalty_amount="50.00", allowness=10)
        customer_data = {"user": {**self.user_data, "user_type": "LC"}, "plan": self.plan.id}
        serializer = LoanCustomerSerializer(data=customer_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        customer = serializer.save()

        self.assertEqual(customer.user.username, self.user_data["username"])
        self.assertEqual(customer.user.user_type, "LC")  # Serializer enforces this
        self.assertEqual(customer.plan, None)
        self.assertNotEqual(customer.user.password, self.user_data["password"])  # Ensure password is hashed

    def test_user_type_is_read_only(self):
        """Ensure user_type cannot be changed after creation"""
        bank_data = {"user": self.user_data}
        serializer = BankSerializer(data=bank_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        bank = serializer.save()

        update_serializer = UserSerializer(bank.user, data={"user_type": "LC"}, partial=True)
        self.assertTrue(update_serializer.is_valid())
        updated_user = update_serializer.save()
        self.assertEqual(updated_user.user_type, "BK")  # Ensure user_type remains unchanged
        
    def test_balance_field_is_read_only(self):
        """Ensure balance is correctly sourced and read-only"""
        provider_data = {"user": self.user_data}
        serializer = LoanProviderSerializer(data=provider_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        provider = serializer.save()

        user_serializer = UserSerializer(provider.user)
        self.assertIn("balance", user_serializer.data)
        self.assertEqual(user_serializer.data["balance"], "0.00")  # Default balance value

    def test_update_user_details(self):
        """Ensure user details like username and password can be updated"""
        bank_data = {"user": self.user_data}
        serializer = BankSerializer(data=bank_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        bank = serializer.save()

        updated_data = {
            "username": "updated_bank",
            "password": "newsecurepassword123"
        }
        update_serializer = UserSerializer(bank.user, data=updated_data, partial=True)
        self.assertTrue(update_serializer.is_valid(), update_serializer.errors)
        updated_user = update_serializer.save()

        self.assertEqual(updated_user.username, "updated_bank")
        self.assertNotEqual(updated_user.password, "newsecurepassword123")  # Ensure new password is hashed


class LoanCustomerSerializerTestCase(APITestCase):
    """Additional tests for LoanCustomerSerializer"""

    def setUp(self):
        """Setup test data for LoanCustomer"""
        self.user_data = {
            "username": "customer_test",
            "password": "securepassword123",
            "user_type": "LC"  # This should be ignored
        }
        self.plan=LoanPlan.objects.create(name="Gold", interest_rate=5.5, min_loan_amount=1000.00, max_loan_amount=50000.00, min_loan_duration=6, max_loan_duration=24, penalty_amount="50.00", allowness=10)
        customer_data = {"user": self.user_data, "plan": self.plan.id}
        serializer = LoanCustomerSerializer(data=customer_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.customer = serializer.save()

    def test_update_customer_plan(self):
        """Ensure plan can be updated but user_type remains unchanged"""
        self.plan = LoanPlan.objects.create(name="Silver", interest_rate=6.5, min_loan_amount=2000.00, max_loan_amount=40000.00, min_loan_duration=6, max_loan_duration=24, penalty_amount="50.00", allowness=10)
        update_data = {"plan": self.plan.id}
        serializer = LoanCustomerSerializer(self.customer, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_customer = serializer.save()

        self.assertEqual(updated_customer.plan, None)
        self.assertEqual(updated_customer.user.user_type, "LC")  # Ensure user type remains unchanged
