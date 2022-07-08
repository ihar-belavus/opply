from django.db.models import F
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db import transaction


from shop_api.models import Product, Order


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )


class UserRegistrationSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'confirm_password',
        )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return attrs

    @transaction.atomic()
    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': 'User account is disabled.',
        'invalid_credentials': 'Unable to login with provided credentials.'
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")


class ProductSerializer(ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'quantity',
            'seller'
        )

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'product',
            'quantity',
            'created_at'
        )

    @transaction.atomic()
    def create(self, validated_data):
        product = validated_data['product']
        if product.quantity < validated_data['quantity']:
            raise serializers.ValidationError({'quantity': 'Not enough products left'})
        product.quantity = F('quantity') - validated_data['quantity']
        order = Order.objects.create(**validated_data)
        product.save()
        return order
