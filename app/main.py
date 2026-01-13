from fastapi import FastAPI, HTTPException
from app.models import OptimizeRequest, OptimizeResponse
from app.optimizer import optimize

app = FastAPI(title="SmartLoad Optimizer")

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/api/v1/load-optimizer/optimize", response_model=OptimizeResponse)
def run_optimizer(req: OptimizeRequest):

    if len(req.orders) > 22:
        raise HTTPException(status_code=413, detail="Too many orders (max 22)")

    selected, payout, weight, volume = optimize(req.truck, req.orders)

    if not selected:
        return OptimizeResponse(
            truck_id=req.truck.id,
            selected_order_ids=[],
            total_payout_cents=0,
            total_weight_lbs=0,
            total_volume_cuft=0,
            utilization_weight_percent=0,
            utilization_volume_percent=0
        )

    weight_util = round((weight / req.truck.max_weight_lbs) * 100, 2)
    volume_util = round((volume / req.truck.max_volume_cuft) * 100, 2)

    return OptimizeResponse(
        truck_id=req.truck.id,
        selected_order_ids=selected,
        total_payout_cents=payout,
        total_weight_lbs=weight,
        total_volume_cuft=volume,
        utilization_weight_percent=weight_util,
        utilization_volume_percent=volume_util
    )
