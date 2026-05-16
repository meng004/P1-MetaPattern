"""
SBAGGAGE: Air China baggage billing service.

Re-implemented from Sun 2021 Tables 9-10 (prose spec).

Inputs:
  count:        int (number of bags, 0..)
  weight_kg:    float (total weight)
  region:       "domestic" | "international"
  cabin:        "economy" | "business" | "first"
  is_special:   bool (frequent flyer / staff / etc.)

Output: baggage fee in dollars.
"""

# Free allowance by cabin and region
FREE_ALLOWANCE = {
    ("domestic", "economy"): {"count": 1, "weight": 20},
    ("domestic", "business"): {"count": 2, "weight": 30},
    ("domestic", "first"): {"count": 2, "weight": 40},
    ("international", "economy"): {"count": 1, "weight": 23},
    ("international", "business"): {"count": 2, "weight": 32},
    ("international", "first"): {"count": 3, "weight": 40},
}
SPECIAL_BONUS_KG = 10  # extra free weight for frequent flyers
OVERWEIGHT_RATE = {"domestic": 5.0, "international": 12.0}  # $/kg
OVERCOUNT_FEE = {"domestic": 30.0, "international": 100.0}  # per extra bag


def compute_fee(count: int, weight_kg: float, region: str,
                cabin: str, is_special: bool) -> float:
    """SBAGGAGE billing function."""
    if count < 0 or weight_kg < 0:
        raise ValueError("Negative inputs not allowed")
    if region not in {"domestic", "international"}:
        raise ValueError(f"Unknown region: {region}")
    if cabin not in {"economy", "business", "first"}:
        raise ValueError(f"Unknown cabin: {cabin}")

    allowance = FREE_ALLOWANCE[(region, cabin)]
    free_count = allowance["count"]
    free_weight = allowance["weight"]
    if is_special:
        free_weight = free_weight + SPECIAL_BONUS_KG

    fee = 0.0

    # Excess bag count
    if count > free_count:
        fee = fee + (count - free_count) * OVERCOUNT_FEE[region]

    # Overweight
    if weight_kg > free_weight:
        fee = fee + (weight_kg - free_weight) * OVERWEIGHT_RATE[region]

    return round(fee, 2)


# Input categories for MR-identification enumeration
INPUT_CATEGORIES = {
    "count": {"zero": 0, "free": 1, "one_over": 2, "two_over": 3},
    "weight_kg": {
        "zero": 0,
        "within_econ": 15,
        "within_biz": 25,
        "within_first": 35,
        "overweight_small": 25,
        "overweight_large": 60,
    },
    "region": {"domestic": "domestic", "international": "international"},
    "cabin": {"economy": "economy", "business": "business", "first": "first"},
    "is_special": {"regular": False, "special": True},
}


def sample_inputs():
    """Generate test-input grid."""
    samples = []
    for cnt_cat, cnt in INPUT_CATEGORIES["count"].items():
        for wt_cat, wt in INPUT_CATEGORIES["weight_kg"].items():
            for region in INPUT_CATEGORIES["region"].values():
                for cabin in INPUT_CATEGORIES["cabin"].values():
                    for sp_cat, sp in INPUT_CATEGORIES["is_special"].items():
                        samples.append({
                            "count": cnt, "weight_kg": wt,
                            "region": region, "cabin": cabin,
                            "is_special": sp,
                            "_meta": {"cnt_cat": cnt_cat, "wt_cat": wt_cat,
                                      "sp_cat": sp_cat},
                        })
    return samples


if __name__ == "__main__":
    print("domestic econ regular 1 bag 18kg:",
          compute_fee(1, 18, "domestic", "economy", False))
    print("intl biz special 3 bags 50kg:",
          compute_fee(3, 50, "international", "business", True))
    print("Total test samples:", len(sample_inputs()))
