from urllib.parse import parse_qs, urlparse
from django.db import models
from accounts.models import UserAccount
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    upc = models.CharField(max_length=12, unique=True)
    asin = models.CharField(max_length=10, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    popularity = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)

    def converted_image_url(self):
        if not self.image_url:
            return ""
        parsed_url = urlparse(self.image_url)
        if "drive.google.com" not in parsed_url.netloc:
            return f"/static/{self.image_url}"
        path_parts = parsed_url.path.strip("/").split("/")
        if "d" in path_parts:
            drive_file_id = path_parts[path_parts.index("d") + 1]
            return f"https://drive.google.com/thumbnail?id={drive_file_id}&sz=w1000"
        drive_ids = parse_qs(parsed_url.query).get("id")
        if drive_ids:
            return f"https://drive.google.com/thumbnail?id={drive_ids[0]}&sz=w1000"
        return self.image_url

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} - {self.product} ({self.rating})"


class Favorite(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")


class Cart(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart({self.user})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
