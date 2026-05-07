from __future__ import annotations

from time import perf_counter
from typing import Iterable

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth


def _mine_frequent_itemsets(
    basket_df: pd.DataFrame,
    algorithm: str,
    min_support: float,
) -> pd.DataFrame:
    algorithm = algorithm.lower()
    if algorithm == "apriori":
        frequent_itemsets = apriori(basket_df, min_support=min_support, use_colnames=True)
    elif algorithm in {"fp-growth", "fpgrowth", "fp_growth"}:
        frequent_itemsets = fpgrowth(basket_df, min_support=min_support, use_colnames=True)
    else:
        raise ValueError("algorithm must be 'apriori' or 'fpgrowth'")

    if frequent_itemsets.empty:
        return frequent_itemsets

    frequent_itemsets = frequent_itemsets.copy()
    frequent_itemsets["itemset_length"] = frequent_itemsets["itemsets"].apply(len)
    frequent_itemsets = frequent_itemsets.sort_values(
        ["support", "itemset_length"], ascending=[False, False]
    )
    return frequent_itemsets.reset_index(drop=True)


def _rules_from_itemsets(
    frequent_itemsets: pd.DataFrame,
    min_confidence: float,
    min_lift: float,
) -> pd.DataFrame:
    if frequent_itemsets.empty:
        return pd.DataFrame()

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence,
    )
    if rules.empty:
        return rules

    rules = rules[rules["lift"] >= min_lift].copy()
    rules["antecedent_length"] = rules["antecedents"].apply(len)
    rules["consequent_length"] = rules["consequents"].apply(len)
    return rules.sort_values(["lift", "confidence", "support"], ascending=False).reset_index(drop=True)


def mine_rules(
    basket_df: pd.DataFrame,
    algorithm: str = "apriori",
    min_support: float = 0.01,
    min_confidence: float = 0.5,
    min_lift: float = 1.2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    frequent_itemsets = _mine_frequent_itemsets(basket_df, algorithm, min_support)
    rules = _rules_from_itemsets(frequent_itemsets, min_confidence, min_lift)
    if not rules.empty:
        rules["algorithm"] = algorithm
        rules["min_support_threshold"] = min_support
    return frequent_itemsets, rules


def run_apriori(
    basket_df: pd.DataFrame,
    min_support: float = 0.01,
    min_confidence: float = 0.5,
    min_lift: float = 1.2,
) -> pd.DataFrame:
    _, rules = mine_rules(basket_df, "apriori", min_support, min_confidence, min_lift)
    return rules


def run_fpgrowth(
    basket_df: pd.DataFrame,
    min_support: float = 0.01,
    min_confidence: float = 0.5,
    min_lift: float = 1.2,
) -> pd.DataFrame:
    _, rules = mine_rules(basket_df, "fpgrowth", min_support, min_confidence, min_lift)
    return rules


def compare_algorithms(
    basket_df: pd.DataFrame,
    support_values: Iterable[float] = (0.01, 0.02, 0.05),
    min_confidence: float = 0.5,
    min_lift: float = 1.2,
) -> pd.DataFrame:
    rows = []
    for algorithm in ("apriori", "fpgrowth"):
        for support in support_values:
            started_at = perf_counter()
            frequent_itemsets, rules = mine_rules(
                basket_df,
                algorithm=algorithm,
                min_support=support,
                min_confidence=min_confidence,
                min_lift=min_lift,
            )
            rows.append(
                {
                    "algorithm": algorithm,
                    "min_support": support,
                    "min_confidence": min_confidence,
                    "min_lift": min_lift,
                    "runtime_seconds": round(perf_counter() - started_at, 4),
                    "frequent_itemsets": len(frequent_itemsets),
                    "rules": len(rules),
                    "avg_lift": round(rules["lift"].mean(), 4) if not rules.empty else 0,
                    "avg_confidence": round(rules["confidence"].mean(), 4) if not rules.empty else 0,
                }
            )
    return pd.DataFrame(rows)


def prune_redundant_rules(rules: pd.DataFrame) -> pd.DataFrame:
    if rules.empty:
        return rules

    pruned = rules.copy()
    pruned["antecedents_key"] = pruned["antecedents"].apply(lambda values: tuple(sorted(values)))
    pruned["consequents_key"] = pruned["consequents"].apply(lambda values: tuple(sorted(values)))
    pruned = pruned.sort_values(["lift", "confidence", "support"], ascending=False)
    pruned = pruned.drop_duplicates(["antecedents_key", "consequents_key"])
    return pruned.drop(columns=["antecedents_key", "consequents_key"]).reset_index(drop=True)


def serialize_itemsets(df: pd.DataFrame) -> pd.DataFrame:
    serialized = df.copy()
    for column in ("itemsets", "antecedents", "consequents"):
        if column in serialized.columns:
            serialized[column] = serialized[column].apply(
                lambda values: ", ".join(sorted(values)) if isinstance(values, frozenset) else values
            )
    return serialized
