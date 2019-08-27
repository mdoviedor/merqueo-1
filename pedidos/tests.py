from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pedidos.models import Order, User, Product, OrderProducts, Inventory
import datetime


class MerqueoTests(APITestCase):
    def setUp(self):
        self.u = User.objects.create(name="Prueba", address="Address #pr")
        self.p = Product.objects.create(name="producto prueba")
        Inventory.objects.create(product=self.p, quantity=5)
        self.o = Order.objects.create(priority=1, user=self.u, delivery_date=datetime.date(2019, 3, 1))
        self.op = OrderProducts.objects.create(product=self.p, order=self.o, quantity=2)

    def test_orders_in_inventory(self):
        url = reverse('order-in-inventory')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': self.p.id, 'name': self.p.name, 'quantity': 2}])

    def test_order_provider(self):
        url = reverse('order-provider', args=[self.o.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            "id": self.op.id,
            "user": self.u.id,
            "address": self.u.address,
            "products": {
                "provider": [],
                "inventory": [
                    {
                        "id": self.p.id,
                        "name": self.p.name,
                        "total_quantity": 2
                    }
                ]
            }
        }
        self.assertEqual(response.data, data)

    def test_inventory_after(self):
        url = reverse('inventory-after')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{"product": self.p.id, "quantity": 3, "date": "2019-03-02"}])

    def test_product_best_seller(self):
        url = reverse('product-best-sellers')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = [{
            "id": self.p.id,
            "name": self.p.name,
            "total_quantity": 2
        }]
        self.assertEqual(response.data, data)

    def test_product_less_sold(self):
        url = reverse('product-less-sold')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = [{
            "id": self.p.id,
            "name": self.p.name,
            "total_quantity": 2
        }]
        self.assertEqual(response.data, data)

