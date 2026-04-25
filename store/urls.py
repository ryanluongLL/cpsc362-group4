from django.urls import path

from . import views

urlpatterns = [
        path("", views.HomeView.as_view(), name="home"),
        path("products/<str:upc>", views.ProductView.as_view(), name="products"),
        path('favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
        path("favorites/", views.FavoritesView.as_view(), name="favorites")
]
