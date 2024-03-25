# api\views.py
from django.shortcuts import render
from rest_framework import viewsets
from .models import DailyData
from App_Login.models import User, Profile
from App_Order.models import Cart, Order, Coupon
from App_Payment.models import BillingAddress
from App_Order.models import Product
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    ProductSerializer,
    CartSerializer,
    OrderSerializer,
    DailyDataSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


#  code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


############### viewSet for Order ############
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        id = self.request.query_params.get("id", None)

        if id is not None:
            queryset = queryset.filter(user__id=id)

        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # create new product entry
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Product.objects.all()
        id = self.request.query_params.get("id", None)

        if id is not None:
            queryset = queryset.filter(user__id=id)

        return queryset


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class DailyDataViewSet(viewsets.ModelViewSet):
    queryset = DailyData.objects.all()
    serializer_class = DailyDataSerializer
