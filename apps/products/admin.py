from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Color, Size])
admin.site.register([Category, SubCategory, Product, ProductImage])
