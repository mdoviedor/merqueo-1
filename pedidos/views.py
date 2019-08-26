import datetime

from django.db.models import Sum, Q, Max
from rest_framework import viewsets
from pedidos.serializers import UserSerializer, OrderSerializer, ProductSerializer, SalesTotalSerializer, \
    InventorySerializer, ProviderSerializer
from pedidos.models import Order, User, Product, Inventory, Provider
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['GET'])
    def in_inventory(self, request):
        filter_sum = Sum('orders__quantity', filter=Q(orders__order__delivery_date=datetime.date(2019, 3, 1)))
        query_orders = Product.objects.annotate(total_quantity=filter_sum).exclude(total_quantity__isnull=True)

        list_products = []
        for order_item in query_orders:
            product_inventory = Inventory.objects.filter(product=order_item)
            if product_inventory:
                product_inventory = product_inventory[0]
                product_item = {'id': product_inventory.product.id, 'name': product_inventory.product.name}
                if order_item.total_quantity >= product_inventory.quantity:
                    product_item['quantity'] = product_inventory.quantity
                else:
                    product_item['quantity'] = order_item.total_quantity
                list_products.append(product_item)
        return Response(list_products)

    # Dado el Id de un pedido, saber qué productos y qué cantidad pueden ser
    # alistados según sistema de inventario y cuáles deben ser abastecidos por los proveedores
    @action(detail=True, methods=['GET'])
    def provider(self, request, pk=None):
        order = Order.objects.filter(id=pk)
        if order:
            order = order[0]
            priority = Order.objects.filter(user=order.user).aggregate(Max('priority'))['priority__max']
            filter_sum_higher = Sum('orders__quantity', filter=Q(orders__order__priority__gt=int(priority)))
            orders_higher = Product.objects.annotate(total_quantity=filter_sum_higher).exclude(
                total_quantity__isnull=True)
            filter_sum_users = Sum('orders__quantity', filter=Q(orders__order__user=order.user))
            orders_user = Product.objects.annotate(total_quantity=filter_sum_users).exclude(total_quantity__isnull=True)
            providers = []
            inventory = []
            for order_user in orders_user:
                order_higher = orders_higher.filter(id=order_user.id)
                product_inventory = Inventory.objects.filter(product=order_user)
                if product_inventory:
                    product_inventory = product_inventory[0]
                    if order_higher:
                        product_inventory.quantity = product_inventory.quantity - order_higher[0].total_quantity
                    if product_inventory.quantity < 1:
                        providers.append(SalesTotalSerializer(order_user).data)
                    else:
                        if product_inventory.quantity >= order_user.total_quantity:
                            inventory.append(SalesTotalSerializer(order_user).data)
                        else:
                            item_inventory = {'id': order_user.id, 'name': order_user.name,
                                              'total_quantity': product_inventory.quantity}
                            item_provider = {'id': order_user.id, 'name': order_user.name,
                                             'total_quantity': order_user.total_quantity - product_inventory.quantity}
                            inventory.append(item_inventory)
                            providers.append(item_provider)
                else:
                    providers.append(SalesTotalSerializer(order_user).data)
            response = {'id': order.id, 'user': order.user.id, 'address': order.user.address,
                        'products': {'provider': providers, 'inventory': inventory}}
            return Response(response)
        return Response(data={'detail': 'Not found.'}, status=404)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['GET'])
    def best_sellers(self, request):
        filter_sum = Sum('orders__quantity', filter=Q(orders__order__delivery_date=datetime.date(2019, 3, 1)))
        query = Product.objects.annotate(total_quantity=filter_sum).order_by('-total_quantity')
        data = SalesTotalSerializer(query, many=True)
        return Response(data.data)

    @action(detail=False, methods=['GET'])
    def less_sold(self, request):
        filter_sum = Sum('orders__quantity', filter=Q(orders__order__delivery_date=datetime.date(2019, 3, 1)))
        query = Product.objects.annotate(total_quantity=filter_sum).order_by('total_quantity')
        data = SalesTotalSerializer(query, many=True)
        return Response(data.data)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @action(detail=False, methods=['GET'])
    def after(self, request):
        filter_sum = Sum('orders__quantity', filter=Q(orders__order__delivery_date=datetime.date(2019, 3, 1)))
        orders_p = Product.objects.annotate(total_quantity=filter_sum).order_by('-total_quantity')
        inventory = self.queryset
        for inventory_item in inventory:
            orders_quantity = orders_p.filter(id=inventory_item.product.id)
            if orders_quantity:
                orders_quantity = orders_quantity[0].total_quantity
                inventory_item.quantity = (
                            inventory_item.quantity - orders_quantity) if inventory_item.quantity > orders_quantity else 0
                inventory_item.date = datetime.date(2019, 3, 2)
        data = InventorySerializer(inventory, many=True)
        return Response(data.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Provider.objects.all()
