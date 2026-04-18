from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from decimal import Decimal

from .models import Product, Review, Order, OrderItem
from accounts.models import UserAccount

from .cart import (
    get_session_cart,
    session_add,
    session_remove,
    session_increase,
    session_decrease
)

from .cart_db import (
    get_user_cart,
    db_add_item,
    db_remove_item,
    db_increase_item,
    db_decrease_item,
    merge_session_to_db
)


# =========================================================
# HOME
# =========================================================

class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        products = Product.objects.select_related("category").order_by("-created_at")
        if query:
            products = products.filter(name__icontains=query) | products.filter(
                category__name__icontains=query
            )
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.session.get("user_id")
        context["current_user"] = UserAccount.objects.filter(id=user_id).first() if user_id else None

        return context


# =========================================================
# PRODUCT DETAIL
# =========================================================

class ProductView(ListView):
    model = Product
    template_name = "product.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(upc=self.kwargs["upc"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_queryset().first()
        context["product"] = product

        context["reviews"] = Review.objects.filter(product=product).order_by("-created_at")

        user_id = self.request.session.get("user_id")
        context["current_user"] = UserAccount.objects.filter(id=user_id).first() if user_id else None

        return context


# =========================================================
# CART VIEW (UNIFIED DISPLAY ONLY)
# =========================================================

def cart_view(request):
    products = []
    total = Decimal("0.00")

    user_id = request.session.get("user_id")

    # -------------------------
    # DB CART (LOGGED IN)
    # -------------------------
    if user_id:
        cart = get_user_cart(request)

        if cart:
            items = cart.items.select_related("product")

            for item in items:
                subtotal = item.product.price * item.quantity
                total += subtotal

                products.append({
                    "product": item.product,
                    "quantity": item.quantity,
                    "subtotal": subtotal
                })

    # -------------------------
    # SESSION CART (GUEST)
    # -------------------------
    else:
        cart = get_session_cart(request.session)

        for product_id, qty in cart.items():
            product = Product.objects.filter(id=product_id).first()
            if not product:
                continue

            qty = int(qty)
            subtotal = product.price * qty
            total += subtotal

            products.append({
                "product": product,
                "quantity": qty,
                "subtotal": subtotal
            })

    return render(request, "cart.html", {
        "products": products,
        "total": total
    })


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart_view(request, product_id):
    user_id = request.session.get("user_id")

    if user_id:
        cart = get_user_cart(request)
        product = get_object_or_404(Product, id=product_id)
        db_add_item(cart, product)
    else:
        session_add(request.session, product_id)

    return redirect(request.META.get("HTTP_REFERER", "cart"))


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart_view(request, product_id):
    user_id = request.session.get("user_id")

    if user_id:
        cart = get_user_cart(request)
        db_remove_item(cart, product_id)
    else:
        session_remove(request.session, product_id)

    return redirect("cart")


# =========================================================
# AJAX ADD
# =========================================================

def add_to_cart_ajax(request, product_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid"}, status=400)

    user_id = request.session.get("user_id")
    product = get_object_or_404(Product, id=product_id)

    if user_id:
        cart = get_user_cart(request)
        db_add_item(cart, product)

        total_items = sum(i.quantity for i in cart.items.all())
        return JsonResponse({"cart_count": total_items})

    session_add(request.session, product_id)
    return JsonResponse({"cart_count": sum(get_session_cart(request.session).values())})


# =========================================================
# AJAX INCREASE
# =========================================================

def increase_qty_ajax(request, product_id):
    if request.session.get("user_id"):
        cart = get_user_cart(request)
        db_increase_item(cart, product_id)
    else:
        session_increase(request.session, product_id)

    return cart_response(request)


# =========================================================
# AJAX DECREASE
# =========================================================

def decrease_qty_ajax(request, product_id):
    if request.session.get("user_id"):
        cart = get_user_cart(request)
        db_decrease_item(cart, product_id)
    else:
        session_decrease(request.session, product_id)

    return cart_response(request)


# =========================================================
# AJAX REMOVE ITEM
# =========================================================

def remove_item_ajax(request, product_id):
    if request.session.get("user_id"):
        cart = get_user_cart(request)
        db_remove_item(cart, product_id)
    else:
        session_remove(request.session, product_id)

    return cart_response(request)


# =========================================================
# CHECKOUT
# =========================================================

def checkout_view(request):
    products = []
    total = Decimal("0.00")

    user_id = request.session.get("user_id")

    # -------------------------
    # DB CART (LOGGED IN)
    # -------------------------
    if user_id:
        cart = get_user_cart(request)

        if cart:
            items = cart.items.select_related("product")

            for item in items:
                subtotal = item.product.price * item.quantity
                total += subtotal

                products.append({
                    "product": item.product,
                    "quantity": item.quantity,
                    "subtotal": subtotal
                })

    # -------------------------
    # SESSION CART (GUEST)
    # -------------------------
    else:
        cart = get_session_cart(request.session)

        for product_id, qty in cart.items():
            product = Product.objects.filter(id=product_id).first()
            if not product:
                continue

            qty = int(qty)
            subtotal = product.price * qty
            total += subtotal

            products.append({
                "product": product,
                "quantity": qty,
                "subtotal": subtotal
            })

    return render(request, "checkout.html", {
        "products": products,
        "total": total
    })


# =========================================================
# ORDER FLOW
# =========================================================

def place_order(request):
    if request.method != "POST":
        return redirect("checkout")

    user_id = request.session.get("user_id")

    name = request.POST.get("name")
    address = request.POST.get("address")
    city = request.POST.get("city")

    if user_id:
        cart = get_user_cart(request)

        if not cart.items.exists():
            return redirect("cart")

        order = Order.objects.create(
            user_id=user_id,
            name=name,
            address=address,
            city=city
        )

        for item in cart.items.select_related("product"):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

    else:
        request.session["cart"] = {}
        request.session.modified = True

    return redirect("order_success")

def order_success(request):
    return render(request, "order_success.html")


# =========================================================
# LOGIN MERGE (CALL ONCE AFTER LOGIN)
# =========================================================

def merge_after_login(request):
    merge_session_to_db(request)


def cart_response(request):
    cart = request.session.get("cart", {})

    items = []
    total = Decimal("0.00")
    total_items = 0

    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
        except Product.DoesNotExist:
            continue

        qty = int(qty)
        subtotal = product.price * qty

        total += subtotal
        total_items += qty

        items.append({
            "id": product.id,
            "quantity": qty,
            "subtotal": float(subtotal)
        })

    return JsonResponse({
        "items": items,
        "total": float(total),
        "cart_count": total_items
    })