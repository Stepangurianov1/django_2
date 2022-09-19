from django.db import models

from authapp.models import User
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STD'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'
    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачено'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отмена'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    update = models.DateTimeField(verbose_name='обнавлен', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус', max_length=3, default=FORMING)
    ia_active = models.BooleanField(verbose_name='активность', default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        # return sum(list(map(lambda x: x.quantity, items)))
        return sum([item.quantity for item in items])

    #     пробую свой варинат второй с map точно рабочий

    def get_total_cost(self):
        items = self.orderitems.select_related()
        # return sum(list(map(lambda x: x.quantity, items)))
        return sum([item.get_product_cost() for item in items])

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.save()
        self.ia_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказы', related_name='orderitems', on_delete=models.CASCADE)
    # related_name сможем обратиться к OrderItem из Order по имени
    product = models.ForeignKey(Product, verbose_name='продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
# Create your models here.
