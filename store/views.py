from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import redirect
from .models import Product, Review, Favorite
from accounts.models import UserAccount
from django.contrib import messages
from django.shortcuts import get_object_or_404

class HomeView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_queryset().first()
        user_id = self.request.session.get("user_id")
        context["product"] = product
        # Gets all reviews for the selected product, by order starting from newest.
        context["reviews"] = Review.objects.filter(product=product).order_by("-created_at")
        # Gets currently logged-in user
        context["current_user"] = UserAccount.objects.filter(id=user_id).first() if user_id else None
        return context


class ProductView(ListView):
    model = Product
    template_name = "product.html"
    context_object_name = "products"

    def get_queryset(self):
        # Matching details webpage to the UPC passed in the URL.
        return Product.objects.select_related("category").filter(upc=self.kwargs["upc"])

    def get_context_data(self, **kwargs):
        # Adds product and review data to template
        context = super().get_context_data(**kwargs)
        # Retrieves single product object from queryset
        product = self.get_queryset().first()
        # Sends product to template for display, and fetches all reviews for the specific product.
        context["product"] = product
        context["reviews"] = Review.objects.filter(product=product).order_by("-created_at")
        # Favorites logic starts here
        user_id = self.request.session.get("user_id")
        is_favorite = False
        if user_id and product:
            is_favorite = Favorite.objects.filter(
                user_id=user_id,
                product=product
            ).exists()
        context["is_favorite"] = is_favorite
        return context

    # Handles the user input, when user clicks submit button.
    def post(self, request, *args, **kwargs):
        product = self.get_queryset().first()
        user_id = request.session.get("user_id")
        # User must be logged in, to be valid.
        if not user_id:
            messages.error(request, "You must be logged in to leave a review.")
            return redirect(request.path)
        # Retrieves actual user object from database
        user = UserAccount.objects.filter(id=user_id).first()
        # Handles invalid or expired session data
        if not user:
            messages.error(request, "User session invalid. Please log in again.")
            return redirect("/accounts/login/")
        rating = int(request.POST.get("rating", 0))
        text = request.POST.get("text", "").strip()
        # User must leave a star rating with thier review.
        if rating <= 0 or not text:
            messages.error(request, "Please select a rating and write a review.")
            return redirect(request.path)
        # User cannot submit multiple reviews on same product.
        if Review.objects.filter(user=user, product=product).exists():
            messages.error(request, "You already reviewed this product.")
            return redirect(request.path)
        # Saves the review into database, linking it with relevant information.
        Review.objects.create(
            user=user,
            product=product,
            rating=request.POST.get("rating"),
            text=request.POST.get("text")
        )

        messages.success(request, "Review submitted successfully!")
        return redirect(request.path)

# For the logic of the favorite button
def toggle_favorite(request, product_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=403)

    # SAFE user lookup
    user = UserAccount.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": "Invalid user"}, status=403)

    # SAFE product lookup
    product = get_object_or_404(Product, id=product_id)

    try:
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            product=product
        )

        if not created:
            favorite.delete()
            return JsonResponse({"favorited": False})

        return JsonResponse({"favorited": True})

    except Exception as e:
        # This prevents the 500 HTML responses
        return JsonResponse({"error": str(e)}, status=500)

# For the other button, that leads to a seperate page of favorited items
class FavoritesView(ListView):
    template_name = "favorites.html"
    context_object_name = "favorites"

    def get_queryset(self):
        user_id = self.request.session.get("user_id")
        return Favorite.objects.select_related("product").filter(
            user_id=user_id
        )