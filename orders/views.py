from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, Customer
from .serializers import OrderSerializer, CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        status_value = request.data.get('status')
        if not status_value:
            return Response({'error': 'Status is required'}, status=400)

        order.status = status_value
        order.save()
        return Response({'status': 'Order status updated successfully'})



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'], url_path='orders')
    def get_orders(self, request, pk=None):
        customer = self.get_object()
        orders = Order.objects.filter(customer=customer)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)