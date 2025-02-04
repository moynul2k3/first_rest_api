from rest_framework import serializers
from .models import *

class ProductImageSerializer(serializers.ModelSerializer):
    size = serializers.CharField(source='size.name', read_only=True)
    color = serializers.CharField(source='color.name', read_only=True)
    class Meta:
        model = ProductImage
        fields = [
            'size',
            'color',
            'image',
            'created_at',
        ]


class AllProductSerializer(serializers.ModelSerializer):
    productimage = ProductImageSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'details',
            'stock',
            'price',
            'discount',
            'discount_price',
            'sell_price',
            'weight',
            'point',
            'top',
            'ratings',
            'created_at',
            'image',  # First image URL field
            'productimage',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        first_image = obj.productimage.first()  # Get the first image
        if first_image and first_image.image:
            # return first_image.image.url  # Return the image URL
            return request.build_absolute_uri(first_image.image.url) if first_image else None
        return None  # Return None if no image exists

class ProductSerializer(serializers.ModelSerializer):
    productimage = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'details',
            'stock',
            'price',
            'discount',
            'discount_price',
            'sell_price',
            'weight',
            'point',
            'top',
            'ratings',
            'created_at',
            'productimage',
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            'id',
            'name',
            'description',
            'banner',
            'image',
            'top',
            'created_at',
            'products',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if obj.image else None



class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(
        many=True, read_only=True)  # Nested subcategories

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'banner',
            'image',
            'top',
            'created_at',
            'subcategories',  # Include nested subcategories
        ]
