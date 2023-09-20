from django.urls import path, include
from . import views

urlpatterns =[
    path('GET/booth-search', views.BoothSearchView.as_view(), name="boothSearch"),
]
