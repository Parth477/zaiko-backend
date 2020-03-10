from django.urls import re_path
from . import views

urlpatterns = [

    re_path('suppliers', views.SupplierGetAndPostView.as_view()),

]
