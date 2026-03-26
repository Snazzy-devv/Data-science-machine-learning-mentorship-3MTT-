import random

def generate_transaction(fraud=False):
    # Time
    t = random.uniform(0, 86400)
    
    # Amount
    if fraud:
        amt = random.uniform(1000, 2000)  # High amount for fraud
    else:
        amt = random.uniform(0, 200)      # Normal amount

    # V1–V28
    V = {}
    for i in range(1, 29):
        if fraud:
            # pick extreme values in PCA features
            V[f"V{i}"] = random.choice([random.uniform(-6, -3), random.uniform(3, 6)])
        else:
            # normal Gaussian values
            V[f"V{i}"] = random.gauss(0, 1.5)
    
    return t, amt, V
