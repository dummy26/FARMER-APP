from django.conf.urls import url
from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *
from django.conf import settings
from django.conf.urls.static import static


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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
