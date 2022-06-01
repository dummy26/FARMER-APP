from rest_framework import serializers

from app.models import (Bookmark, CartItem, Delivery, Machine, Order,
                        RentOrder, Residue, ResidueOrder, User)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email',
                  'phone', 'is_industry', 'location']
        extra_kwargs = {'password': {'write_only': True}}


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name',
                  'phone', 'is_industry', 'location']


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'owner', 'name', 'description', 'details', 'warranty', 'guarantee', 'loyalty', 'for_sale', 'for_rent', 'sell_price', 'rent_price', 'discount', 'image']
        read_only_fields = ['id', 'owner']


class RentMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'owner', 'name', 'description', 'rent_price', 'discount', 'image']
        read_only_fields = ['id', 'owner']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class ResidueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residue
        fields = ['owner', 'type_of_residue', 'price', 'quantity']
        read_only_fields = ['owner']


class ResidueSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Residue
        fields = ['id', 'owner', 'type_of_residue', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'machine', 'quantity', 'status']
        read_only_fields = ['id', 'customer']


class RentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentOrder
        fields = ['id', 'customer', 'machine', 'num_of_days', 'status']
        read_only_fields = ['id', 'customer']


class ResidueOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidueOrder
        fields = ['customer', 'residue', 'status']
        read_only_fields = ['customer']


class ResidueOrderSerializer(serializers.ModelSerializer):
    residue = ResidueSerializer()

    class Meta:
        model = ResidueOrder
        fields = ['id', 'customer', 'residue', 'status']


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'machine', 'quantity']
        write_only_fields = ['cart']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'machine', 'quantity']
        read_only_fields = ['id']


class CartItemDetailSerializer(serializers.ModelSerializer):
    machine = MachineSerializer()

    class Meta:
        model = CartItem
        fields = ['machine', 'quantity']


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['machine', 'quantity']
        read_only_fields = ['machine']
