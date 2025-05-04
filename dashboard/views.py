from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from products.models import Product
from orders.models import Order, OrderItem, Customer
from .serializers import DashboardStatsSerializer


# Asosiy Dashboard statistikasi
class DashboardStatsView(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_customers = Customer.objects.count()
        total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

        top_products_qs = (
            OrderItem.objects
            .values('product', 'product__name')
            .annotate(
                total_sold=Sum('quantity'),
                revenue=Sum('price')
            )
            .order_by('-total_sold')[:5]
        )

        top_products = [
            {
                'id': item['product'],
                'name': item['product__name'],
                'total_sold': item['total_sold'],
                'revenue': item['revenue'],
            }
            for item in top_products_qs
        ]

        recent_orders = Order.objects.prefetch_related('items', 'customer__user').order_by('-created_at')[:5]
        recent_orders_data = []
        for order in recent_orders:
            recent_orders_data.append({
                'id': order.id,
                'customer': order.customer.id,
                'customer_username': order.customer.user.username,
                'status': order.status,
                'total_price': order.total_price,
                'shipping_address': order.shipping_address,
                'payment_method': order.payment_method,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'items': [
                    {
                        'id': item.id,
                        'product': item.product.id,
                        'product_name': item.product.name,
                        'quantity': item.quantity,
                        'price': item.price,
                        'created_at': item.created_at,
                    }
                    for item in order.items.all()
                ]
            })

        data = {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_revenue': total_revenue,
            'top_products': top_products,
            'recent_orders': recent_orders_data,
        }

        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)


# Eng ko'p sotilgan mahsulotlar
class TopProductsView(APIView):
    def get(self, request):
        top_products_qs = (
            OrderItem.objects
            .values('product', 'product__name')
            .annotate(
                total_sold=Sum('quantity'),
                revenue=Sum('price')
            )
            .order_by('-total_sold')[:5]
        )

        data = [
            {
                'id': item['product'],
                'name': item['product__name'],
                'total_sold': item['total_sold'],
                'revenue': item['revenue'],
            }
            for item in top_products_qs
        ]
        return Response(data)


# Eng faol mijozlar
class TopCustomersView(APIView):
    def get(self, request):
        top_customers_qs = (
            Order.objects
            .values('customer', 'customer__user__username')
            .annotate(
                total_orders=Sum('id'),
                total_spent=Sum('total_price')
            )
            .order_by('-total_spent')[:5]
        )

        data = [
            {
                'id': item['customer'],
                'username': item['customer__user__username'],
                'total_orders': item['total_orders'],
                'total_spent': item['total_spent'],
            }
            for item in top_customers_qs
        ]
        return Response(data)


# Daromad statistikasi (kunlik, haftalik, oylik)
class RevenueStatsView(APIView):
    def get(self, request):
        period = request.query_params.get('period', 'daily')  # default period is 'daily'
        today = timezone.now().date()
        start_date = None

        if period == 'weekly':
            start_date = today - timedelta(weeks=1)
        elif period == 'monthly':
            start_date = today - timedelta(days=30)
        else:  # 'daily' period
            start_date = today

        revenue_qs = (
            Order.objects
            .filter(created_at__gte=start_date)
            .aggregate(total_revenue=Sum('total_price'))
        )

        return Response({
            'period': period,
            'total_revenue': revenue_qs['total_revenue'] or 0,
        })
