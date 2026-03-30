from django.db import models

# Separate models.py file for the account databases.

# Database for User Account, which is the PK for User Profile 
class UserAccount(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "store_useraccount"
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"

# Database for the User Profile, customizable by users in a future panel
class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    class Meta:
        db_table = "store_userprofile"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

# Database for Addresses, FK is User Account- for storing for quick shopping
class Address(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="addresses")
    address_type = models.CharField(max_length=20, default="shipping")
    street_line_1 = models.CharField(max_length=255)
    street_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="United States")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.address_type} address"

    class Meta:
        db_table = "store_address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class PaymentMethodToken(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="payment_tokens")
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payment_method_id = models.CharField(max_length=255, unique=True)
    card_brand = models.CharField(max_length=50, blank=True)
    card_last4 = models.CharField(max_length=4, blank=True)
    exp_month = models.PositiveSmallIntegerField(blank=True, null=True)
    exp_year = models.PositiveSmallIntegerField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.card_brand} ending in {self.card_last4}"

    class Meta:
        db_table = "store_paymentmethodtoken"
        verbose_name = "Payment Method Token"
        verbose_name_plural = "Payment Method Tokens"
