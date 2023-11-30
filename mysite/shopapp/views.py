from timeit import default_timer

from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponseNotFound

from .models import Product, Order
from .forms import CreateProductForm, CreateOrderForm
from django.contrib.auth import authenticate

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import ProductSerializer, OrderSerializer


def admin(request: HttpRequest):
    return redirect("/admin/")


def index(request: HttpRequest):
    pk = request.user.pk

    pages = [
        ("Info page", reverse("shopapp:index"), "shopindex.html"),
        ("Products page", reverse("shopapp:products_list"), "products_list.html"),
        ("Orders page", reverse("shopapp:orders_list"), "order_list.html"),
        ("GET page", reverse("requestdataapp:get_view"), "request_query_params.html"),
        ("File upload page", reverse("requestdataapp:file_upload"), "upload.html"),
    ]

    api_pages = [
        ("API page", reverse("shopapp:api-root"), "api_root_page"),
        ("API documentation", reverse("schema"), "api_documentation_page"),
        ("API swagger documentation", reverse("swagger_schema"), "api_swagger_documentation_page"),
        ("API redoc documentation", reverse("redoc_schema"), "api_redoc_documentation_page"),
    ]

    if request.user.is_authenticated:
        pages.append(("Logout", reverse("myauth:logout"), "logout No Html"))
        pages.append(("My profile", reverse("myauth:profile"), "my_profile.html"))
        # pages.append(("Users list", reverse("myauth:accounts_list"), "accounts_list.html"))
        pages.append(("My orders", reverse("shopapp:user_order_details", kwargs={"user_id": pk}), "userorders_list.html"))
        pages.append(("Export my orders", reverse("shopapp:user_orders_export", kwargs={"user_id": pk}), "return JSON"))
    else:
        pages.append(("Login", reverse("myauth:login"), "login.html"))
        pages.append(("Register NOW", reverse("myauth:register"), "register.html"))

    if request.user.username == "admin":
        pages.append(("admin", reverse("shopapp:admin"), "Admin page"))

    pages.append(("Users list", reverse("myauth:accounts_list"), "accounts_list.html"))
    pages.append(("Articles", reverse("blogapp:article_list"), "article_list.html"))

    context = {
        "pages": pages,
        "api_pages": api_pages,
    }

    return render(request, 'shopapp/index.html', context=context)


# Create your views here.
def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]

    context = {
        "time_running": default_timer(),
        "products": products,
    }

    return render(request, 'shopapp/shopindex.html', context=context)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ["name", "description", "created_at"]
    search_fields = ["name", "description", "created_at"]


class ProductsListView(ListView):
    template_name = 'shopapp/products_list.html'
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


# class ProductsListView(TemplateView):
#     template_name = 'shopapp/products_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["products"] = Product.objects.all()
#         return context

# class ProductsListView(View):
#     def get(self, request: HttpRequest) -> HttpResponse:
#         context = {
#             "products": Product.objects.all(),
#         }
#
#         return render(request, 'shopapp/products_list.html', context=context)

class ProductDetailsView(DetailView):
    template_name = 'shopapp/product_detail.html'
    model = Product
    context_object_name = "product"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["user"] = request.user
        context["prod_count"] = Product.objects.filter(archived=False).count()
        return self.render_to_response(context)

# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         # product = Product.objects.get(pk=pk)
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             "product": product
#         }
#         return render(request, "shopapp/product_detail.html", context=context)


class CreateProductView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "description", "price", "discount"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        request = self.request
        form.instance.created_by = request.user
        self.object = form.save()
        return super().form_valid(form)


# class CreateProductFormView(View):
#     def get(self, request: HttpRequest) -> HttpResponse:
#         form = CreateProductForm()
#
#         context = {
#             "form": form,
#         }
#         return render(request, 'shopapp/product_create.html', context=context)
#
#     def post(self, request: HttpRequest) -> HttpResponse:
#         form = CreateProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#         url = reverse("shopapp:products_list")
#         return redirect(url)


class UpdateProductView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        self.object = self.get_object()
        return ((self.object.created_by.pk == self.request.user.pk)
                or (self.request.user.is_superuser))

    permission_required = "shopapp.change_product"
    model = Product
    fields = "name", "description", "price", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:product_details", kwargs = {
            "pk": self.object.pk,
        })


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        # self.object.delete()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class LatestProductsFeed(Feed):
    title = "Latest Products"
    description = "Updatets on add Products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.filter(archived=False).order_by("created_at")[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description[:150]

    # def item_link(self, item):
    #     return reverse("shopapp:product_details", kwargs={"pk": item.pk})


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = [
        "delivery_address",
        "promocode",
        "created_at"
    ]
    filterset_fields = [
        "delivery_address",
        "promocode",
        "created_at"
    ]

class OrderListView(ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )

# class OrderListView(View):
#     def get(self, request: HttpRequest) -> HttpResponse:
#         context = {
#             "orders": Order.objects.select_related("user").prefetch_related("products").all(),
#         }
#         return render(request, 'shopapp/order_list.html', context=context)


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )

# class CreateOrderFormView(View):
#     def get(self, request: HttpRequest) -> HttpResponse:
#         form = CreateOrderForm()
#         context = {
#             "form": form,
#         }
#         return render(request, 'shopapp/order_create.html', context=context)
#
#     def post(self, request: HttpRequest) -> HttpResponse:
#         form = CreateOrderForm(request.POST)
#         if form.is_valid():
#             # form.cleaned_data[]
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:orders_list")
#             return redirect(url)


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")


class UpdateOrderView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("shopapp:order_details", kwargs = {
            "pk": self.object.pk,
        })


class DeleteOrderView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")


class OrdersExportView(UserPassesTestMixin, PermissionRequiredMixin, View):
    permission_required = ['shopapp.view_order']

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        # for order in Order.objects.all():
        #     print(order.pk)
        #     print(order.delivery_address)
        #     print(order.user)
        orders = {}
        for order in Order.objects.select_related("user").prefetch_related("products").all():
            orders[order.pk] = {"delivery_address": order.delivery_address,
                                "promocode": order.promocode,
                                "user_id": order.user.pk,
                                "user_name": order.user.username,
                                "products": {p.id: {"name": p.name,
                                                    "price": round(p.price, 2),
                                                    "discount": p.discount}
                                             for p in order.products.all()},
                                }
        return JsonResponse(orders)


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/userorders_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["owner"] = User.objects.filter(pk=self.user_id).get
        context["owner"] = self.owner
        return context

    def get(self, request: HttpRequest, **kwargs):
        self.owner = get_object_or_404(User, pk=self.kwargs["user_id"])
        self.user_id = self.kwargs["user_id"]
        return super().get(request, **kwargs)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.user_id)
        return queryset


class UserOrdersExportView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, user_id: int):
        owner = get_object_or_404(User, pk=user_id)
        cache_key = "orders_data_"+str(user_id)
        orders = cache.get(cache_key)
        if orders is None:
            order = Order.objects.select_related("user").prefetch_related("products").filter(user=user_id).order_by("pk")
            orders = OrderSerializer(order, many=True).data
            cache.set(cache_key, orders, 200)
        return JsonResponse(orders, safe=False)
