from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from wordcloud import WordCloud

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.models import compare_algorithms, mine_rules, prune_redundant_rules, serialize_itemsets
from src.preprocessing import (
    clean_groceries_data,
    co_occurrence_matrix,
    create_basket_matrix,
    item_frequency,
    monthly_transaction_counts,
    transaction_size_summary,
)


DATA_PATH = ROOT / "data" / "groceries.csv"
OUTPUT_DIR = ROOT / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
MIN_ITEM_FREQUENCY = 10
MIN_LIFT = 1.2
ACTIONABLE_CONFIDENCE = 0.05
DASHBOARD_CONFIDENCE = 0.05
DASHBOARD_SUPPORT = 0.001


CATEGORY_KEYWORDS = {
    "produce": (
        "fruit",
        "vegetables",
        "berries",
        "grapes",
        "onions",
        "potato",
        "salad",
        "herbs",
    ),
    "dairy": (
        "milk",
        "yogurt",
        "cheese",
        "curd",
        "butter",
        "cream",
        "dessert",
    ),
    "bakery": (
        "bread",
        "rolls",
        "buns",
        "pastry",
        "cake",
    ),
    "meat and seafood": (
        "sausage",
        "beef",
        "pork",
        "ham",
        "chicken",
        "meat",
        "fish",
        "turkey",
    ),
    "beverages": (
        "water",
        "soda",
        "beer",
        "wine",
        "coffee",
        "tea",
        "beverages",
        "juice",
        "liquor",
        "whisky",
    ),
    "pantry": (
        "flour",
        "sugar",
        "rice",
        "pasta",
        "oil",
        "sauce",
        "spices",
        "salt",
        "vinegar",
        "canned",
        "soups",
    ),
    "snacks and sweets": (
        "chocolate",
        "candy",
        "gum",
        "snack",
        "waffles",
        "honey",
        "jam",
    ),
    "household": (
        "detergent",
        "cleaner",
        "napkins",
        "toilet",
        "bags",
        "kitchen",
        "hygiene",
        "cosmetics",
        "spray",
    ),
}


def infer_category(item: str) -> str:
    item_text = str(item).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in item_text for keyword in keywords):
            return category
    return "other"


def pairwise_statistics(basket_df: pd.DataFrame, top_n: int = 35) -> pd.DataFrame:
    selected_items = item_frequency(basket_df).head(top_n).index
    selected = basket_df[selected_items].astype(bool)
    transaction_count = len(selected)
    rows = []

    for left, right in combinations(selected.columns, 2):
        left_values = selected[left]
        right_values = selected[right]
        both = int((left_values & right_values).sum())
        left_only = int((left_values & ~right_values).sum())
        right_only = int((~left_values & right_values).sum())
        neither = int((~left_values & ~right_values).sum())

        support_left = left_values.mean()
        support_right = right_values.mean()
        support_pair = both / transaction_count
        expected = support_left * support_right
        category_left = infer_category(left)
        category_right = infer_category(right)
        category_pair = " + ".join(sorted({category_left, category_right}))
        denominator = (both + left_only) * (right_only + neither) * (both + right_only) * (left_only + neither)
        chi_squared = (
            transaction_count * ((both * neither) - (left_only * right_only)) ** 2 / denominator
            if denominator
            else 0
        )
        rows.append(
            {
                "item_a": left,
                "item_b": right,
                "category_a": category_left,
                "category_b": category_right,
                "category_pair": category_pair,
                "cross_category": category_left != category_right,
                "co_occurrences": both,
                "support_a": support_left,
                "support_b": support_right,
                "pair_support": support_pair,
                "lift": support_pair / expected if expected else 0,
                "jaccard": support_pair / (support_left + support_right - support_pair)
                if support_left + support_right - support_pair
                else 0,
                "chi_squared": chi_squared,
            }
        )

    return pd.DataFrame(rows).sort_values(["lift", "co_occurrences"], ascending=False)


def category_pair_statistics(pair_stats: pd.DataFrame) -> pd.DataFrame:
    if pair_stats.empty:
        return pd.DataFrame()

    summary = (
        pair_stats.groupby(["category_pair", "cross_category"], as_index=False)
        .agg(
            pairs=("category_pair", "size"),
            total_co_occurrences=("co_occurrences", "sum"),
            avg_lift=("lift", "mean"),
            max_lift=("lift", "max"),
            avg_jaccard=("jaccard", "mean"),
            max_chi_squared=("chi_squared", "max"),
        )
        .sort_values(["cross_category", "avg_lift", "total_co_occurrences"], ascending=[False, False, False])
    )
    summary["avg_lift"] = summary["avg_lift"].round(3)
    summary["avg_jaccard"] = summary["avg_jaccard"].round(4)
    summary["max_lift"] = summary["max_lift"].round(3)
    summary["max_chi_squared"] = summary["max_chi_squared"].round(3)
    return summary.reset_index(drop=True)


def antecedent_category_summary(rules: pd.DataFrame) -> pd.DataFrame:
    if rules.empty:
        return pd.DataFrame()

    rows = []
    for _, row in rules.iterrows():
        for antecedent in row["antecedents"]:
            rows.append(
                {
                    "antecedent_category": infer_category(antecedent),
                    "antecedent_item": antecedent,
                    "consequents": ", ".join(sorted(row["consequents"])),
                    "lift": float(row["lift"]),
                    "confidence": float(row["confidence"]),
                    "support": float(row["support"]),
                }
            )

    summary = pd.DataFrame(rows)
    return (
        summary.groupby("antecedent_category", as_index=False)
        .agg(
            rules=("antecedent_item", "size"),
            unique_antecedents=("antecedent_item", "nunique"),
            avg_lift=("lift", "mean"),
            max_lift=("lift", "max"),
            avg_confidence=("confidence", "mean"),
            top_consequents=("consequents", lambda values: "; ".join(values.head(3))),
        )
        .sort_values(["max_lift", "avg_lift"], ascending=False)
        .round({"avg_lift": 3, "max_lift": 3, "avg_confidence": 3})
        .reset_index(drop=True)
    )


def basket_clusters(basket_df: pd.DataFrame, top_n: int = 30, clusters: int = 4) -> pd.DataFrame:
    top_items = item_frequency(basket_df).head(top_n).index
    matrix = basket_df[top_items].astype(int)
    basket_sizes = basket_df.sum(axis=1)

    try:
        from sklearn.cluster import KMeans

        labels = KMeans(n_clusters=clusters, random_state=42, n_init=10).fit_predict(matrix)
    except Exception:
        labels = pd.qcut(basket_sizes.rank(method="first"), clusters, labels=False)

    cluster_df = pd.DataFrame({"cluster": labels, "basket_size": basket_sizes.values})
    rows = []
    for cluster, group in cluster_df.groupby("cluster"):
        cluster_baskets = matrix.iloc[group.index]
        top_cluster_items = cluster_baskets.sum().sort_values(ascending=False).head(5)
        rows.append(
            {
                "cluster": int(cluster),
                "transactions": len(group),
                "avg_basket_size": round(group["basket_size"].mean(), 2),
                "top_items": ", ".join(top_cluster_items.index),
            }
        )
    return pd.DataFrame(rows).sort_values("cluster")


def save_eda_figures(cleaned_df: pd.DataFrame, basket_df: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    frequencies = item_frequency(basket_df)

    plt.figure(figsize=(10, 6))
    frequencies.head(20).sort_values().plot(kind="barh", color="#2f80ed")
    plt.title("Top 20 Items")
    plt.xlabel("Transactions")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "top_items.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    basket_df.sum(axis=1).plot(kind="hist", bins=20, color="#27ae60", edgecolor="white")
    plt.title("Transaction Size Distribution")
    plt.xlabel("Items per transaction")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "transaction_size_histogram.png", dpi=160)
    plt.close()

    plt.figure(figsize=(11, 9))
    sns.heatmap(co_occurrence_matrix(basket_df, top_n=20), cmap="YlGnBu")
    plt.title("Top Item Co-occurrence Heatmap")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "co_occurrence_heatmap.png", dpi=160)
    plt.close()

    monthly_transaction_counts(cleaned_df).plot(figsize=(10, 5), marker="o", color="#8e44ad")
    plt.title("Monthly Transaction Trend")
    plt.xlabel("Month")
    plt.ylabel("Transactions")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "monthly_transaction_trend.png", dpi=160)
    plt.close()

    text = " ".join(cleaned_df["itemDescription"])
    wordcloud = WordCloud(width=1200, height=700, background_color="white").generate(text)
    plt.figure(figsize=(12, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "product_wordcloud.png", dpi=160)
    plt.close()


def save_network_html(rules: pd.DataFrame) -> None:
    network_rules = rules.sort_values(["lift", "confidence"], ascending=False).head(75)
    graph = nx.Graph()
    for _, row in network_rules.iterrows():
        antecedents = str(row["antecedents"]).split(", ")
        consequents = str(row["consequents"]).split(", ")
        for antecedent in antecedents:
            for consequent in consequents:
                if antecedent and consequent:
                    graph.add_edge(antecedent, consequent, weight=float(row["lift"]))

    if graph.number_of_edges() == 0:
        return

    positions = nx.spring_layout(graph, seed=42, weight="weight")
    edge_x, edge_y = [], []
    for source, target in graph.edges():
        edge_x.extend([positions[source][0], positions[target][0], None])
        edge_y.extend([positions[source][1], positions[target][1], None])

    node_x = [positions[node][0] for node in graph.nodes()]
    node_y = [positions[node][1] for node in graph.nodes()]
    node_degree = [graph.degree(node) for node in graph.nodes()]

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1, color="#9aa4b2")))
    figure.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=list(graph.nodes()),
            textposition="top center",
            marker=dict(size=10, color=node_degree, colorscale="Viridis", showscale=True),
        )
    )
    figure.update_layout(
        title="Interactive Product Association Network",
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    figure.write_html(OUTPUT_DIR / "product_network.html")


def write_reports(
    cleaned_df: pd.DataFrame,
    basket_df: pd.DataFrame,
    pair_stats: pd.DataFrame,
    category_pairs: pd.DataFrame,
    comparison: pd.DataFrame,
    rules: pd.DataFrame,
    strict_rules: pd.DataFrame,
    antecedent_summary: pd.DataFrame,
    clusters: pd.DataFrame,
) -> None:
    sizes = transaction_size_summary(basket_df)
    monthly = monthly_transaction_counts(cleaned_df)
    top_items = item_frequency(basket_df).head(10)
    raw_product_count = cleaned_df["itemDescription"].nunique()
    removed_products = raw_product_count - basket_df.shape[1]

    (OUTPUT_DIR / "eda_report.md").write_text(
        "\n".join(
            [
                "# EDA Report",
                "",
                f"- Raw rows after cleaning: {len(cleaned_df):,}",
                f"- Transactions: {len(basket_df):,}",
                f"- Unique products after rare-item filtering: {basket_df.shape[1]:,}",
                f"- Rare products removed with min frequency {MIN_ITEM_FREQUENCY}: {removed_products:,}",
                f"- Average basket size: {sizes['mean']:.2f}",
                f"- Median basket size: {sizes['50%']:.2f}",
                f"- Date range: {cleaned_df['Date'].min().date()} to {cleaned_df['Date'].max().date()}",
                f"- Busiest month: {monthly.idxmax().strftime('%Y-%m')} ({int(monthly.max()):,} transactions)",
                "",
                "## Top Products",
                "",
                top_items.to_frame("transactions").to_markdown(),
                "",
                "## Seasonal Trend",
                "",
                f"Monthly transaction counts range from {int(monthly.min()):,} to {int(monthly.max()):,}; the busiest month is {monthly.idxmax().strftime('%Y-%m')}.",
                "",
                "Figures are saved in `outputs/figures/`, including item frequency, basket size, co-occurrence heatmap, word cloud, and monthly transaction trend.",
            ]
        ),
        encoding="utf-8",
    )

    (OUTPUT_DIR / "co_occurrence_report.md").write_text(
        "\n".join(
            [
                "# Co-occurrence Analysis Report",
                "",
                "The table below ranks top product pairs by lift, with chi-squared and Jaccard similarity included for statistical context.",
                "",
                pair_stats.head(15).to_markdown(index=False),
                "",
                "## Cross-category Opportunities",
                "",
                category_pairs.head(10).to_markdown(index=False),
                "",
                "## Basket Segments",
                "",
                clusters.to_markdown(index=False),
            ]
        ),
        encoding="utf-8",
    )

    (OUTPUT_DIR / "mining_report.md").write_text(
        "\n".join(
            [
                "# Mining Report",
                "",
                "Apriori and FP-Growth were compared using relaxed thresholds suitable for this sparse dataset: confidence >= 0.05 and lift >= 1.2.",
                "",
                comparison.to_markdown(index=False),
                "",
                f"Actionable rule count at support >= {DASHBOARD_SUPPORT}, confidence >= {ACTIONABLE_CONFIDENCE}, and lift >= {MIN_LIFT}: {len(strict_rules):,}.",
                "",
                "The Groceries transactions are sparse, so the dashboard uses a practical confidence threshold of 0.05. A stricter 0.50 confidence threshold was tested but produced no rules.",
                "",
                "## Rules by Antecedent Category",
                "",
                antecedent_summary.to_markdown(index=False) if not antecedent_summary.empty else "No exploratory rules were available for grouping.",
                "",
                "## Top Rules",
                "",
                rules.head(15).to_markdown(index=False),
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    raw_df = pd.read_csv(DATA_PATH)
    cleaned_df = clean_groceries_data(raw_df)
    basket_df = create_basket_matrix(cleaned_df, min_item_frequency=MIN_ITEM_FREQUENCY)

    basket_df.astype(int).to_csv(OUTPUT_DIR / "transaction_matrix.csv")
    co_occurrence_matrix(basket_df, top_n=35).to_csv(OUTPUT_DIR / "co_occurrence_matrix.csv")

    pair_stats = pairwise_statistics(basket_df)
    pair_stats.to_csv(OUTPUT_DIR / "pairwise_statistics.csv", index=False)
    category_pairs = category_pair_statistics(pair_stats)
    category_pairs.to_csv(OUTPUT_DIR / "category_pair_statistics.csv", index=False)

    clusters = basket_clusters(basket_df)
    clusters.to_csv(OUTPUT_DIR / "cluster_summary.csv", index=False)

    comparison = compare_algorithms(
        basket_df,
        support_values=(DASHBOARD_SUPPORT, 0.0015, 0.002),
        min_confidence=DASHBOARD_CONFIDENCE,
        min_lift=MIN_LIFT,
    )
    comparison.to_csv(OUTPUT_DIR / "algorithm_comparison.csv", index=False)

    frequent_itemsets, rules = mine_rules(
        basket_df,
        algorithm="fpgrowth",
        min_support=DASHBOARD_SUPPORT,
        min_confidence=DASHBOARD_CONFIDENCE,
        min_lift=MIN_LIFT,
    )
    rules = prune_redundant_rules(rules)
    antecedent_summary = antecedent_category_summary(rules)
    antecedent_summary.to_csv(OUTPUT_DIR / "antecedent_rule_summary.csv", index=False)
    serialize_itemsets(frequent_itemsets).to_csv(OUTPUT_DIR / "frequent_itemsets_fpgrowth.csv", index=False)
    serialize_itemsets(rules).to_csv(OUTPUT_DIR / "rules.csv", index=False)

    strict_itemsets, strict_rules = mine_rules(
        basket_df,
        algorithm="fpgrowth",
        min_support=DASHBOARD_SUPPORT,
        min_confidence=ACTIONABLE_CONFIDENCE,
        min_lift=MIN_LIFT,
    )
    serialize_itemsets(strict_itemsets).to_csv(OUTPUT_DIR / "frequent_itemsets_actionable.csv", index=False)
    serialize_itemsets(prune_redundant_rules(strict_rules)).to_csv(
        OUTPUT_DIR / "rules_actionable.csv",
        index=False,
    )

    apriori_itemsets, apriori_rules = mine_rules(
        basket_df,
        algorithm="apriori",
        min_support=DASHBOARD_SUPPORT,
        min_confidence=DASHBOARD_CONFIDENCE,
        min_lift=MIN_LIFT,
    )
    serialize_itemsets(apriori_itemsets).to_csv(OUTPUT_DIR / "frequent_itemsets_apriori.csv", index=False)
    serialize_itemsets(prune_redundant_rules(apriori_rules)).to_csv(OUTPUT_DIR / "rules_apriori.csv", index=False)

    save_eda_figures(cleaned_df, basket_df)
    save_network_html(serialize_itemsets(rules))
    write_reports(
        cleaned_df,
        basket_df,
        pair_stats,
        category_pairs,
        comparison,
        serialize_itemsets(rules),
        serialize_itemsets(prune_redundant_rules(strict_rules)),
        antecedent_summary,
        clusters,
    )

    print(f"Generated outputs in {OUTPUT_DIR}")
    print(f"Transactions: {len(basket_df):,}; Products: {basket_df.shape[1]:,}; Rules: {len(rules):,}")


if __name__ == "__main__":
    main()
