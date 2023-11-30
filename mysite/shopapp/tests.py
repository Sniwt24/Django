from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

import json

from django.http import HttpResponse, HttpRequest

from shopapp.models import Order


# Create your tests here.
class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="admin", password="admin")
        cls.user.user_permissions.set([32])



    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(delivery_address="Test_addr", promocode="Test_code", user = self.user)
        self.pk = self.order.pk

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse("shopapp:order_details", kwargs={
            "pk": self.pk,
        }))

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["object"].pk, self.pk)
        self.assertContains(response, reverse("shopapp:order_details", kwargs={
            "pk": self.order.pk,
        }))


class OrdersExportTestCase(TestCase):
    fixtures = [
                'users.json',
                'shopapp_fixtures.json',
                ]
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="Test_user", password="123", is_staff=True)
        cls.user.user_permissions.set([32])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_export(self):
        response = self.client.get(reverse("shopapp:orders_export"))

        orders = {}
        for order in Order.objects.select_related("user").prefetch_related("products").all():
            orders[str(order.pk)] = {"delivery_address": order.delivery_address,
                                     "promocode": order.promocode,
                                     "user_id": order.user.pk,
                                     "user_name": order.user.username,
                                     "products": {str(p.id): {"name": p.name,
                                                              "price": str(round(p.price,2)),
                                                              "discount": p.discount}
                                                  for p in order.products.all()},
                                     }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertJSONEqual(response.content, orders)
