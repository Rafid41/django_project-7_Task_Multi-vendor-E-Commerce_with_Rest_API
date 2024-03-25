from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# import views
from django.views.generic import ListView, DetailView

# Models
from App_Shop.models import Product

# Mixin
from django.contrib.auth.mixins import LoginRequiredMixin


# add product
from App_Shop.forms import AddProductForm
from django.contrib.auth.decorators import login_required

# product per page
from django.core.paginator import Paginator

# Create your views here.


# display products
class Home(ListView):
    model = Product
    template_name = "App_Shop/home.html"
    paginate_by = 12  # Number of products per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "App_Shop/product_detail.html"


@login_required
def add_product(request):
    form = AddProductForm()
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            return HttpResponseRedirect(reverse("App_Shop:home"))

    return render(request, "App_Shop/add_product.html", context={"form": form})
