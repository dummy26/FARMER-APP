from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    location = models.TextField()
    is_industry = models.BooleanField(default=False)
    first_name = None
    last_name = None

    def __str__(self):
        return self.username


class Machine(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    details = models.JSONField(null=True, blank=True)
    warranty = models.IntegerField(default=3)  # number of years
    guarantee = models.IntegerField(default=1)  # number of years
    loyalty = models.BooleanField(default=False)
    for_sale = models.BooleanField(default=True)
    for_rent = models.BooleanField(default=False)
    sell_price = models.IntegerField(default=0)
    rent_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)  # percentage
    image = models.ImageField(upload_to='machine_images/')

    def __str__(self):
        return self.name


class Delivery(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller")
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer")
    payment = models.BooleanField(default=False)

    def __str__(self):
        return self.buyer + self.machine


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + self.machine


class Residue(models.Model):
    type_of_residue = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.type_of_residue


class Order(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, default=PENDING)

    def __str__(self):
        return f'{self.customer.name} {self.machine.name} {self.quantity} {str(self.status)}'


class RentOrder(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, default=PENDING)
    num_of_days = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.customer.name} {self.machine.name} {self.num_of_days} {str(self.status)}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_items(self):
        return self.cartitem_set.all()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.machine.name + ' ' + str(self.quantity)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance=None,  created=False, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)
