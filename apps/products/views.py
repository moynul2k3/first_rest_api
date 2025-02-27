from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

class SubCategoryListView(APIView):
    def get(self, request):
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(
            subcategories, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)
    
class SubCategoryView(APIView):
    def get(self, request, pk):
        subcategory = get_object_or_404(SubCategory, pk=pk)
        serializer = SubCategorySerializer(
            subcategory, context={'request': request})
        return Response(serializer.data)

class ProductView(APIView):
    def get(self, request, slug):
        products = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(products, context={'request': request})
        return Response(serializer.data)


class AllProductView(APIView):
    def get(self, request):
        products = Product.objects.all()  # QuerySet of Product instances
        serializer = AllProductSerializer(
            # Use many=True to indicate multiple objects
            products, many=True, context={'request': request})
        return Response(serializer.data)












# @api_view(['GET'])
# @permission_classes([AllowAny])  # Allow any user to access this endpoint
# def category(request):
#     category = Category.objects.all()
#     serializer = CategorySerializer(category, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([AllowAny])  # Allow any user to access this endpoint
# def subcategory(request):
#     subcategory = SubCategory.objects.all()
#     serializer = SubCategorySerializer(subcategory, many=True)
#     return Response(serializer.data)