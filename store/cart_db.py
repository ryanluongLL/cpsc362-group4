from .models import Cart, CartItem, Product


# =========================================================
# GET OR CREATE USER CART
# =========================================================

def get_user_cart(request):
    """
    Returns the Cart object for the logged-in user.
    Assumes user_id is stored in session.
    """
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    cart, created = Cart.objects.get_or_create(user_id=user_id)
    return cart


# =========================================================
# ADD ITEM TO DB CART
# =========================================================

def db_add_item(cart, product, quantity=1):
    """
    Adds product to DB cart or increases quantity if exists.
    """
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity}
    )

    if not created:
        item.quantity += quantity
        item.save()


# =========================================================
# REMOVE ITEM FROM DB CART
# =========================================================

def db_remove_item(cart, product_id):
    """
    Removes a product completely from DB cart.
    """
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()


# =========================================================
# INCREASE QUANTITY
# =========================================================

def db_increase_item(cart, product_id):
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        item.quantity += 1
        item.save()
    except CartItem.DoesNotExist:
        pass


# =========================================================
# DECREASE QUANTITY
# =========================================================

def db_decrease_item(cart, product_id):
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)

        item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

    except CartItem.DoesNotExist:
        pass


# =========================================================
# CLEAR DB CART
# =========================================================

def db_clear_cart(cart):
    """
    Deletes all items in cart.
    """
    CartItem.objects.filter(cart=cart).delete()


# =========================================================
# SESSION → DB MERGE (CRITICAL AFTER LOGIN)
# =========================================================

def merge_session_to_db(request):
    """
    Moves session cart into DB cart after login.
    MUST be called ONCE right after login success.
    """
    session_cart = request.session.get("cart", {})

    cart = get_user_cart(request)
    if not cart:
        return

    for product_id, qty in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
        except Product.DoesNotExist:
            continue

        db_add_item(cart, product, quantity=int(qty))

    # clear session cart after merge
    request.session["cart"] = {}
    request.session.modified = True