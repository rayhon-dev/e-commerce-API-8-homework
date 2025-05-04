from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'id',
            'image',
            'is_primary',
            'created_at'
        ]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'discount_price',
            'category_id',
            'category_name',
            'images',
            'stock',
            'is_active',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for image_data in images_data:
            image_instance = instance.images.filter(id=image_data.get('id')).first()
            if image_instance:
                image_instance.image = image_data.get('image', image_instance.image)
                image_instance.is_primary = image_data.get('is_primary', image_instance.is_primary)
                image_instance.save()
            else:
                ProductImage.objects.create(product=instance, **image_data)

        return instance
