from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken import views as auth_views

from app.views import (CartCheckoutView, CartItemView, CartView, Connections,
                       MachineDetailView, MachinesView, NewResiduesViewset,
                       OrderDetailView, OrdersView, Residuelist,
                       ResidueViewset, UserViewset, login, registerUser)

urlpatterns = [
    path('register/', registerUser.as_view(), name='register'),
    path('login/', login.as_view(), name='login'),
    path('users/<int:pk>', UserViewset.as_view(), name='user'),
    path('machines/', MachinesView.as_view(), name='machines'),
    path('machines/<int:pk>', MachineDetailView.as_view(), name='machine'),
    path('residue/<int:pk>', ResidueViewset.as_view(), name='residue'),
    path('residue/', NewResiduesViewset.as_view(), name='add-residue'),
    path('residues/',
         Residuelist.as_view({'get': 'list'}), name='residue-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart-items/<int:pk>', CartItemView.as_view(), name='cart-items'),
    path('cart/checkout', CartCheckoutView.as_view(), name='cart-checkout'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('connections/', Connections.as_view(), name='connections'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('token/', auth_views.obtain_auth_token)
]
