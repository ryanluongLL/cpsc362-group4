from accounts.models import UserAccount
from .cart import get_session_cart


# =========================================================
# GLOBAL CONTEXT PROCESSOR
# =========================================================

def global_context(request):
    """
    Provides global variables to all templates safely.
    MUST NOT modify session or database.
    """

    # --------------------
    # USER
    # --------------------
    user_id = request.session.get("user_id")
    current_user = None

    if user_id:
        current_user = UserAccount.objects.filter(id=user_id).first()

    # --------------------
    # CART COUNT (DISPLAY ONLY)
    # --------------------
    cart = get_session_cart(request.session)

    cart_item_count = sum(cart.values()) if cart else 0

    return {
        "current_user": current_user,
        "cart_item_count": cart_item_count,
    }