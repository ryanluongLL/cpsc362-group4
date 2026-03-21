from django.db import models

# Create your models here.

# Database table for a product's primary category. Add categories in admin
# Only primary categories for now, can add subcategories later if needed
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

# Database table for products and their attributes. 
# Comments are present for each line on this table as an example guide for team.
class Product(models.Model):
    name = models.CharField(max_length=250)
    # Storing product names in text for display and search

    description = models.TextField(blank=True)
    # Storing an optional product description 

    upc = models.CharField(max_length=12, unique=True)
    # Universal Product Code, unique identifier of product across every retailer (candidate key) 
    # Use to implement Amazon price comparison feature; e.g match UPC to ASIN and return price

    asin = models.CharField(max_length=10, unique=True, blank=True, null=True)
    # Optional Amazon Standard Identification Number (ASIN) for product ID
    # Use for future Amazon price comparison feature 

    price = models.DecimalField(max_digits=10, decimal_places=2)
    # 10 total digits for dollars, 2 decimals for cents 

    discount_price=models.DecimalField(max_digits=10, decimal_places=2, blank = True, null = True)
    # Optional discount price for salesmatch function 

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # FK relating 'category' to the Category table. Only 1 category per product for the time being
    # Note that if a category gets deleted, all products of that category will also be deleted 

    created_at = models.DateTimeField(auto_now_add=True)
    # Storing the date each product is created in system, aka added to the site. 
    # Use to implement sort by newest feature 

    popularity = models.PositiveIntegerField(default=0)
    # Storing how many times a product is purchased to quantify popularity. 
    # Use to implement sort by popular feature

    image_url = models.URLField(blank=True)
    # Storing URL to image of product. Reliable image host needed
    # Alternately can install Pillow to directly use images. e.g; image = models.ImageField()

    # slug = models.SlugField(unique=True)
    # Use to generate SEO urls, adding later 
    
    def __str__(self):
        return self.name 

    
