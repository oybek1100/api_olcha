from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Category Name')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Category Image')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Category')
    title = models.CharField(max_length=100, verbose_name='Subcategory Name')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Subcategory Image')

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return f'{self.category.title} - {self.title}'


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', verbose_name='Subcategory')
    title = models.CharField(max_length=100, verbose_name='Product Name')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Product Image')
    description = models.TextField(default='none', verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Price')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products', verbose_name='Owner')    

    def __str__(self):
        return self.title


class AttributeKey(models.Model):
    key_name = models.CharField(max_length=50, unique=True, verbose_name='Attribute Key')

    def __str__(self):
        return self.key_name


class AttributeValue(models.Model):
    value_name = models.CharField(max_length=255, verbose_name='Attribute Value')

    def __str__(self):
        return self.value_name


class Attribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes', verbose_name='Product')
    attribute_key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE, verbose_name='Key')
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, verbose_name='Value')

    def __str__(self):
        return f'{self.product.title} - {self.attribute_key.key_name} - {self.attribute_value.value_name}'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                              related_name='comments', db_index=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                            related_name='comments', db_index=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),  
            models.Index(fields=['owner', 'product']), 
        ]