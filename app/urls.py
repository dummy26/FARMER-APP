from django.conf.urls import url
from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *


urlpatterns = [
  path('register/',registerUser.as_view(),name = 'register'),
  path('login/',login.as_view(),name = 'login'),
  path('user/<int:pk>',UserViewset.as_view(),name = 'User'),
  path('machine/',NewMachinesViewset.as_view(),name = 'add-machine'),
  path('machine/<int:pk>',MachineViewset.as_view(),name = 'machine'),
  path('machines/',Machinelist.as_view({'get':'list'}),name = 'machine-list'),
  
]