from django.urls import path

from . import views

urlpatterns = [
        #path("", views.index, name="index"),
        path("", views.HomeView.as_view(), name="something"),
        path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
        path("products/<str:upc>", views.ProductView.as_view(), name="something2")
        
]
