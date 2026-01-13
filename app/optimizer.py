from typing import List
from app.models import Order, Truck
from app.validators import orders_compatible

def optimize(truck: Truck, orders: List[Order]):
    n = len(orders)

    if n == 0:
        return [], 0, 0, 0

    # Pre-compute compatibility matrix
    compat = [[True] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                compat[i][j] = orders_compatible(orders[i], orders[j])

    best_mask = 0
    best_payout = 0
    best_weight = 0
    best_volume = 0

    # Cache: mask -> (weight, volume, payout)
    dp = {}

    for mask in range(1, 1 << n):
        lsb = mask & -mask
        i = (lsb).bit_length() - 1
        prev = mask ^ lsb

        if prev in dp:
            w, v, p = dp[prev]
        else:
            w = v = p = 0

        order = orders[i]

        w += order.weight_lbs
        v += order.volume_cuft
        p += order.payout_cents

        if w > truck.max_weight_lbs or v > truck.max_volume_cuft:
            continue

        # Compatibility check
        ok = True
        for j in range(n):
            if prev & (1 << j):
                if not compat[i][j]:
                    ok = False
                    break

        if not ok:
            continue

        dp[mask] = (w, v, p)

        if p > best_payout:
            best_payout = p
            best_mask = mask
            best_weight = w
            best_volume = v

    selected = []
    for i in range(n):
        if best_mask & (1 << i):
            selected.append(orders[i].id)

    return selected, best_payout, best_weight, best_volume
