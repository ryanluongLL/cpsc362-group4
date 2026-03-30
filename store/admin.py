from django.contrib import admin
from .models import Address, Category, PaymentMethodToken, Product, UserAccount, UserProfile

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserAccount)
admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(PaymentMethodToken)
