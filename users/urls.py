from django.urls import re_path
from . import views

urlpatterns = [
    re_path('registration/', views.PostCustomerRegistration.as_view(),  name='registration'),
    re_path('verify-email/(?P<token>\w+)/$',views.VerifyMailAPI.as_view(), name='verify-email'),
    # re_path('details/',views.GetCutomer.as_view()),
    re_path('login/',views.UserLogin.as_view())
]