from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from app.models import CartItem, Machine, Order, RentOrder, Residue, User
from app.serializers import (CartItemCreateSerializer,
                             CartItemDetailSerializer,
                             CartItemUpdateSerializer, MachineSerializer,
                             OrderSerializer, RentMachineSerializer,
                             RentOrderSerializer, ResidueSerializer,
                             UserSerializer, UserUpdateSerializer)


class registerUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        user = User.objects.create_user(
            data["username"], data["email"], data["password"])
        user.name = data["name"]
        user.is_industry = data["is_industry"]
        user.phone = data["phone"]
        user.location = data["location"]
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class login(APIView):
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({"Error": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(generics.RetrieveUpdateDestroyAPIView):

    def get_permissions(self):
        method = self.request.method
        if method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        if request.user != self.get_object():
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = UserUpdateSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object():
            return Response(status=status.HTTP_403_FORBIDDEN)

        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MachinesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MachineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['for_rent', 'owner__location', 'discount', 'name']
    search_fields = ('name', 'owner__name')

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            for_rent = self.request.query_params.get('for_rent')
            if for_rent:
                return RentMachineSerializer
            return MachineSerializer

        if method == 'POST':
            if self.request.user.is_industry:
                return MachineSerializer
            return RentMachineSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_industry:
            return user.machine_set.all()

        return Machine.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_industry:
            serializer.save(owner=self.request.user)
        else:
            serializer.save(owner=self.request.user, for_rent=True)


class MachineDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MachineSerializer

    def get_serializer_class(self):
        user = self.request.user
        if user.is_industry:
            return MachineSerializer

        machine = self.get_object()
        method = self.request.method
        if method == 'GET':
            if machine.owner == user:
                return RentMachineSerializer
            return MachineSerializer

        if machine.for_rent:
            return RentMachineSerializer
        return MachineSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_industry:
            return user.machine_set.all()
        return Machine.objects.all()

    def update(self, request, *args, **kwargs):
        machine = self.get_object()
        if machine.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(machine, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        machine = self.get_object()
        if machine.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        machine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResidueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Residue.objects.all()
    serializer_class = ResidueSerializer

    def update(self, request, *args, **kwargs):
        residue = self.get_object()
        if residue.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(residue, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, **kwargs):
        residue = self.get_object()
        if residue.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        residue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResiduesView(generics.ListCreateAPIView):
    serializer_class = ResidueSerializer
    queryset = Residue.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_of_residue']
    search_fields = ('type_of_residue', 'quantity')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrdersView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(machine__owner=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class RentOrdersView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RentOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        return RentOrder.objects.filter(machine__owner=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderDetailView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        machine = self.get_object().machine
        if machine.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            data = {"status": request.data['status']}
        except KeyError:
            raise ValidationError()

        order = self.get_object()
        serializer = self.get_serializer(order, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class Connections(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_industry:
            return Response(status=status.HTTP_403_FORBIDDEN)

        connections = []
        orders = Order.objects.filter(machine__owner=user)
        for order in orders:
            if order.status != Order.ACCEPTED:
                continue

            customer = order.customer
            if customer not in connections:
                connections.append(customer)

        serializer = UserSerializer(connections, many=True)
        return Response(serializer.data)


class CartView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def post(self, request, *args, **kwargs):
        cart = self.request.user.cart
        items = request.data['items']

        for item in items:
            item['cart'] = cart.id
            serializer = CartItemCreateSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class CartItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def put(self, request, *args, **kwargs):
        item = self.get_object()
        cart = item.cart
        if cart != self.request.user.cart:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            quantity = int(request.data["quantity"])
            if quantity < 1:
                raise ValidationError()
        except (KeyError, TypeError, ValueError, ValidationError):
            return Response({'quantity': ['quantity should be a positive integer']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartItemUpdateSerializer(instance=item, data={'quantity': quantity})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CartCheckoutView(APIView):
    def get(self, request, *args, **kwargs):
        cart = request.user.cart
        for item in cart.get_items():
            Order.objects.create(customer=request.user, machine=item.machine, quantity=item.quantity)
            item.delete()

        return Response(status=status.HTTP_200_OK)
