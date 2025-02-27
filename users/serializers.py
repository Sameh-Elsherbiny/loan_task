from rest_framework import serializers
from .models import CustomUser , LoanCustomer , LoanProvider , Bank

class UserSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='account.balance')
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'user_type', 'balance', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'user_type': {'read_only': True}

        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('user_type', None)
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
    
class LoanProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = LoanProvider
        fields = ['id', 'user']
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'LP'
        user = UserSerializer().create(user_data)
        provider = LoanProvider.objects.create(user=user)
        return provider
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user = UserSerializer().update(user, user_data)
        instance.save()
        return instance
    
class LoanCustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = LoanCustomer
        fields = ['id', 'user', 'plan']
        extra_kwargs = {
            'id': {'read_only': True},
        }
    
    def create(self, validated_data):
        validated_data.pop('plan')
        user_data = validated_data.pop('user')
        user_data['user_type']='LC'
        user = UserSerializer().create(user_data)
        customer = LoanCustomer.objects.create(user=user, **validated_data)
        return customer
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        user = UserSerializer().update(user, user_data)
        if 'plan' in validated_data and 'request' in self.context and self.context['request'].user.user_type == 'BK':
            instance.plan = validated_data.get('plan', instance.plan)
        instance.save()
        return instance
    
class BankSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Bank
        fields = ['id', 'user']
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type']='BK'
        user = UserSerializer().create(user_data)
        bank = Bank.objects.create(user=user)
        return bank
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user = UserSerializer().update(user, user_data)
        instance.save()
        return instance

    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    class Meta:
        fields = ['username', 'password']
        
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = CustomUser.objects.filter(username=username).first()
            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError('Invalid password')
                user = UserSerializer(user).data
            else:
                raise serializers.ValidationError('Invalid username')
        else:
            raise serializers.ValidationError('Username and password are required')
        data['user'] = user
        return data