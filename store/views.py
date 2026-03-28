from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import render,redirect, get_object_or_404
from .models import Product

def index(request):
    return HttpResponse("You've reached the homepage for Meow Mart!")

class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        # Showing the newest products first.
        return Product.objects.select_related("category").order_by("-created_at")

class ProductView(ListView):
    model = Product
    template_name = "product.html"
    context_object_name = "products"

    def get_queryset(self):
        # Matching details webpage to the UPC passed in the URL.
        return Product.objects.select_related("category").filter(upc=self.kwargs["upc"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Template should receive only one object (product) for the selected UPC.
        context["product"] = self.get_queryset().first()
        return context

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'store'))

def cart_view(request):
    cart = request.session.get('cart', {})

    # Build a list of cart items with product info and quantity
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    if request.method == 'POST':
        # Handle update/remove form submission
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        if product_id and product_id in cart:
            if action == 'remove':
                del cart[product_id]
            elif action == 'update':
                try:
                    new_qty = int(request.POST.get('quantity', 1))
                    if new_qty > 0:
                        cart[product_id] = new_qty
                    else:
                        del cart[product_id]
                except ValueError:
                    pass
            request.session['cart'] = cart
            return redirect('cart')

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1  
        else:
            del cart[str(product_id)]   

    request.session['cart'] = cart
    return redirect('cart')  