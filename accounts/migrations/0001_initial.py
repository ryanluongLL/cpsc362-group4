import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("store", "0004_address_paymentmethodtoken_userprofile"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="UserAccount",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("username", models.CharField(max_length=150, unique=True)),
                        ("email", models.EmailField(max_length=254, unique=True)),
                        ("password", models.CharField(max_length=128)),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                    ],
                    options={
                        "db_table": "store_useraccount",
                        "verbose_name": "User Account",
                        "verbose_name_plural": "User Accounts",
                    },
                ),
                migrations.CreateModel(
                    name="UserProfile",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("first_name", models.CharField(blank=True, max_length=100)),
                        ("last_name", models.CharField(blank=True, max_length=100)),
                        ("phone_number", models.CharField(blank=True, max_length=20)),
                        ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="accounts.useraccount")),
                    ],
                    options={
                        "db_table": "store_userprofile",
                        "verbose_name": "User Profile",
                        "verbose_name_plural": "User Profiles",
                    },
                ),
                migrations.CreateModel(
                    name="Address",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("address_type", models.CharField(default="shipping", max_length=20)),
                        ("street_line_1", models.CharField(max_length=255)),
                        ("street_line_2", models.CharField(blank=True, max_length=255)),
                        ("city", models.CharField(max_length=100)),
                        ("state", models.CharField(max_length=100)),
                        ("postal_code", models.CharField(max_length=20)),
                        ("country", models.CharField(default="United States", max_length=100)),
                        ("is_default", models.BooleanField(default=False)),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="addresses", to="accounts.useraccount")),
                    ],
                    options={
                        "db_table": "store_address",
                        "verbose_name": "Address",
                        "verbose_name_plural": "Addresses",
                    },
                ),
                migrations.CreateModel(
                    name="PaymentMethodToken",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("stripe_customer_id", models.CharField(blank=True, max_length=255)),
                        ("stripe_payment_method_id", models.CharField(max_length=255, unique=True)),
                        ("card_brand", models.CharField(blank=True, max_length=50)),
                        ("card_last4", models.CharField(blank=True, max_length=4)),
                        ("exp_month", models.PositiveSmallIntegerField(blank=True, null=True)),
                        ("exp_year", models.PositiveSmallIntegerField(blank=True, null=True)),
                        ("is_default", models.BooleanField(default=False)),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payment_tokens", to="accounts.useraccount")),
                    ],
                    options={
                        "db_table": "store_paymentmethodtoken",
                        "verbose_name": "Payment Method Token",
                        "verbose_name_plural": "Payment Method Tokens",
                    },
                ),
            ],
        ),
    ]
