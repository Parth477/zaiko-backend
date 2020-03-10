from django.urls import re_path
from . import views

urlpatterns = [

    re_path('categories', views.CategoryGetAndPostView.as_view()),
    re_path('products/', views.ProductGetAndPostView.as_view()),

]
