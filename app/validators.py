from app.models import Order

def orders_compatible(a: Order, b: Order) -> bool:
    if a.origin != b.origin:
        return False
    if a.destination != b.destination:
        return False

    # Time window check (simplified)
    if a.pickup_date > b.delivery_date or b.pickup_date > a.delivery_date:
        return False

    # Hazmat: cannot mix hazmat with non-hazmat
    if a.is_hazmat != b.is_hazmat:
        return False

    return True
