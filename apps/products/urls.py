from django.urls import path
from .views import *
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list-class'),
    path('sub_categories/', SubCategoryListView.as_view(), name='sub-category-list-class'),

    path('categories/<int:pk>/', CategoryView.as_view(), name='category'),
    path('sub_categories/<int:pk>/', SubCategoryView.as_view(), name='sub-category'),
    path('product/<str:slug>/', ProductView.as_view(), name='Product'),
]
