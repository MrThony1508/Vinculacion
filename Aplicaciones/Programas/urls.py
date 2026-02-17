from django.urls import path 
from . import views
urlpatterns=[
    path('inicio3',views.inicio3, name='inicio3'),
]