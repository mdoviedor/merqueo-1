import datetime

from django.db.models import Sum, Count, Q
from rest_framework import viewsets
from pedidos.serializers import UserSerializer, OrderSerializer, ProductSerializer, SalesTotalSerializer
from pedidos.models import Order, User, Product, OrderProducts, Inventory
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['GET'])
    def in_inventory(self, request):
        filter_sum = Sum('orderproducts__quantity', orderproducts__order__delivery_date=datetime.date(2019, 3, 1))
        query_orders = Product.objects.annotate(total_quantity=filter_sum)

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
            filter_sum = Sum('orderproducts__quantity', orderproducts__order__delivery_date=datetime.date(2019, 3, 1))
            query_orders = Product.objects.annotate(total_quantity=filter_sum)

            return Response(pk)
        return Response(data={'detail': 'Not found.'}, status=404)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['GET'])
    def best_sellers(self, request):
        filter_sum = Sum('orderproducts__quantity', orderproducts__order__delivery_date=datetime.date(2019, 3, 1))
        query = Product.objects.annotate(total_quantity=filter_sum).order_by('-total_quantity')
        data = SalesTotalSerializer(query, many=True)
        return Response(data.data)

    @action(detail=False, methods=['GET'])
    def less_sold(self, request):
        filter_sum = Sum('orderproducts__quantity', orderproducts__order__delivery_date=datetime.date(2019, 3, 1))
        query = Product.objects.annotate(total_quantity=filter_sum).order_by('total_quantity')
        data = SalesTotalSerializer(query, many=True)
        return Response(data.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
