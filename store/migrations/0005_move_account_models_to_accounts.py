from django.db import migrations

# Migrating the user accounts to the app accounts.py
class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("store", "0004_address_paymentmethodtoken_userprofile"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name="Address"),
                migrations.DeleteModel(name="PaymentMethodToken"),
                migrations.DeleteModel(name="UserProfile"),
                migrations.DeleteModel(name="UserAccount"),
            ],
        ),
    ]
