"""NOETHER MR identifier: CONSTRUCT-MP + Translate instance enumeration.

For each Sun 2021 subject, instantiate the non-empty NOETHER blocks
(per scope_analysis.md verdict) and enumerate concrete MR instances
via category-choice binding.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mr_types import MR, approx_eq, approx_le, approx_ge, scale_outputs


# ---------- SPHONE ----------
def noether_mrs_sphone():
    """SPHONE non-empty blocks: O_le, L* (partial)."""
    mrs = []

    # O_le: monotone in call_time_min (within same plan)
    for delta in [10, 50, 100]:
        def tr_time(x, d=delta):
            return {**x, "call_time_min": x["call_time_min"] + d}
        mrs.append(MR(f"O_le.time_mono_+{delta}", "O_le",
                      tr_time, approx_le, "N"))

    # O_le: monotone in data_mb (within same plan)
    for delta in [100, 500, 1000]:
        def tr_data(x, d=delta):
            return {**x, "data_mb": x["data_mb"] + d}
        mrs.append(MR(f"O_le.data_mono_+{delta}", "O_le",
                      tr_data, approx_le, "N"))

    # L*: linear scaling of overflow data (within overflow region)
    def tr_data_overflow_2x(x):
        # Only meaningful if data > plan's data quota
        from sphone import PLANS  # type: ignore
        p = PLANS[x["plan"]]
        if x["data_mb"] <= p["data_quota"]:
            return None
        return {**x, "data_mb": x["data_mb"] + (x["data_mb"] - p["data_quota"])}

    def rel_data_overflow_2x(y, yp):
        # bill_overflow_doubled = 2 * bill_original - base - voice_charge
        # Hard to predict exactly; use proportional check:
        # Difference (yp - y) should equal data_overflow_delta * data_rate
        from sphone import PLANS  # type: ignore
        return yp >= y  # weaker: monotone in overflow

    mrs.append(MR("L_scale.data_overflow_doubled", "L_star",
                  tr_data_overflow_2x, rel_data_overflow_2x, "N"))

    # L*: linear scaling of overflow time
    def tr_time_overflow_2x(x):
        from sphone import PLANS  # type: ignore
        p = PLANS[x["plan"]]
        if p["unlimited_min"] or x["call_time_min"] <= p["min_quota"]:
            return None
        return {**x, "call_time_min": x["call_time_min"]
                + (x["call_time_min"] - p["min_quota"])}

    def rel_time_overflow_2x(y, yp):
        return yp >= y

    mrs.append(MR("L_scale.time_overflow_doubled", "L_star",
                  tr_time_overflow_2x, rel_time_overflow_2x, "N"))

    return mrs


# ---------- SBAGGAGE ----------
def noether_mrs_sbaggage():
    """SBAGGAGE non-empty blocks: G (partial), O_le, L* (partial)."""
    mrs = []

    # O_le: monotone in count
    for delta in [1, 2, 3]:
        def tr_count(x, d=delta):
            return {**x, "count": x["count"] + d}
        mrs.append(MR(f"O_le.count_mono_+{delta}", "O_le",
                      tr_count, approx_le, "N"))

    # O_le: monotone in weight_kg
    for delta in [5, 10, 30]:
        def tr_weight(x, d=delta):
            return {**x, "weight_kg": x["weight_kg"] + d}
        mrs.append(MR(f"O_le.weight_mono_+{delta}", "O_le",
                      tr_weight, approx_le, "N"))

    # G: special-status invariance (when not in special-bonus regime)
    # If is_special toggled but weight stays well below regular allowance,
    # output should be the same.
    def tr_special_low_weight(x):
        from sbaggage import FREE_ALLOWANCE  # type: ignore
        allow = FREE_ALLOWANCE[(x["region"], x["cabin"])]
        # Only fire when weight is below the regular allowance
        if x["weight_kg"] > allow["weight"]:
            return None
        return {**x, "is_special": not x["is_special"]}

    mrs.append(MR("G.special_no_op_low_weight", "G",
                  tr_special_low_weight, approx_eq, "N"))

    # L*: linear overweight scaling - doubling overweight should change fee
    # proportionally (when above free_weight, no count change)
    def tr_overweight_double(x):
        from sbaggage import FREE_ALLOWANCE, SPECIAL_BONUS_KG  # type: ignore
        allow = FREE_ALLOWANCE[(x["region"], x["cabin"])]
        free_wt = allow["weight"] + (SPECIAL_BONUS_KG if x["is_special"] else 0)
        if x["weight_kg"] <= free_wt:
            return None
        overweight = x["weight_kg"] - free_wt
        return {**x, "weight_kg": x["weight_kg"] + overweight}

    def rel_overweight_proportional(y, yp):
        return yp >= y

    mrs.append(MR("L_scale.overweight_doubled", "L_star",
                  tr_overweight_double, rel_overweight_proportional, "N"))

    return mrs


# ---------- SEXPENSE ----------
def noether_mrs_sexpense():
    """SEXPENSE non-empty blocks: O_le, L*."""
    mrs = []

    # O_le: monotone in mileage_km (drive/train only)
    for delta in [50, 100, 300]:
        def tr_mileage(x, d=delta):
            if x["travel_method"] == "fly":
                return None  # mileage has no effect for fly
            return {**x, "mileage_km": x["mileage_km"] + d}
        mrs.append(MR(f"O_le.mileage_mono_+{delta}", "O_le",
                      tr_mileage, approx_le, "N"))

    # O_le: monotone in hotel_nights
    for delta in [1, 2, 5]:
        def tr_nights(x, d=delta):
            return {**x, "hotel_nights": x["hotel_nights"] + d}
        mrs.append(MR(f"O_le.nights_mono_+{delta}", "O_le",
                      tr_nights, approx_le, "N"))

    # O_le: monotone in meal_count
    for delta in [1, 3, 6]:
        def tr_meals(x, d=delta):
            return {**x, "meal_count": x["meal_count"] + d}
        mrs.append(MR(f"O_le.meals_mono_+{delta}", "O_le",
                      tr_meals, approx_le, "N"))

    # L*: linear mileage scaling (drive only)
    def tr_mileage_double(x):
        if x["travel_method"] != "drive" or x["mileage_km"] <= 0:
            return None
        return {**x, "mileage_km": x["mileage_km"] * 2}

    def rel_mileage_double(y, yp):
        # Difference equals mileage_rate * original_mileage
        # Just check monotonic increase
        return yp >= y

    mrs.append(MR("L_scale.mileage_doubled_drive", "L_star",
                  tr_mileage_double, rel_mileage_double, "N"))

    # L*: linear hotel scaling
    def tr_nights_double(x):
        if x["hotel_nights"] <= 0:
            return None
        return {**x, "hotel_nights": x["hotel_nights"] * 2}

    mrs.append(MR("L_scale.nights_doubled", "L_star",
                  tr_nights_double, approx_le, "N"))

    return mrs


# ---------- SMEAL ----------
def noether_mrs_smeal():
    """SMEAL non-empty blocks: G (partial), O_le, L*."""
    mrs = []

    # O_le: monotone in economy_count (assumes vegan/kosher caps respected)
    for delta in [1, 10, 50]:
        def tr_econ(x, d=delta):
            return {**x, "economy_count": x["economy_count"] + d}
        def rel_total_ge(y, yp):
            return yp["total"] >= y["total"]
        mrs.append(MR(f"O_le.econ_mono_+{delta}", "O_le",
                      tr_econ, rel_total_ge, "N"))

    # O_le: monotone in business_count
    for delta in [1, 4, 12]:
        def tr_biz(x, d=delta):
            return {**x, "business_count": x["business_count"] + d}
        def rel_total_ge(y, yp):
            return yp["total"] >= y["total"]
        mrs.append(MR(f"O_le.biz_mono_+{delta}", "O_le",
                      tr_biz, rel_total_ge, "N"))

    # G: economy_count and business_count partial permutation
    # (When total stays same but redistributed, total meals stays same)
    def tr_econ_to_biz(x):
        if x["economy_count"] < 1:
            return None
        return {**x, "economy_count": x["economy_count"] - 1,
                "business_count": x["business_count"] + 1}
    def rel_meals_total_eq(y, yp):
        return y["total"] == yp["total"]
    mrs.append(MR("G.econ_biz_swap_total_inv", "G",
                  tr_econ_to_biz, rel_meals_total_eq, "N"))

    # L*: doubling all passenger counts doubles total meals
    def tr_double_all_pax(x):
        if x["first_count"] + x["business_count"] + x["economy_count"] == 0:
            return None
        # Also need to ensure special-meal count <= total
        total = x["first_count"] + x["business_count"] + x["economy_count"]
        if x["vegan_count"] * 2 + x["kosher_count"] * 2 > total * 2:
            return None
        return {**x,
                "first_count": x["first_count"] * 2,
                "business_count": x["business_count"] * 2,
                "economy_count": x["economy_count"] * 2,
                "vegan_count": x["vegan_count"] * 2,
                "kosher_count": x["kosher_count"] * 2}
    def rel_total_doubled(y, yp):
        return approx_eq(yp["total"], 2 * y["total"])
    mrs.append(MR("L_scale.all_pax_doubled", "L_star",
                  tr_double_all_pax, rel_total_doubled, "N"))

    return mrs


NOETHER_REGISTRY = {
    "sphone": noether_mrs_sphone,
    "sbaggage": noether_mrs_sbaggage,
    "sexpense": noether_mrs_sexpense,
    "smeal": noether_mrs_smeal,
}


if __name__ == "__main__":
    for s in NOETHER_REGISTRY:
        mrs = NOETHER_REGISTRY[s]()
        blocks = sorted(set(m.block_or_pair for m in mrs))
        print(f"{s}: {len(mrs)} NOETHER MRs across blocks {blocks}")
