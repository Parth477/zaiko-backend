from django.urls import path
from . import views

urlpatterns = [

    path('categories', views.CategoryGetAndPostView.as_view()),

    path('products', views.ProductGetAndPostView.as_view()),

]
