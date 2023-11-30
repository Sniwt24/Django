from django.shortcuts import redirect
from django.urls import path, include, reverse
from rest_framework.routers import DefaultRouter
from .views import (shop_index, ProductsListView, OrderListView, index,
                    CreateProductView, CreateOrderView,
                    ProductDetailsView, UpdateProductView, DeleteProductView,
                    OrderDetailsView, UpdateOrderView, DeleteOrderView,
                    admin, OrdersExportView,
                    ProductViewSet, OrderViewSet, LatestProductsFeed, UserOrderListView, UserOrdersExportView)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("", index, name="index_def"),
    path("admin/", admin, name="admin"),
    path("info/", shop_index, name="index"),
    path("api/", include(routers.urls), name="api"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", CreateProductView.as_view(), name="product_create"),
    path("products/details/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/details/<int:pk>/update/", UpdateProductView.as_view(), name="product_update"),
    path("products/details/<int:pk>/delete/", DeleteProductView.as_view(), name="product_delete"),
    path("products/latest/feed/", LatestProductsFeed(), name="products_feed"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path("orders/details/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path("user/<int:user_id>/orders/", UserOrderListView.as_view(), name="user_order_details"),
    path("orders/details/<int:pk>/update", UpdateOrderView.as_view(), name="order_update"),
    path("orders/details/<int:pk>/delete", DeleteOrderView.as_view(), name="order_delete"),
    path("orders/create/", CreateOrderView.as_view(), name="order_create"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),
    path("user/<int:user_id>/orders/export/", UserOrdersExportView.as_view(), name="user_orders_export"),
]
