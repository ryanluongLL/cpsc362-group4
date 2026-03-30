from django.contrib import admin

from .models import Address, PaymentMethodToken, UserAccount, UserProfile


admin.site.register(UserAccount)
admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(PaymentMethodToken)
