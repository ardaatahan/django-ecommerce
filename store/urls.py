from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    # API routes
    path('update_item/', views.update_item, name='update_item')
]
