"""METRIC+ MR identifier: 11-pair D x R category enumeration.

Re-implements Sun et al. 2021 's input-domain x output-relation
framework as an automated identifier. The 11 D x R pairs:

  Input-domain categories (D, Sun 2021 Sec IV):
    D1 = "equivalent input" : x' is in the same equivalence class as x
    D2 = "subsume input"    : x' is a strict containment / superset of x
    D3 = "include input"    : x is contained within x'
    D4 = "permute input"    : x' is a permutation of x
    D5 = "negate input"     : x' is the additive inverse / opposite of x
    D6 = "scale input"      : x' = k * x for some scalar k

  Output-relation categories (R, Sun 2021 Sec IV):
    R1 = output equality        : f(x') == f(x)
    R2 = output set equivalence : set(f(x')) == set(f(x))
    R3 = output multiplicative  : f(x') == k * f(x) for scaling k
    R4 = output containment     : f(x') subset/superset of f(x)
    R5 = output prefix equality : prefix relation on f outputs

Sun 2021 uses 11 valid D x R pairs out of 6 * 5 = 30; not all
combinations are non-vacuous for scalar-output programs.

This file enumerates Set MP per subject by binding each D x R pair
to category-choice instances. Vacuous pairs (e.g. R2 on scalar
output) are skipped.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mr_types import MR, approx_eq, approx_le, approx_ge, scale_outputs


# ----------------- SPHONE -----------------
def metricplus_mrs_sphone():
    mrs = []

    # (D1, R1) Equivalent input -> equal output.
    # Within-quota changes are equivalent (no metering effect).
    for new_time in [0, 25, 50, 80]:
        def tr(x, t=new_time):
            from sphone import PLANS  # type: ignore
            p = PLANS[x["plan"]]
            # If both current and new are below quota, equivalence holds
            if x["call_time_min"] > p["min_quota"] or t > p["min_quota"]:
                return None
            return {**x, "call_time_min": t}
        mrs.append(MR(f"MP.D1R1.equiv_time_inplan_{new_time}", "(D1,R1)",
                      tr, approx_eq, "MP"))

    for new_data in [0, 100, 250, 400]:
        def tr(x, d=new_data):
            from sphone import PLANS  # type: ignore
            p = PLANS[x["plan"]]
            if x["data_mb"] > p["data_quota"] or d > p["data_quota"]:
                return None
            return {**x, "data_mb": d}
        mrs.append(MR(f"MP.D1R1.equiv_data_inplan_{new_data}", "(D1,R1)",
                      tr, approx_eq, "MP"))

    # (D2, R4) Subsume input -> output containment (monotone).
    # Adding to time/data only increases bill.
    for delta in [10, 50, 100, 300]:
        def tr(x, d=delta):
            return {**x, "call_time_min": x["call_time_min"] + d}
        mrs.append(MR(f"MP.D2R4.add_time_+{delta}", "(D2,R4)",
                      tr, approx_le, "MP"))

    for delta in [50, 200, 500, 1500]:
        def tr(x, d=delta):
            return {**x, "data_mb": x["data_mb"] + d}
        mrs.append(MR(f"MP.D2R4.add_data_+{delta}", "(D2,R4)",
                      tr, approx_le, "MP"))

    # (D6, R3) Scale input -> scale output (when in linear regime).
    for k in [2, 3, 5]:
        def tr(x, sk=k):
            from sphone import PLANS  # type: ignore
            p = PLANS[x["plan"]]
            # Only fire when in overflow regime (linear)
            if x["data_mb"] <= p["data_quota"]:
                return None
            return {**x, "data_mb": x["data_mb"] * sk}
        def rel(y, yp, sk=k):
            # Bill not exactly scaled (base + voice contribute fixed parts);
            # use directional monotonic check
            return yp >= y

        mrs.append(MR(f"MP.D6R3.scale_data_x{k}", "(D6,R3)",
                      tr, rel, "MP"))

    return mrs


# ----------------- SBAGGAGE -----------------
def metricplus_mrs_sbaggage():
    mrs = []

    # (D1, R1) Equivalent input (within allowance) -> equal output (zero fee).
    for new_count in [0, 1]:
        def tr(x, c=new_count):
            from sbaggage import FREE_ALLOWANCE  # type: ignore
            allow = FREE_ALLOWANCE[(x["region"], x["cabin"])]
            if x["count"] > allow["count"] or c > allow["count"]:
                return None
            return {**x, "count": c}
        mrs.append(MR(f"MP.D1R1.equiv_count_inalw_{new_count}", "(D1,R1)",
                      tr, approx_eq, "MP"))

    # (D2, R4) Subsume input (add bags / weight) -> output monotone.
    for delta in [1, 2, 3, 5]:
        def tr(x, d=delta):
            return {**x, "count": x["count"] + d}
        mrs.append(MR(f"MP.D2R4.add_count_+{delta}", "(D2,R4)",
                      tr, approx_le, "MP"))

    for delta in [5, 15, 30, 50]:
        def tr(x, d=delta):
            return {**x, "weight_kg": x["weight_kg"] + d}
        mrs.append(MR(f"MP.D2R4.add_weight_+{delta}", "(D2,R4)",
                      tr, approx_le, "MP"))

    # (D6, R3) Scale weight (overweight regime)
    for k in [2, 3]:
        def tr(x, sk=k):
            from sbaggage import FREE_ALLOWANCE, SPECIAL_BONUS_KG  # type: ignore
            allow = FREE_ALLOWANCE[(x["region"], x["cabin"])]
            free_wt = allow["weight"] + (SPECIAL_BONUS_KG if x["is_special"] else 0)
            if x["weight_kg"] <= free_wt:
                return None
            return {**x, "weight_kg": x["weight_kg"] * sk}
        mrs.append(MR(f"MP.D6R3.scale_weight_x{k}", "(D6,R3)",
                      tr, approx_le, "MP"))

    return mrs


# ----------------- SEXPENSE -----------------
def metricplus_mrs_sexpense():
    mrs = []

    # (D1, R1) Equivalent: when travel_method == fly, mileage value is irrelevant
    for new_mileage in [0, 100, 500, 2000]:
        def tr(x, m=new_mileage):
            if x["travel_method"] != "fly":
                return None
            return {**x, "mileage_km": m}
        mrs.append(MR(f"MP.D1R1.fly_mileage_inv_{new_mileage}", "(D1,R1)",
                      tr, approx_eq, "MP"))

    # (D2, R4) Add nights / meals / mileage -> output monotone
    for delta in [1, 2, 3, 5]:
        def tr(x, d=delta):
            return {**x, "hotel_nights": x["hotel_nights"] + d}
        mrs.append(MR(f"MP.D2R4.add_nights_+{delta}", "(D2,R4)",
                      tr, approx_le, "MP"))

    for delta in [1, 3, 6, 12]:
        def tr(x, d=delta):
            return {**x, "meal_count": x["meal_count"] + d}
        mrs.append(MR(f"MP.D2R4.add_meals_+{delta}", "(D2,R4)",
                      tr, approx_le, "MP"))

    for delta in [50, 200, 500, 1000]:
        def tr(x, d=delta):
            if x["travel_method"] == "fly":
                return None
            return {**x, "mileage_km": x["mileage_km"] + d}
        mrs.append(MR(f"MP.D2R4.add_mileage_+{delta}", "(D2,R4)",
                      tr, approx_le, "MP"))

    # (D6, R3) Scale mileage (drive only)
    for k in [2, 3]:
        def tr(x, sk=k):
            if x["travel_method"] != "drive" or x["mileage_km"] <= 0:
                return None
            return {**x, "mileage_km": x["mileage_km"] * sk}
        mrs.append(MR(f"MP.D6R3.scale_mileage_x{k}", "(D6,R3)",
                      tr, approx_le, "MP"))

    return mrs


# ----------------- SMEAL -----------------
def metricplus_mrs_smeal():
    mrs = []

    # (D2, R4) Add passengers -> output monotone
    for delta in [1, 10, 50]:
        def tr(x, d=delta):
            return {**x, "economy_count": x["economy_count"] + d}
        def rel(y, yp):
            return yp["total"] >= y["total"]
        mrs.append(MR(f"MP.D2R4.add_econ_+{delta}", "(D2,R4)",
                      tr, rel, "MP"))

    for delta in [1, 3, 10]:
        def tr(x, d=delta):
            return {**x, "business_count": x["business_count"] + d}
        def rel(y, yp):
            return yp["total"] >= y["total"]
        mrs.append(MR(f"MP.D2R4.add_biz_+{delta}", "(D2,R4)",
                      tr, rel, "MP"))

    # (D4, R1) Permute passenger composition with same totals
    # E.g. swap 1 econ -> 1 biz (total preserved); meal totals should remain equal
    def tr_swap_econ_biz(x):
        if x["economy_count"] < 1:
            return None
        return {**x, "economy_count": x["economy_count"] - 1,
                "business_count": x["business_count"] + 1}
    def rel_total_eq(y, yp):
        return y["total"] == yp["total"]
    mrs.append(MR("MP.D4R1.swap_econ_biz", "(D4,R1)",
                  tr_swap_econ_biz, rel_total_eq, "MP"))

    # (D6, R3) Scale all passengers (multiplicative)
    for k in [2, 3]:
        def tr(x, sk=k):
            tot = x["first_count"] + x["business_count"] + x["economy_count"]
            if tot == 0:
                return None
            if (x["vegan_count"] * sk + x["kosher_count"] * sk) > (tot * sk):
                return None
            return {**x,
                    "first_count": x["first_count"] * sk,
                    "business_count": x["business_count"] * sk,
                    "economy_count": x["economy_count"] * sk,
                    "vegan_count": x["vegan_count"] * sk,
                    "kosher_count": x["kosher_count"] * sk}
        def rel(y, yp, sk=k):
            return approx_eq(yp["total"], sk * y["total"])
        mrs.append(MR(f"MP.D6R3.scale_all_x{k}", "(D6,R3)",
                      tr, rel, "MP"))

    return mrs


METRICPLUS_REGISTRY = {
    "sphone": metricplus_mrs_sphone,
    "sbaggage": metricplus_mrs_sbaggage,
    "sexpense": metricplus_mrs_sexpense,
    "smeal": metricplus_mrs_smeal,
}


if __name__ == "__main__":
    for s in METRICPLUS_REGISTRY:
        mrs = METRICPLUS_REGISTRY[s]()
        pairs = sorted(set(m.block_or_pair for m in mrs))
        print(f"{s}: {len(mrs)} METRIC+ MRs across pairs {pairs}")
