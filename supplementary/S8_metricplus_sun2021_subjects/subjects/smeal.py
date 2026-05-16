"""
SMEAL: airline catering meal-ordering service.

Re-implemented from Sun 2021 Tables 13-14.

Inputs:
  first_count:    int (number of first-class passengers)
  business_count: int
  economy_count:  int
  vegan_count:    int (subset across classes)
  kosher_count:   int (subset across classes)
  flight_hours:   float

Output: dict of meal counts per type.
"""

VEGAN_FRAC_DEFAULT = 0.0  # vegan_count is explicit input
KOSHER_FRAC_DEFAULT = 0.0


def compute_meals(first_count: int, business_count: int, economy_count: int,
                  vegan_count: int, kosher_count: int,
                  flight_hours: float) -> dict:
    """SMEAL meal allocation function.

    Returns a dict {first, business, economy, vegan, kosher, total}.
    """
    if any(c < 0 for c in (first_count, business_count, economy_count,
                            vegan_count, kosher_count)):
        raise ValueError("Negative passenger counts not allowed")
    if flight_hours <= 0:
        raise ValueError("Flight hours must be positive")

    total_pax = first_count + business_count + economy_count

    # Meals per passenger based on flight duration
    if flight_hours < 2:
        meals_per_pax = 1
    elif flight_hours < 6:
        meals_per_pax = 2
    else:
        meals_per_pax = 3

    # Adjustments
    if total_pax == 0:
        return {"first": 0, "business": 0, "economy": 0,
                "vegan": 0, "kosher": 0, "total": 0}

    # First / business get premium meals (count each as 1.0 of allocation)
    # Special-diet meals override regular allocations for those passengers
    first_meals = first_count * meals_per_pax
    business_meals = business_count * meals_per_pax
    economy_meals = economy_count * meals_per_pax

    # Reduce regular allocations by special-diet pax (one for one)
    special_total = vegan_count + kosher_count
    if special_total > total_pax:
        raise ValueError("Special-diet count exceeds total passengers")

    # Allocate special meals primarily from economy first, then business, then first
    remaining_special = special_total
    if remaining_special > 0 and economy_count > 0:
        take = min(remaining_special, economy_count) * meals_per_pax
        economy_meals = economy_meals - take
        remaining_special = remaining_special - min(special_total, economy_count)
    if remaining_special > 0 and business_count > 0:
        take = min(remaining_special, business_count) * meals_per_pax
        business_meals = business_meals - take
        remaining_special = remaining_special - min(remaining_special, business_count)
    if remaining_special > 0 and first_count > 0:
        take = min(remaining_special, first_count) * meals_per_pax
        first_meals = first_meals - take

    vegan_meals = vegan_count * meals_per_pax
    kosher_meals = kosher_count * meals_per_pax

    total_meals = (first_meals + business_meals + economy_meals
                   + vegan_meals + kosher_meals)

    return {"first": first_meals, "business": business_meals,
            "economy": economy_meals, "vegan": vegan_meals,
            "kosher": kosher_meals, "total": total_meals}


INPUT_CATEGORIES = {
    "first_count": {"zero": 0, "few": 4, "many": 12},
    "business_count": {"zero": 0, "few": 8, "many": 24},
    "economy_count": {"zero": 0, "few": 40, "medium": 150, "many": 280},
    "vegan_count": {"zero": 0, "few": 3, "many": 15},
    "kosher_count": {"zero": 0, "few": 2, "many": 10},
    "flight_hours": {"short": 1.5, "medium": 4.5, "long": 9.0},
}


def sample_inputs():
    samples = []
    for fc_cat, fc in INPUT_CATEGORIES["first_count"].items():
        for bc_cat, bc in INPUT_CATEGORIES["business_count"].items():
            for ec_cat, ec in INPUT_CATEGORIES["economy_count"].items():
                for vc_cat, vc in INPUT_CATEGORIES["vegan_count"].items():
                    for kc_cat, kc in INPUT_CATEGORIES["kosher_count"].items():
                        for fh_cat, fh in INPUT_CATEGORIES["flight_hours"].items():
                            # Ensure special-diet count does not exceed total
                            total = fc + bc + ec
                            if vc + kc > total:
                                continue
                            samples.append({
                                "first_count": fc, "business_count": bc,
                                "economy_count": ec, "vegan_count": vc,
                                "kosher_count": kc, "flight_hours": fh,
                                "_meta": {"fc": fc_cat, "bc": bc_cat,
                                          "ec": ec_cat, "vc": vc_cat,
                                          "kc": kc_cat, "fh": fh_cat},
                            })
    return samples


if __name__ == "__main__":
    print("4F/8B/40E, 3 vegan, 2 kosher, 4.5h:",
          compute_meals(4, 8, 40, 3, 2, 4.5))
    print("Total test samples:", len(sample_inputs()))
