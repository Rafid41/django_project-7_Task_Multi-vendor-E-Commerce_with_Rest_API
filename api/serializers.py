# api\serializers.py
from rest_framework import serializers
from .models import DailyData
from App_Login.models import User, Profile
from App_Order.models import Cart, Order, Coupon
from App_Payment.models import BillingAddress
from App_Order.models import Product


class UserSerializer(serializers.ModelSerializer):
    # pass read kora jabena
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={
            "input_type": "password",
        },
    )

    class Meta:
        model = User
        fields = ["id", "email", "password", "account_type"]

    # overwrite built-in create fn of ModelSerializer
    # validated data er moddhe email, pass etc thake
    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        account_type = validated_data["account_type"]
        # User Model er create_user fn
        user = User.objects.create_user(email, password, account_type)
        return user


# ####################### others #########################
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class DailyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyData
        fields = "__all__"
