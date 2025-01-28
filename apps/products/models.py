from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import default_storage
from apps.tools.compressor import *

# Create your models here.


class Color(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Color'

    def __str__(self):
        return f"{self.name}"


class Size(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Size'

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    banner = models.ImageField(upload_to='banner', blank=True, null=True)
    image = models.ImageField(upload_to='category_images')
    top = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.id}: {self.name}"

    def save(self, *args, **kwargs):
        try:
            old_instance = Category.objects.get(pk=self.pk)
            if self.banner != old_instance.banner:
                if old_instance.banner:
                    default_storage.delete(old_instance.banner.path)
                # Compress the new image
                self.banner = compress_image(self.banner, 50)
            if self.image != old_instance.image:
                if old_instance.image:
                    default_storage.delete(old_instance.image.path)
                # Compress the new image
                self.image = compress_image(self.image, 50)
        except:  # Create mode
            if self.banner:
                self.banner = compress_image(self.banner, 50)
            if self.image:
                self.image = compress_image(self.image, 50)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=300, blank=True, null=True)
    banner = models.ImageField(upload_to='banner', blank=True, null=True)
    image = models.ImageField(upload_to='subcategory_images')
    top = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return f"{self.id}: {self.name}"

    def save(self, *args, **kwargs):
        try:
            old_instance = SubCategory.objects.get(pk=self.pk)
            if self.banner != old_instance.banner:
                if old_instance.banner:
                    default_storage.delete(old_instance.banner.path)
                # Compress the new image
                self.banner = compress_image(self.banner, 50)
            if self.image != old_instance.image:
                if old_instance.image:
                    default_storage.delete(old_instance.image.path)
                # Compress the new image
                self.image = compress_image(self.image, 50)
        except:  # Create mode
            if self.banner:
                self.banner = compress_image(self.banner, 50)
            if self.image:
                self.image = compress_image(self.image, 50)
        super().save(*args, **kwargs)


class Product(models.Model):
    slug = models.SlugField(unique=True, max_length=255)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)

    stock = models.IntegerField(default=0, blank=True, null=True)
    price = models.IntegerField()
    discount = models.DecimalField(max_digits=2,  decimal_places=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0.01)
    ])
    point = models.IntegerField(default=0, blank=True, null=True)
    top = models.BooleanField(default=False)
    ratings = models.FloatField(default=0, validators=[
        MinValueValidator(0.0),
        MaxValueValidator(5.0)
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    @property
    def discount_price(self):
        return int(((self.price)*(self.discount))/100)

    @property
    def sell_price(self):
        return (self.price)-(self.discount_price)

    def __str__(self):
        return f"{self.id}: {self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="productimage", on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.DO_NOTHING, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING, blank=True, null=True)
    image = models.ImageField(upload_to='product_images')
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural = 'Product Images'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}: {self.product.name}"

    def save(self, *args, **kwargs):
        try:
            old_instance = ProductImage.objects.get(pk=self.pk)
            if self.image != old_instance.image:
                if old_instance.image:
                    default_storage.delete(old_instance.image.path)
                # Compress the new image
                self.image = compress_image(self.image, 50)
        except:  # Create mode
            if self.image:
                self.image = compress_image(self.image, 50)
        super().save(*args, **kwargs)

