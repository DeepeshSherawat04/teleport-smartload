from pydantic import BaseModel, Field
from typing import List
from datetime import date

class Truck(BaseModel):
    id: str
    max_weight_lbs: int = Field(gt=0)
    max_volume_cuft: int = Field(gt=0)

class Order(BaseModel):
    id: str
    payout_cents: int = Field(ge=0)
    weight_lbs: int = Field(gt=0)
    volume_cuft: int = Field(gt=0)
    origin: str
    destination: str
    pickup_date: date
    delivery_date: date
    is_hazmat: bool

class OptimizeRequest(BaseModel):
    truck: Truck
    orders: List[Order]

class OptimizeResponse(BaseModel):
    truck_id: str
    selected_order_ids: List[str]
    total_payout_cents: int
    total_weight_lbs: int
    total_volume_cuft: int
    utilization_weight_percent: float
    utilization_volume_percent: float
