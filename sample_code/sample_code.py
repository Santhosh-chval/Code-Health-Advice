# A sample file containing a mix of simple functions and a high-complexity function

def calculate_square(x):
    """Simple function: low complexity."""
    return x * x


def check_even_odd(number):
    """Simple conditional function: moderate complexity."""
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"


def process_user_checkout(cart_total, user_status, promo_code, is_express_shipping, payment_method):
    """
    Complex function with deep nesting and multiple conditional branches.
    This will trigger the High Risk warning (>10 complexity) in your dashboard.
    """
    discount = 0.0
    shipping_fee = 15.0
    
    if user_status == "premium":
        if cart_total > 100:
            if promo_code == "SAVE20":
                discount = 0.20
            elif promo_code == "SAVE10":
                discount = 0.10
            else:
                discount = 0.05
        else:
            if promo_code == "WELCOME":
                discount = 0.15
            else:
                discount = 0.0
    elif user_status == "regular":
        if cart_total > 200:
            if promo_code == "BIGSALE":
                discount = 0.15
            else:
                discount = 0.05
        else:
            discount = 0.0
    else:
        if promo_code == "FIRSTTIME":
            discount = 0.10
        else:
            discount = 0.0

    if is_express_shipping:
        if payment_method == "credit_card":
            shipping_fee = 25.0
        elif payment_method == "paypal":
            shipping_fee = 22.0
        else:
            shipping_fee = 30.0
    else:
        shipping_fee = 5.0

    final_price = (cart_total - (cart_total * discount)) + shipping_fee
    return final_price