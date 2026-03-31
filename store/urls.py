from django.urls import path

from . import views

urlpatterns = [
        path("", views.HomeView.as_view(), name="home"),
        path("products/<str:upc>", views.ProductView.as_view(), name="products")
]
