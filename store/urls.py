from django.urls import path

from . import views

urlpatterns = [
        #path("", views.index, name="index"),
        path("", views.HomeView.as_view(), name="something"),
        path("products/<str:asin>", views.ProductView.as_view(), name="something2")
]
