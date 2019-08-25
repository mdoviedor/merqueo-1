from django.core.management.base import BaseCommand, CommandError
from pedidos.models import Product, Inventory, Provider, Order, User, OrderProducts
import json
import datetime


class Command(BaseCommand):
    help("Load the data of the json files.")

    def handle(self, *args, **options):
        self.stdout.write("loading inventory")
        self.load_inventory()
        self.stdout.write("loading providers")
        self.load_providers()
        self.stdout.write("loading orders")
        self.load_orders()

    def load_providers(self):
        providers_file = open('./pedidos/management/commands/resources/providers-merqueo.json')
        providers_data = json.load(providers_file)
        if providers_data:
            for provider_item in providers_data['providers']:
                p_name = provider_item['name']
                provider = Provider(name=p_name)
                provider.save()
                for product_item in provider_item['products']:
                    p = self.get_product(product_item['productId'])
                    provider.products.add(p)
                provider.save()

    def load_inventory(self):
        inventory_file = open('./pedidos/management/commands/resources/inventory-merqueo.json')
        inventory_data = json.load(inventory_file)
        if inventory_data:
            for inventory_item in inventory_data['inventory']:
                p_id = inventory_item['id']
                date = datetime.datetime.strptime(inventory_item['date'], '%Y-%m-%d')
                quantity = inventory_item['quantity']
                product = self.get_product(pk=p_id)
                inventory = Inventory(product=product, quantity=quantity, date=date)
                inventory.save()

    def load_orders(self):
        orders_file = open('./pedidos/management/commands/resources/orders-merqueo.json')
        orders_data = json.load(orders_file)
        if orders_data:
            for order_item in orders_data['orders']:
                o_date = datetime.datetime.strptime(order_item['deliveryDate'],'%Y-%m-%d')
                o_priority = order_item['priority']
                o_id = order_item['id']
                o_user = self.get_user(name=order_item['user'], address=order_item['address'])
                order = Order(id=o_id, delivery_date=o_date, user=o_user, priority=o_priority)
                order.save()
                for product_item in order_item['products']:
                    p = self.get_product(pk=product_item['id'], name=product_item['name'])
                    quantity = product_item['quantity']
                    order_products = OrderProducts(order=order, product=p, quantity=quantity)
                    order_products.save()

    @staticmethod
    def get_product(pk, name=None):
        p = Product.objects.filter(id=pk)
        if p:
            p[0].name = name
            p[0].save()
            return p[0]
        p = Product(id=pk, name=name)
        p.save()
        return p

    @staticmethod
    def get_user(name, address):
        user = User.objects.filter(name=name, address=address)
        if user:
            return user[0]
        user = User(name=name, address=address)
        user.save()
        return user
