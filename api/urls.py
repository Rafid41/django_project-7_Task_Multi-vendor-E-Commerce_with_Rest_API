# api\urls.py
from django.urls import path
from rest_framework import routers
from .views import (
    UserViewSet,
    ProductViewSet,
    OrderViewSet,
    CartViewSet,
    ProfileViewSet,
    DailyDataViewSet,
    BillingAddressViewSet,
)

# default view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", ProfileViewSet, basename="profiles")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"carts", CartViewSet, basename="cart")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"dailydata", DailyDataViewSet, basename="dailydata")
router.register(r"billing_address", BillingAddressViewSet, basename="billing_address")


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
