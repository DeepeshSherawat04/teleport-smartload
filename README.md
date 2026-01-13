# SmartLoad Optimization API 

This project implements the core microservice behind Teleport’s **SmartLoad** feature.

Carriers can tap **“Find Best Loads”** in the mobile app and instantly receive the most profitable, legally and operationally valid combination of shipments that their truck can carry.

The service is fully **stateless**, **in-memory**, and optimized for **n ≤ 22 orders** using a combinatorial optimization strategy.

---

## What this service does

Given:
- A truck (weight & volume limits)
- A list of shipment orders

The API returns the best combination of orders that:
- Maximizes carrier revenue
- Does not exceed truck capacity
- Respects hazmat isolation
- Ensures all orders share the same route
- Ensures pickup & delivery windows do not conflict

---

## Optimization Strategy

The optimizer evaluates all valid subsets of orders (up to 2²² combinations) using:

- Constraint pruning (weight, volume, hazmat, time window, route)
- Efficient subset evaluation
- 64-bit integer arithmetic for all money values (no floats)

This guarantees:
- Correctness
- Deterministic optimal selection
- Execution under 1 second for the maximum input size

---

## 🧩 API

### Health Check

GET /healthz


Response:
```json
{ "status": "ok" }

Optimize Truck Load
POST /api/v1/load-optimizer/optimize


Input:

{
  "truck": {
    "id": "truck-123",
    "max_weight_lbs": 44000,
    "max_volume_cuft": 3000
  },
  "orders": [
    {
      "id": "ord-001",
      "payout_cents": 250000,
      "weight_lbs": 18000,
      "volume_cuft": 1200,
      "origin": "Los Angeles, CA",
      "destination": "Dallas, TX",
      "pickup_date": "2025-12-05",
      "delivery_date": "2025-12-09",
      "is_hazmat": false
    }
  ]
}


Response:

{
  "truck_id": "truck-123",
  "selected_order_ids": ["ord-001", "ord-002"],
  "total_payout_cents": 430000,
  "total_weight_lbs": 30000,
  "total_volume_cuft": 2100,
  "utilization_weight_percent": 68.18,
  "utilization_volume_percent": 70.0
}

How to run
1. Clone the repository
git clone https://github.com/DeepeshSherawat04/teleport-smartload.git
cd smartload

2. Start the service
docker compose up --build


The service will be available at:

http://localhost:8080

🔍 Verify

Health check:

curl http://localhost:8080/healthz


Run optimizer:

curl -X POST http://localhost:8080/api/v1/load-optimizer/optimize \
  -H "Content-Type: application/json" \
  -d @sample-request.json


(Windows PowerShell users can use Invoke-WebRequest instead.)

Architecture:

FastAPI
   ↓
Request Validation (Pydantic)
   ↓
Constraint Filtering
   ↓
Subset Optimization Engine
   ↓
Optimal Load Selection
   ↓
JSON Response

No database, no shared state, no external dependencies.