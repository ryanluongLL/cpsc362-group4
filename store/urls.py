from django.urls import path

from . import views

urlpatterns = [
        path("", views.HomeView.as_view(), name="home"),
        path("products/<str:upc>", views.ProductView.as_view(), name="products"),
        path("cart/", views.cart_view, name="cart"),
        path("cart/add/<int:product_id>/", views.add_to_cart_view, name="add_to_cart"),
        path("cart/remove/<int:product_id>/", views.remove_from_cart_view, name="remove_from_cart"),
        path("cart/add/ajax/<int:product_id>/", views.add_to_cart_ajax, name="add_to_cart_ajax"),
        path("cart/increase/ajax/<int:product_id>/", views.increase_qty_ajax),
        path("cart/decrease/ajax/<int:product_id>/", views.decrease_qty_ajax),
        path("cart/remove/ajax/<int:product_id>/", views.remove_item_ajax),
        path("checkout/", views.checkout_view, name="checkout"),
        path("place-order/", views.place_order, name="place_order"),
        path("order-success/", views.order_success, name="order_success"),


]
