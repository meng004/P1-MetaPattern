#!/usr/bin/env python3
"""
Generate the human inter-rater kappa materials from the real 36 Set N MRs
(supplementary/S3_case_study/lrca_llm_labels.json). Produces:
  - items_to_rate.csv          : the 36 MRs raters classify (BLIND; no gold label)
  - rating_sheet_TEMPLATE.csv  : blank sheet each rater copies and fills
  - _gold_author_labels.csv    : the author's labels (HIDDEN KEY -- do NOT show
                                 raters before they finish; used only for the
                                 optional human-vs-author comparison)
Run: python3 make_items.py
"""
import csv, json, pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE.parent.parent / "supplementary" / "S3_case_study" / "lrca_llm_labels.json"

def main():
    items = json.load(open(SRC))["labels"]
    items_rows, gold_rows, sheet_rows = [], [], []
    for i, it in enumerate(items, 1):
        iid = "M%02d" % i
        items_rows.append({
            "item_id": iid,
            "subject": it["subject"],
            "mr_name": it["mr_name"],
            "input_relation_JIR": it["jir"],
            "output_relation_JOR": it["jor"],
        })
        gold_rows.append({"item_id": iid, "author_label": it["author_label"]})
        sheet_rows.append({"item_id": iid, "subject": it["subject"],
                           "mr_name": it["mr_name"], "category": "", "notes": ""})

    def dump(name, rows, fields):
        with open(HERE / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        print("wrote", name, "(%d rows)" % len(rows))

    dump("items_to_rate.csv", items_rows,
         ["item_id", "subject", "mr_name", "input_relation_JIR", "output_relation_JOR"])
    dump("rating_sheet_TEMPLATE.csv", sheet_rows,
         ["item_id", "subject", "mr_name", "category", "notes"])
    dump("_gold_author_labels.csv", gold_rows, ["item_id", "author_label"])
    print("\nDONE. %d items. Categories raters may use: "
          "G, O_le, T_star, T_rev, L_star, D_star, E_star, B_rel, orphan" % len(items_rows))

if __name__ == "__main__":
    main()
