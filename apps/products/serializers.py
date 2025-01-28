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
    products = ProductSerializer(many=True, read_only=True)  # Nested products

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
