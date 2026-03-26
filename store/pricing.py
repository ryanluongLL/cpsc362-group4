MIN_MARGIN = 0.10; # 10% minimum profit margin

def compute_undercut_price(competitor_price):
    # undercut by 5%
    return round(competitor_price * 0.95, 2)

def check_constraints(undercut_price, our_cost):
    #make sure we still make at least 10%
    margin = (undercut_price - our_cost) / undercut_price
    return margin >= MIN_MARGIN

def run_pricing(competitor_price, our_cost=None):
    
    #check to see if competitor price is available
    if competitor_price is None:
        print(f"[LOG] Missing competitor data")
        return None
    
    undercut_price = compute_undercut_price(competitor_price)

    # check constraints
    # if our_cost is not None:
    #     if not check_constraints(undercut_price, our_cost):
    #         print(f"[LOG] Pricing exception: constraints not satisfied for {product.name}")
    #         print(f"[FLAG] Flagged for admin review")
    #         return None

    return undercut_price
