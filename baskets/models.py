from django.db import models

# Create your models here.
from authapp.models import User
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для  {self.user.username} | Продукт{self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    # @property
    # def get_baskets(self):
    #     baskets = Basket.objects.filter(user=self.user)
    #     return baskets

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if self.pk:
            self.product.quantity -= 1
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(Basket, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # print(self.product.quantity)
        self.product.quantity += self.quantity
        print(self.product.quantity)
        self.save()
        super(Basket, self).delete(*args, **kwargs)
