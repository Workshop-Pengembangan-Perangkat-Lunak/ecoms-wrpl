from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Customer, Product, TransactionDetail


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()


@receiver(post_save, sender=TransactionDetail)
def decrease_stock(sender, instance, created, **kwargs):
    if created:
        product = Product.objects.get(id=instance.product_id)
        product.stock = product.stock - instance.qty
        product.save()
