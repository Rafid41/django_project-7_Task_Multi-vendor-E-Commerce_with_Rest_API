from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from api.models import DailyData

# models and forms
from App_Order.models import Order, Cart, Coupon
from App_Payment.forms import BillingAddress, BillingForm, CollectCouponForm

from django.contrib.auth.decorators import login_required
from decimal import Decimal
import uuid

# views

coupon_percentise = 0


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]  # touple to object

    form = BillingForm(
        instance=saved_address
    )  # already save kora adds er upor form generate hbe, save na thakle blank form

    coupon_form = CollectCouponForm()
    global coupon_percentise
    coupon_percentise = 0

    if request.method == "POST":
        form_name = request.POST.get("form_name")

        if form_name == "address_form":
            form = BillingForm(request.POST, instance=saved_address)

            if form.is_valid():
                form.save()
                form = BillingForm(instance=saved_address)
                messages.success(request, f"Shipping Address Saved!")

        elif form_name == "coupon_form":
            coupon_form = CollectCouponForm(request.POST)

            if coupon_form.is_valid():
                collect_code = coupon_form.cleaned_data[
                    "collect"
                ]  # or, collect_code = coupon_form.cleaned_data.get('collect')

                try:

                    coupon = Coupon.objects.get(coupon_code=collect_code)
                    coupon_percentise = coupon.coupon_percent
                    messages.success(request, f"Coupon Applied")

                except Coupon.DoesNotExist:
                    coupon_percentise = 0
                    messages.warning(request, f"Invalid coupon code")

    # show ordered items in checkout page
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[
        0
    ].orderitems.all()  # 'orderitems' models.py er ekta field(App_Order)
    order_total = order_qs[0].get_totals()  # 'get_totals' models.y er ekta fn

    order_total_after_coupon_applied = 0

    if coupon_percentise > 0:
        order_total_after_coupon_applied = order_total - (
            (order_total * coupon_percentise) / 100
        )

    return render(
        request,
        "App_Payment/checkout.html",
        context={
            "form": form,
            "order_items": order_items,
            "order_total": order_total,
            "saved_address": saved_address,
            "coupon_form": coupon_form,
            "order_total_after_coupon_applied": order_total_after_coupon_applied,
        },
    )


# view for payment
@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]

    # check all fields are filled //models.py
    if not saved_address.is_fully_filled():
        messages.info(request, f"Please complete shipping address!")
        return redirect("App_Payment:checkout")

    # App_login er modles.py er fn, "profile"==related_name
    if not request.user.profile.is_fully_filled():
        messages.info(request, f"Please complete profile detail")
        return redirect("App_Login:profile")

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()  # get_totals() is a fn from models.py

    if coupon_percentise > 0:
        order_total = order_total - ((order_total * coupon_percentise) / 100)

    ######################## update daily data ###############################
    current_date = timezone.now().date()

    # Get or create DailyData object for the current date
    daily_data, created = DailyData.objects.get_or_create(date_data=current_date)

    # same date
    if not created:
        daily_data.revenue += order_total
        daily_data.save()

    else:
        # new date
        daily_data.revenue = order_total
        daily_data.save()

    return complete(request)


def complete(request):

    val_id = str(uuid.uuid4())
    tran_id = str(uuid.uuid4())

    if True:

        messages.success(request, f"Your Payment Completed Successfully!")

        return HttpResponseRedirect(
            reverse(
                "App_Payment:purchase",
                kwargs={"val_id": val_id, "tran_id": tran_id},
            )
        )
    return render(request, "App_Payment/complete.html", context={})


# purchase korar por cart clear korbe
# order er ordered=True and cart er purchased = True hbe
@login_required
def purchase(request, val_id, tran_id):

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]

    order.ordered = True
    order.orderId = tran_id
    order.paymentId = val_id
    order.save()

    cart_items = Cart.objects.filter(user=request.user, purchased=False)

    for item in cart_items:
        item.purchased = True
        item.save()

    return HttpResponseRedirect(reverse("App_Shop:home"))


# show previous orders
@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {"orders": orders}

    except:
        messages.warning(request, "You do not have an active order")
        return redirect("App_Shop:home")

    return render(request, "App_Payment/order.html", context)
