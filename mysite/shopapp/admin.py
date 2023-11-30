from io import TextIOWrapper
from csv import DictReader
from ast import literal_eval

import json
from xml.etree import ElementTree as ET

from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description="Archive product(s)")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description="Unrchive product(s)")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived, mark_unarchived, "export_csv",
    ]
    inlines = [OrderInline, ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    ordering = "-pk",
    search_fields = "name", "price"
    fieldsets = [
        (
            None, {"fields": ("name", "description")}
        ),
        (
            "Price options", {
                "fields": ("price", "discount"),
                "classes": ("collapse",)
            }
        ),
        (
            "Extra options", {
                "fields": ("archived",),
                "classes": ("collapse",),
                "description": "Extra option for soft delete"
            }
        )
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

# Register your models here.


class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"
    inlines = [ProductInline, ]
    list_display = "pk", "delivery_address", "promocode", "created_at", "user_verbose"
    list_display_links = "pk", "delivery_address",

    def get_queryset(self, request):
        return Order.objects.select_related("user")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form
            }
            return render(request, "admin/csv_form.html", context, status=400)
        csv_file = TextIOWrapper(
            form.files["file"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        for row in reader:
            ord = Order.objects.create(delivery_address=row["delivery_address"],
                    promocode=row["promocode"],
                    user=User.objects.get(pk=row["user"]),
                                 )
            ord.products.set([Product.objects.get(pk=prodid) for prodid in literal_eval(row["products"])])

        self.message_user(request, "Data from CSV was imported")
        return redirect("..")

    def import_json(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)

        form = CSVImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                "form": form
            }
            return render(request, "admin/csv_form.html", context, status=400)

        json_file = TextIOWrapper(
            form.files["file"].file,
            encoding=request.encoding,
        )
        reader = json.load(json_file)

        for row in reader:
            ord = Order.objects.create(delivery_address=row["fields"]["delivery_address"],
                    promocode=row["fields"]["promocode"],
                    user=User.objects.get(pk=row["fields"]["user"]),
                                 )
            ord.products.set([Product.objects.get(pk=prodid) for prodid in row["fields"]["products"]])

        self.message_user(request, "Data from JSON was imported")
        return redirect("..")

    def import_xml(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form
            }
            return render(request, "admin/csv_form.html", context, status=400)
        xml_file = TextIOWrapper(
            form.files["file"].file,
            encoding=request.encoding,
        )

        reader = ET.parse(xml_file)
        root = reader.getroot()

        ord = Order()

        for row in root:
            for field in row:
                match field.get("name"):
                    case "delivery_address":
                        da = field.text
                    case "promocode":
                        pr = field.text
                    case "user":
                        us = field.text
                    case "products":
                        prods = [pr.get("pk") for pr in field]
            ord = Order.objects.create(delivery_address=da,
                    promocode=pr,
                    user=User.objects.get(pk=us),
                                 )
            ord.products.set([Product.objects.get(pk=prodid) for prodid in prods])

        self.message_user(request, "Data from CSV was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path
        new_urls = [
            path(
                "import-orders-csv/",
                self.import_csv,
                name="import_orders_csv",
            ),
            path(
                "import-orders-json/",
                self.import_json,
                name="import_orders_json",
            ),
            path(
                "import-orders-xml/",
                self.import_xml,
                name="import_orders_xml",
            ),
        ]
        return new_urls + urls


admin.site.register(Product, ProductAdmin)
