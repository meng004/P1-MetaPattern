"""
SEXPENSE: sales-department expense reimbursement.

Re-implemented from Sun 2021 Tables 11-12.

Inputs:
  staff_level:    "junior" | "senior" | "manager"
  travel_method:  "drive" | "fly" | "train"
  mileage_km:     float (distance traveled)
  hotel_nights:   int
  meal_count:     int

Output: reimbursement amount (dollars).
"""

# Per-mile / per-km rate by travel method
TRAVEL_RATE = {"drive": 0.55, "fly": 0.0, "train": 0.30}  # train/drive per km
# Per-night hotel cap by staff level
HOTEL_CAP = {"junior": 120, "senior": 180, "manager": 250}  # USD/night
# Per-meal cap
MEAL_CAP = {"junior": 30, "senior": 50, "manager": 75}  # USD/meal

# Fixed flight allowance by staff level
FLIGHT_ALLOWANCE = {"junior": 400, "senior": 700, "manager": 1200}


def compute_reimbursement(staff_level: str, travel_method: str,
                          mileage_km: float, hotel_nights: int,
                          meal_count: int) -> float:
    """SEXPENSE reimbursement function."""
    if staff_level not in HOTEL_CAP:
        raise ValueError(f"Unknown staff level: {staff_level}")
    if travel_method not in TRAVEL_RATE:
        raise ValueError(f"Unknown travel method: {travel_method}")
    if mileage_km < 0 or hotel_nights < 0 or meal_count < 0:
        raise ValueError("Negative inputs not allowed")

    amount = 0.0

    # Travel reimbursement
    if travel_method == "fly":
        amount = amount + FLIGHT_ALLOWANCE[staff_level]
    else:
        amount = amount + mileage_km * TRAVEL_RATE[travel_method]

    # Hotel (capped per night)
    amount = amount + hotel_nights * HOTEL_CAP[staff_level]

    # Meals (capped per meal)
    amount = amount + meal_count * MEAL_CAP[staff_level]

    return round(amount, 2)


INPUT_CATEGORIES = {
    "staff_level": {"junior": "junior", "senior": "senior",
                    "manager": "manager"},
    "travel_method": {"drive": "drive", "fly": "fly", "train": "train"},
    "mileage_km": {
        "zero": 0, "short": 50, "medium": 250, "long": 800,
    },
    "hotel_nights": {"zero": 0, "one": 1, "three": 3, "week": 7},
    "meal_count": {"zero": 0, "few": 3, "many": 9},
}


def sample_inputs():
    samples = []
    for sl_cat, sl in INPUT_CATEGORIES["staff_level"].items():
        for tm_cat, tm in INPUT_CATEGORIES["travel_method"].items():
            for mi_cat, mi in INPUT_CATEGORIES["mileage_km"].items():
                for hn_cat, hn in INPUT_CATEGORIES["hotel_nights"].items():
                    for mc_cat, mc in INPUT_CATEGORIES["meal_count"].items():
                        samples.append({
                            "staff_level": sl, "travel_method": tm,
                            "mileage_km": mi, "hotel_nights": hn,
                            "meal_count": mc,
                            "_meta": {"sl_cat": sl_cat, "tm_cat": tm_cat,
                                      "mi_cat": mi_cat, "hn_cat": hn_cat,
                                      "mc_cat": mc_cat},
                        })
    return samples


if __name__ == "__main__":
    print("junior drive 250km 2 nights 6 meals:",
          compute_reimbursement("junior", "drive", 250, 2, 6))
    print("manager fly 0km 5 nights 10 meals:",
          compute_reimbursement("manager", "fly", 0, 5, 10))
    print("Total test samples:", len(sample_inputs()))
