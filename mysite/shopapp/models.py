from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.utils.translation import gettext_lazy as _, ngettext_lazy

def g_l(model):
    return model.length

class Product(models.Model):
    class Meta:
        ordering = ["name", "-price"]
        # db_table = "product"
        verbose_name = _("product")
        verbose_name_plural = _("products")
    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1)

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + "..."
    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"

    def get_absolute_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.pk})


class Order(models.Model):
    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
