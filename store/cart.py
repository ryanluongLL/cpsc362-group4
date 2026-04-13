# =========================================================
# SESSION CART ONLY (GUEST USERS)
# =========================================================

def get_session_cart(session):
    """
    Returns the session cart dictionary.
    Format: { "product_id": quantity }
    """
    return session.get("cart", {})


def save_session_cart(session, cart):
    """
    Saves cart back into session safely.
    """
    session["cart"] = cart
    session.modified = True


# =========================================================
# CART MODE DETECTOR
# =========================================================

def get_cart_mode(request):
    """
    Returns:
        "db" -> logged-in user
        "session" -> guest user
    """
    return "db" if request.session.get("user_id") else "session"


# =========================================================
# BASIC SESSION CART OPERATIONS
# =========================================================

def session_add(session, product_id):
    cart = get_session_cart(session)
    pid = str(product_id)

    cart[pid] = cart.get(pid, 0) + 1
    save_session_cart(session, cart)


def session_remove(session, product_id):
    cart = get_session_cart(session)
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    save_session_cart(session, cart)


def session_clear(session):
    save_session_cart(session, {})


# =========================================================
# QUANTITY OPERATIONS
# =========================================================

def session_increase(session, product_id):
    cart = get_session_cart(session)
    pid = str(product_id)

    cart[pid] = cart.get(pid, 0) + 1
    save_session_cart(session, cart)


def session_decrease(session, product_id):
    cart = get_session_cart(session)
    pid = str(product_id)

    if pid in cart:
        cart[pid] -= 1

        if cart[pid] <= 0:
            del cart[pid]

    save_session_cart(session, cart)


# =========================================================
# OPTIONAL HELPERS (SAFE UTILITIES)
# =========================================================

def session_cart_count(session):
    """
    Returns total quantity of all items in session cart.
    Useful for navbar badge.
    """
    cart = get_session_cart(session)
    return sum(cart.values())