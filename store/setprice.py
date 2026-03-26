import os
import sys
import subprocess
import django
import pricing

sys.path.append('/Users/joel/coding/cpsc362/cpsc362-group4/')

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_site.settings')

# Initialize Django
django.setup()

from store.models import Product
all_products = Product.objects.all()

for item in all_products:
    print(item.name)
    result = subprocess.run(["node", "/Users/joel/coding/cpsc362/cpsc362-group4/store/price.mjs", item.asin], capture_output=True, text=True)
    print(result.stdout)

price = float(result.stdout)
undercut_price = pricing.run_pricing(price)
# publish new price
print(f"[LOG] New price for {item.name}: ${undercut_price}")
#return undercut_price
