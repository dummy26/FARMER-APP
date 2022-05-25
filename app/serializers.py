from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.models import (Bookmark, Delivery, Machine, Order, OrderItem, Residue,
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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['machine', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = Order
        fields = ['customer', 'complete', 'order_items']
        read_only_fields = ['customer']

    def create(self, validated_data):
        order_items = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)

        for order_item in order_items:
            OrderItem.objects.create(order=order, **order_item)
        return order
