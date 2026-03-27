from django.http import HttpResponse
from django.views.generic import ListView
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
