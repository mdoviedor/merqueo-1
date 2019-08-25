from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from pedidos.serializers import UserSerializer, OrderSerializer
from pedidos.models import Order
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['GET'])
    def best_sellers(self, request):
        query = Order.objects.all()
        data = OrderSerializer(query, many=True)
        return Response(data.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
