from django.urls import path
from .views import index, create_checkout_session, success

urlpatterns = [
    path('', index, name='index'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('success/', success, name='success'),
]
