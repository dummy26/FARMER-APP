from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.db.models import fields


class UserSerializer(serializers.ModelSerializer):

  id = serializers.IntegerField()
  username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
  password = serializers.CharField(min_length=8, write_only=True)
  email = serializers.EmailField(required=True)
  phone = serializers.CharField(max_length=10,)
  is_industry = serializers.BooleanField(default=False)
  class Meta:
    model = User
    fields = ['id','username','password','name','email','phone','is_industry','location','token']

class AddUser(serializers.ModelSerializer):
  id = serializers.IntegerField()
  username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
  email = serializers.EmailField(required=True)
  phone = serializers.CharField(max_length=10,)
  is_industry = serializers.BooleanField(default=False)
  class Meta:
        model = User
        fields = ['id','username','name','email','phone','is_industry','location','token']

class MachineSerializer(serializers.ModelSerializer):
  class Meta:
    model = Machine
    fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
  
  machine = MachineSerializer()

  class Meta:
    model = Images
    fields = ['Machine','image']

class DeliverySerializer(serializers.ModelSerializer):
  class Meta:
    model = Delivery
    fields = '__all__'

class BookmarkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Bookmark
    fields = '__all__'
    