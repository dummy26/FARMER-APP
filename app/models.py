from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey
# Create your models here.

class User(AbstractUser):
  name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=10)
  location = models.TextField()
  is_industry = models.BooleanField(default=False)
  token = models.TextField(null=True,blank=True)

  def __str__(self):
        return self.name
  
class Machine(models.Model):
  name = models.CharField(max_length=200)
  industry = models.ForeignKey(User,on_delete=models.CASCADE)
  price = models.IntegerField(default=0)
  description = models.TextField()
  fetures = models.TextField()
  details = models.JSONField()
  discount = models.IntegerField(default = 0)#percentage
  warrenty = models.IntegerField(default=3)#number of years
  loyalty = models.BooleanField(default=False)
  guarantee = models.IntegerField(default = 1)#number of years
  sell = models.BooleanField(default = True)# if its for sale
  rent = models.BooleanField(default = False)#if its for rent

  def __str__(self):
        return self.name

class Images(models.Model):
  machine = models.ForeignKey(Machine,on_delete=models.CASCADE)
  image = models.ImageField(upload_to='machine_images/')

class Delivery(models.Model):
  seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name="seller")
  machine = models.ForeignKey(Machine,on_delete=models.CASCADE)
  buyer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="buyer")
  payment = models.BooleanField(default = False)

  def __str__(self):
        return self.buyer + self.machine

class Bookmark(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  machine = models.ForeignKey(Machine,on_delete=models.CASCADE)

  def __str__(self):
        return self.user + self.machine
        