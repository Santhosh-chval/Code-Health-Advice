# ==========================================================
# Sample File: Contains multiple functions with varying complexity
# ==========================================================

def calculate_sum(a, b):
    """Simple function with low complexity (Rank A)."""
    return a + b


def check_number_status(n):
    """Moderate function with a few branches (Rank A or B)."""
    if n > 0:
        if n % 2 == 0:
            return "Positive Even"
        else:
            return "Positive Odd"
    elif n < 0:
        return "Negative"
    else:
        return "Zero"


def process_user_permissions(role, is_active, is_verified, has_subscription):
    """
    High complexity function (Rank C/D/F). 
    This will trigger warning alerts and the Improvised Code Template.
    """
    access_granted = False
    
    if is_active:
        if is_verified:
            if role == "Admin":
                if has_subscription:
                    access_granted = True
                else:
                    access_granted = False
            elif role == "Editor":
                if has_subscription:
                    access_granted = True
                else:
                    access_granted = False
            else:
                access_granted = False
        else:
            access_granted = False
    else:
        access_granted = False
        
    return access_granted