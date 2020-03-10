from django.urls import re_path
from . import views

urlpatterns = [

    re_path('orders', views.GetPostOrder.as_view()),
]
