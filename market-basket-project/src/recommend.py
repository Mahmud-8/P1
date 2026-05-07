from __future__ import annotations

import ast
from collections import defaultdict
from typing import Iterable

import pandas as pd


def normalize_item(value: str) -> str:
    return str(value).strip().lower()


def parse_itemset(value) -> set[str]:
    if isinstance(value, (set, frozenset, list, tuple)):
        return {normalize_item(item) for item in value}

    text = str(value).strip()
    if not text or text.lower() == "nan":
        return set()

    for wrapper in ("frozenset", "set"):
        if text.startswith(wrapper):
            text = text.replace(wrapper, "", 1).strip()

    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, (set, frozenset, list, tuple)):
            return {normalize_item(item) for item in parsed}
    except (SyntaxError, ValueError):
        pass

    return {normalize_item(item) for item in text.split(",") if item.strip()}


def format_itemset(value) -> str:
    return ", ".join(sorted(parse_itemset(value)))


def recommend_items(
    cart_items: Iterable[str],
    rules: pd.DataFrame,
    top_n: int = 5,
    min_confidence: float = 0.0,
    min_lift: float = 0.0,
) -> pd.DataFrame:
    cart = {normalize_item(item) for item in cart_items if str(item).strip()}
    columns = ["item", "score", "lift", "confidence", "support", "matched_rule", "match_type"]
    if not cart or rules.empty:
        return pd.DataFrame(columns=columns)

    candidates = defaultdict(
        lambda: {
            "score": 0.0,
            "lift": 0.0,
            "confidence": 0.0,
            "support": 0.0,
            "matched_rule": "",
            "match_type": "",
        }
    )

    for _, row in rules.iterrows():
        confidence = float(row.get("confidence", 0))
        lift = float(row.get("lift", 0))
        support = float(row.get("support", 0))
        if confidence < min_confidence or lift < min_lift:
            continue

        antecedents = parse_itemset(row.get("antecedents", set()))
        consequents = parse_itemset(row.get("consequents", set()))
        if not antecedents or not consequents:
            continue

        full_match = cart.issubset(antecedents)
        partial_match = bool(cart.intersection(antecedents))
        if not (full_match or partial_match):
            continue

        score = lift * confidence
        match_type = "full antecedent match" if full_match else "partial antecedent match"
        matched_rule = f"{', '.join(sorted(antecedents))} -> {', '.join(sorted(consequents))}"
        for item in consequents.difference(cart):
            if score > candidates[item]["score"]:
                candidates[item].update(
                    {
                        "score": score,
                        "lift": lift,
                        "confidence": confidence,
                        "support": support,
                        "matched_rule": matched_rule,
                        "match_type": match_type,
                    }
                )

    if not candidates:
        return pd.DataFrame(columns=columns)

    recommendations = pd.DataFrame(
        [{"item": item, **metrics} for item, metrics in candidates.items()]
    )
    return recommendations.sort_values(
        ["match_type", "score", "lift", "confidence"],
        ascending=[True, False, False, False],
    ).head(top_n).reset_index(drop=True)


def recommend(items, rules):
    return recommend_items(items, rules)["item"].tolist()
