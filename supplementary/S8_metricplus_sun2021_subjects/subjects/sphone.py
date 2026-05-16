"""
SPHONE: China Unicom phone bill calculator.

Re-implemented from Sun et al. 2021 (METRIC+) Tables 7-8 (prose spec).
Reduced-scale Path A execution (full-scale Java port committed as
future work).

Input categories (Sun 2021 Table 7):
  call_time_min: 0..600+   (within-plan / overflow)
  data_mb:       0..2048+  (within-plan / overflow)
  plan:          A, B, C, D
Output relation categories (Sun 2021 Table 8): R1-R5 over the bill amount.
"""

# Plan tariff specs (within-plan minutes / data; overflow rates):
#   A: 100 min + 500 MB at base $30; overflow $0.20/min + $0.10/MB
#   B: 300 min + 1024 MB at base $50; overflow $0.15/min + $0.08/MB
#   C: 600 min + 2048 MB at base $80; overflow $0.10/min + $0.05/MB
#   D: unlimited min + 4096 MB at base $120; overflow data-only $0.04/MB

PLANS = {
    "A": {"base": 30.0, "min_quota": 100, "data_quota": 500,
          "min_rate": 0.20, "data_rate": 0.10, "unlimited_min": False},
    "B": {"base": 50.0, "min_quota": 300, "data_quota": 1024,
          "min_rate": 0.15, "data_rate": 0.08, "unlimited_min": False},
    "C": {"base": 80.0, "min_quota": 600, "data_quota": 2048,
          "min_rate": 0.10, "data_rate": 0.05, "unlimited_min": False},
    "D": {"base": 120.0, "min_quota": 0, "data_quota": 4096,
          "min_rate": 0.0, "data_rate": 0.04, "unlimited_min": True},
}


def compute_bill(call_time_min: float, data_mb: float, plan: str) -> float:
    """SPHONE billing function.

    Returns total monthly bill in dollars.
    """
    if plan not in PLANS:
        raise ValueError(f"Unknown plan: {plan}")
    if call_time_min < 0 or data_mb < 0:
        raise ValueError("Negative inputs not allowed")

    p = PLANS[plan]
    bill = p["base"]

    # Voice charge
    if not p["unlimited_min"]:
        overflow_min = max(0.0, call_time_min - p["min_quota"])
        bill = bill + overflow_min * p["min_rate"]

    # Data charge
    overflow_data = max(0.0, data_mb - p["data_quota"])
    bill = bill + overflow_data * p["data_rate"]

    return round(bill, 2)


# Category-choice domains for MR-identification enumeration
INPUT_CATEGORIES = {
    "call_time_min": {
        "zero": 0,
        "within_A": 50,         # < quota_A=100
        "within_B": 200,        # 100 < x < quota_B=300
        "within_C": 500,        # 300 < x < quota_C=600
        "overflow_A": 150,
        "overflow_B": 350,
        "overflow_C": 700,
    },
    "data_mb": {
        "zero": 0,
        "within_A": 250,        # < 500
        "within_B": 800,        # 500 < x < 1024
        "within_C": 1500,       # 1024 < x < 2048
        "within_D": 3000,       # 2048 < x < 4096
        "overflow_A": 600,
        "overflow_B": 1200,
        "overflow_C": 2500,
        "overflow_D": 5000,
    },
    "plan": {"A": "A", "B": "B", "C": "C", "D": "D"},
}


def sample_inputs():
    """Generate a deterministic test-input grid for MR evaluation.

    Returns a list of input dictionaries.
    """
    samples = []
    for time_cat, time_val in INPUT_CATEGORIES["call_time_min"].items():
        for data_cat, data_val in INPUT_CATEGORIES["data_mb"].items():
            for plan in INPUT_CATEGORIES["plan"].values():
                samples.append({
                    "call_time_min": time_val,
                    "data_mb": data_val,
                    "plan": plan,
                    "_meta": {"time_cat": time_cat, "data_cat": data_cat},
                })
    return samples


if __name__ == "__main__":
    # Quick sanity check
    print("Plan A, 50 min, 200 MB:", compute_bill(50, 200, "A"))
    print("Plan A, 150 min, 600 MB:", compute_bill(150, 600, "A"))
    print("Plan D, 1000 min, 5000 MB:", compute_bill(1000, 5000, "D"))
    print("Total test samples:", len(sample_inputs()))
