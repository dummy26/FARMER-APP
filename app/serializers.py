from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.models import (Bookmark, CartItem, Delivery, Machine, Order, Residue,
                        User)


class UserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    username = serializers.CharField(required=True, validators=[
                                     UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=10,)
    is_industry = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email',
                  'phone', 'is_industry', 'location', 'token']


class AddUser(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField(required=True, validators=[
                                     UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=10,)
    is_industry = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email',
                  'phone', 'is_industry', 'location', 'token']


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class ResidueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residue
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'machine', 'complete']
        read_only_fields = ['customer']


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["cart", "machine", "quantity"]
        write_only_fields = ['cart']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["machine", "quantity"]
