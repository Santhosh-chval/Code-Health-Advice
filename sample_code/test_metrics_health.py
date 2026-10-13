# ==========================================================
# Sample File 2: Syntactically Valid with High Complexity & Metrics
# ==========================================================

def simple_multiplier(x, y):
    
    return x * y


def complex_user_authentication(user_role, login_attempts, is_active, has_2fa, subscription_type):
   
    access_granted = False
    security_level = 0

    if is_active:
        if user_role == "Admin":
            if has_2fa:
                if subscription_type == "Enterprise":
                    access_granted = True
                    security_level = 5
                else:
                    access_granted = True
                    security_level = 4
            else:
                access_granted = False
                security_level = 1
        elif user_role == "Moderator":
            if login_attempts < 3:
                if has_2fa:
                    access_granted = True
                    security_level = 3
                else:
                    access_granted = False
                    security_level = 2
            else:
                access_granted = False
                security_level = 0
        else:
            if login_attempts < 2 and has_2fa:
                access_granted = True
                security_level = 1
            else:
                access_granted = False
                security_level = 0
    else:
        access_granted = False
        security_level = 0

    return access_granted, security_level