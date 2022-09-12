from django.db import models


class ObjectsProduct(models.Manager):
    def get_queryset(self):
        return super(ObjectsProduct, self).get_queryset().all()


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    objects = ObjectsProduct()
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='product_image', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} | {self.category}'
