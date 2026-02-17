from django.urls import path 
from . import views
urlpatterns=[
    path('inicio2',views.inicio2, name='inicio2'),
]