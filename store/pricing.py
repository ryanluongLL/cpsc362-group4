MIN_MARGIN = 0.10; # 10% minimum profit margin

def get_competitor_price(upc):
    #fake competitor pcies for demo
    #API call later
    fake_competitor_prices = {
        "012345678901": 29.99,
        "098765432109": 14.99,
        "111222333444": 49.99,
    }
    return fake_competitor_prices.get(upc, None)

def compute_undercut_price(competitor_price):
    # undercut by 5%
    return round(competitor_price * 0.95, 2)

def check_constraints(undercut_price, our_cost):
    #make sure we still make at least 10%
    margin = (undercut_price - our_cost) / undercut_price
    return margin >= MIN_MARGIN

def run_pricing(product):
    #fetch competitor price
    competitor_price = get_competitor_price(product.upc)

    #check to see if competitor price is available
    if competitor_price is None:
        print(f"[LOG] Missing competitor data for {product.name}")
        return None
    
    #compute undercut price
    undercut_price = compute_undercut_price(competitor_price)

    #check constraints
    our_cost = float(product.price)
    if not check_constraints(undercut_price, our_cost):
        print(f"[LOG] Pricing exception: constraints not satisfied for {product.name}")
        print(f"[FLAG] Flagged for admin review")
        return None

    # publish new price
    print(f"[LOG] New price for {product.name}: ${undercut_price}")
    return undercut_price