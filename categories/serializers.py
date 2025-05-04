from rest_framework import serializers
from .models import Category
from products.models import Product

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    products_info = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'parent',
            'parent_name',
            'image',
            'products_info',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'image': {'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_products_info(self, obj):
        products = obj.products.filter(is_active=True)[:5]  # optional: limit 5
        return {
            'count': obj.products.count(),
            'products': SimpleProductSerializer(products, many=True).data
        }
