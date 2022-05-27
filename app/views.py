from django.contrib.auth import authenticate
from django.http.response import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from app.models import CartItem, Machine, Order, Residue, User
from app.serializers import (AddUser, CartItemCreateSerializer,
                             CartItemDetailSerializer,
                             CartItemUpdateSerializer, MachineSerializer,
                             OrderSerializer, ResidueSerializer,
                             UserSerializer)


class registerUser(APIView):
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


class UserViewset(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        Serializer = UserSerializer(user)
        return Response(Serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = AddUser(user, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewMachinesViewset(APIView):
    def post(self, request):
        serializer = MachineSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MachineViewset(APIView):
    def get_object(self, pk):
        try:
            return Machine.objects.get(pk=pk)
        except Machine.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        machine = self.get_object(pk)
        serializer = MachineSerializer(machine, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        machine = self.get_object(pk)
        serializer = MachineSerializer(
            machine, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Machinelist(viewsets.ReadOnlyModelViewSet):

    model = Machine
    serializer_class = MachineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['industry__location', 'discount', 'name']
    search_fields = ('name', 'industry__name')

    def get_queryset(self):
        machines = Machine.objects.all()
        return machines


class NewResiduesViewset(APIView):
    def post(self, request):
        serializer = ResidueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResidueViewset(APIView):
    def get_object(self, pk):
        try:
            return Residue.objects.get(pk=pk)
        except Residue.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        residue = self.get_object(pk)
        serializer = ResidueSerializer(residue)
        return Response(serializer.data)

    def put(self, request, pk):
        residue = self.get_object(pk)
        serializer = ResidueSerializer(
            residue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Residuelist(viewsets.ReadOnlyModelViewSet):

    model = Residue
    serializer_class = ResidueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_of_residue']
    search_fields = ('type_of_residue', 'quantity')

    def get_queryset(self):
        residues = Residue.objects.all()
        return residues


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        return user.order_set.all()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderDetailView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
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
        orders = Order.objects.filter(machine__industry=user)
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
