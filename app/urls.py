from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken import views as auth_views

from .views import *

urlpatterns = [
    path('register/', registerUser.as_view(), name='register'),
    path('login/', login.as_view(), name='login'),
    path('user/<int:pk>', UserViewset.as_view(), name='User'),
    path('machine/', NewMachinesViewset.as_view(), name='add-machine'),
    path('machine/<int:pk>', MachineViewset.as_view(), name='machine'),
    path('machines/',
         Machinelist.as_view({'get': 'list'}), name='machine-list'),
    path('residue/<int:pk>', ResidueViewset.as_view(), name='residue'),
    path('residue/', NewResiduesViewset.as_view(), name='add-residue'),
    path('residues/',
         Residuelist.as_view({'get': 'list'}), name='residue-list'),
    path('orders/', OrdersView.as_view(), name='order-list'),
    path('connections/', Connections.as_view(), name='connections'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('token/', auth_views.obtain_auth_token)
]
