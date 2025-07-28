def get_max_lot(user):
    """Return max lot per day based on age, vibe, and subscription tier."""
    # user = dict with 'age', 'subscription', 'vibe', 'is_admin'
    if user.get('is_admin') or user.get('vip'):
        return float('inf')  # No cap for admins/VIPs
    if user.get('age', 0) < 18:
        return 0.1
    base = 0.2
    # Example: vibe increases cap, subscription tiers can also affect
    vibe_bonus = {'high': 0.05, 'medium': 0.02, 'low': 0.0}
    sub_bonus = {'pro': 0.05, 'plus': 0.025, 'free': 0.0}
    return base + vibe_bonus.get(user.get('vibe'), 0) + sub_bonus.get(user.get('subscription'), 0)