from rest_framework import serializers


class TopProductStatsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    total_sold = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=10, decimal_places=2)


class DashboardOrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = serializers.IntegerField()
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()


class DashboardRecentOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    customer = serializers.IntegerField()
    customer_username = serializers.CharField()
    status = serializers.CharField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = serializers.CharField()
    payment_method = serializers.CharField()
    items = DashboardOrderItemSerializer(many=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class DashboardStatsSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    top_products = TopProductStatsSerializer(many=True)
    recent_orders = DashboardRecentOrderSerializer(many=True)
