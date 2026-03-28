from urllib.parse import parse_qs, urlparse

from django.db import models

# Create your models here.

# Database table for a product's primary category. Add categories and products in admin.
# Also has a urlparser to convert pesky Google Drive image links into their direct image links instead of previews. 
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

    # Converts the Google Drive image links into direct image links for the site embed using urllib (native Python library)
    def converted_image_url(self):
        if not self.image_url:
            return ""
    # Checks if it's a Google Drive link 
        parsed_url = urlparse(self.image_url)
        if "drive.google.com" not in parsed_url.netloc:
            #return self.image_url
            return f"/static/{self.image_url}"
    # Grabbing the ID of the file found in the preview URL, then converts it into direct image URL
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

    
