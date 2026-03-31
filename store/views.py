from django.views.generic import ListView
from .models import Product
from accounts.models import UserAccount

class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get("user_id")
        context["current_user"] = (
            UserAccount.objects.filter(id=user_id).first() if user_id else None
        )
        return context


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
