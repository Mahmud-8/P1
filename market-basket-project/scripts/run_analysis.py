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
    comparison: pd.DataFrame,
    rules: pd.DataFrame,
    clusters: pd.DataFrame,
) -> None:
    sizes = transaction_size_summary(basket_df)
    monthly = monthly_transaction_counts(cleaned_df)
    top_items = item_frequency(basket_df).head(10)

    (OUTPUT_DIR / "eda_report.md").write_text(
        "\n".join(
            [
                "# EDA Report",
                "",
                f"- Raw rows after cleaning: {len(cleaned_df):,}",
                f"- Transactions: {len(basket_df):,}",
                f"- Unique products: {basket_df.shape[1]:,}",
                f"- Average basket size: {sizes['mean']:.2f}",
                f"- Median basket size: {sizes['50%']:.2f}",
                f"- Date range: {cleaned_df['Date'].min().date()} to {cleaned_df['Date'].max().date()}",
                f"- Busiest month: {monthly.idxmax().strftime('%Y-%m')} ({int(monthly.max()):,} transactions)",
                "",
                "## Top Products",
                "",
                top_items.to_frame("transactions").to_markdown(),
                "",
                "Figures are saved in `outputs/figures/`.",
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
                "Apriori and FP-Growth were compared at minimum support thresholds 0.01, 0.02, and 0.05 using confidence >= 0.5 and lift >= 1.2.",
                "",
                comparison.to_markdown(index=False),
                "",
                "The dashboard rule database uses a lower exploratory support threshold so the sparse groceries data still yields useful recommendations.",
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
    basket_df = create_basket_matrix(cleaned_df)

    basket_df.astype(int).to_csv(OUTPUT_DIR / "transaction_matrix.csv")
    co_occurrence_matrix(basket_df, top_n=35).to_csv(OUTPUT_DIR / "co_occurrence_matrix.csv")

    pair_stats = pairwise_statistics(basket_df)
    pair_stats.to_csv(OUTPUT_DIR / "pairwise_statistics.csv", index=False)

    clusters = basket_clusters(basket_df)
    clusters.to_csv(OUTPUT_DIR / "cluster_summary.csv", index=False)

    comparison = compare_algorithms(basket_df)
    comparison.to_csv(OUTPUT_DIR / "algorithm_comparison.csv", index=False)

    frequent_itemsets, rules = mine_rules(
        basket_df,
        algorithm="fpgrowth",
        min_support=0.001,
        min_confidence=0.05,
        min_lift=1.2,
    )
    rules = prune_redundant_rules(rules)
    serialize_itemsets(frequent_itemsets).to_csv(OUTPUT_DIR / "frequent_itemsets_fpgrowth.csv", index=False)
    serialize_itemsets(rules).to_csv(OUTPUT_DIR / "rules.csv", index=False)

    apriori_itemsets, apriori_rules = mine_rules(
        basket_df,
        algorithm="apriori",
        min_support=0.001,
        min_confidence=0.05,
        min_lift=1.2,
    )
    serialize_itemsets(apriori_itemsets).to_csv(OUTPUT_DIR / "frequent_itemsets_apriori.csv", index=False)
    serialize_itemsets(prune_redundant_rules(apriori_rules)).to_csv(OUTPUT_DIR / "rules_apriori.csv", index=False)

    save_eda_figures(cleaned_df, basket_df)
    save_network_html(serialize_itemsets(rules))
    write_reports(cleaned_df, basket_df, pair_stats, comparison, serialize_itemsets(rules), clusters)

    print(f"Generated outputs in {OUTPUT_DIR}")
    print(f"Transactions: {len(basket_df):,}; Products: {basket_df.shape[1]:,}; Rules: {len(rules):,}")


if __name__ == "__main__":
    main()
