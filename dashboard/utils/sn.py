import random
from datetime import datetime

def generate_sn(asset):
    """Generate unique serial number for each signal."""
    now = datetime.utcnow()
    code = random.randint(1000,9999)
    return f"#SN-{code}-{asset}-{now.strftime('%m%d')}"