import pandas as pd
import random
from datetime import datetime, timedelta

activities = [
    "Order Created",
    "Invoice Generated",
    "Payment Received",
    "Order Packed",
    "Order Shipped",
    "Order Delivered"
]

data = []
NUM_CASES = 200  # Large dataset

for i in range(1, NUM_CASES + 1):

    case_id = f"ORD_{i:04}"
    base_time = datetime(2026, 1, 1, 9, 0, 0)
    current_time = base_time + timedelta(days=random.randint(0, 10))

    for activity in activities:

        # 15% chance to stop process early (incomplete case)
        if random.random() < 0.15:
            break

        data.append({
            "case_id": case_id,
            "activity": activity,
            "timestamp": current_time
        })

        # Normal delay between steps
        delay_hours = random.randint(1, 12)
        current_time += timedelta(hours=delay_hours)

        # Introduce bottleneck at packing stage
        if activity == "Order Packed" and random.random() < 0.25:
            current_time += timedelta(hours=random.randint(12, 48))

df = pd.DataFrame(data)
df.to_csv("event_log.csv", index=False)

print("Large synthetic event log generated successfully.")
