from __future__ import annotations

import sys
from math import cos, pi, sin
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.recommend import format_itemset, parse_itemset, recommend_items


RULES_PATH = ROOT / "outputs" / "rules.csv"
COMPARISON_PATH = ROOT / "outputs" / "algorithm_comparison.csv"
PAIRWISE_PATH = ROOT / "outputs" / "pairwise_statistics.csv"


st.set_page_config(page_title="Market Basket Analysis", layout="wide")


@st.cache_data
def load_rules() -> pd.DataFrame:
    if not RULES_PATH.exists():
        return pd.DataFrame()

    rules = pd.read_csv(RULES_PATH)
    if rules.empty:
        return rules

    rules["antecedents_display"] = rules["antecedents"].apply(format_itemset)
    rules["consequents_display"] = rules["consequents"].apply(format_itemset)
    rules["rule"] = rules["antecedents_display"] + " -> " + rules["consequents_display"]
    return rules


@st.cache_data
def load_optional_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def available_products(rules: pd.DataFrame) -> list[str]:
    products: set[str] = set()
    for column in ("antecedents", "consequents"):
        for value in rules[column].dropna():
            products.update(parse_itemset(value))
    return sorted(products)


def filter_rules(
    rules: pd.DataFrame,
    min_support: float,
    min_confidence: float,
    min_lift: float,
    search: str,
    sort_by: str,
) -> pd.DataFrame:
    filtered = rules[
        (rules["support"] >= min_support)
        & (rules["confidence"] >= min_confidence)
        & (rules["lift"] >= min_lift)
    ].copy()

    if search.strip():
        query = search.strip().lower()
        filtered = filtered[
            filtered["antecedents_display"].str.contains(query, case=False, na=False)
            | filtered["consequents_display"].str.contains(query, case=False, na=False)
        ]

    return filtered.sort_values(sort_by, ascending=False)


def build_network_figure(rules: pd.DataFrame, max_edges: int = 75) -> go.Figure:
    network_rules = rules.sort_values(["lift", "confidence"], ascending=False).head(max_edges)
    edges = []
    nodes: set[str] = set()
    degrees: dict[str, int] = {}

    for _, row in network_rules.iterrows():
        antecedents = parse_itemset(row["antecedents"])
        consequents = parse_itemset(row["consequents"])
        for antecedent in antecedents:
            for consequent in consequents:
                if antecedent != consequent:
                    edges.append((antecedent, consequent, float(row["lift"])))
                    nodes.update([antecedent, consequent])
                    degrees[antecedent] = degrees.get(antecedent, 0) + 1
                    degrees[consequent] = degrees.get(consequent, 0) + 1

    figure = go.Figure()
    if not edges:
        figure.update_layout(
            height=620,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[
                dict(
                    text="No network edges match the current filters.",
                    showarrow=False,
                    x=0.5,
                    y=0.5,
                )
            ],
        )
        return figure

    ordered_nodes = sorted(nodes, key=lambda node: (-degrees.get(node, 0), node))
    positions = {
        node: (
            cos(2 * pi * index / len(ordered_nodes)),
            sin(2 * pi * index / len(ordered_nodes)),
        )
        for index, node in enumerate(ordered_nodes)
    }

    edge_x, edge_y = [], []
    for source, target, _weight in edges:
        edge_x.extend([positions[source][0], positions[target][0], None])
        edge_y.extend([positions[source][1], positions[target][1], None])

    node_x = [positions[node][0] for node in ordered_nodes]
    node_y = [positions[node][1] for node in ordered_nodes]
    node_degree = [degrees.get(node, 0) for node in ordered_nodes]

    figure.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=1.2, color="#94a3b8"),
            hoverinfo="skip",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=ordered_nodes,
            textposition="top center",
            hovertemplate="%{text}<extra></extra>",
            marker=dict(
                size=[12 + degree * 2 for degree in node_degree],
                color=node_degree,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Links"),
                line=dict(width=1, color="#0f172a"),
            ),
        )
    )
    figure.update_layout(
        height=620,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
    )
    return figure


rules = load_rules()

st.title("Market Basket Analysis")
st.caption("Association rule explorer, product recommender, and network visualization")

if rules.empty:
    st.error("No rules were found. Run `python scripts/run_analysis.py` from the project root first.")
    st.stop()

max_support = float(max(rules["support"].max(), 0.001))
default_support = min(0.001, max_support)

with st.sidebar:
    st.header("Filters")
    min_support = st.slider("Minimum Support", 0.0, max_support, default_support, 0.001, format="%.3f")
    min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.05, 0.01, format="%.2f")
    min_lift = st.slider("Minimum Lift", 0.0, max(3.0, float(rules["lift"].max())), 1.2, 0.1, format="%.1f")
    search = st.text_input("Search Product")
    sort_by = st.selectbox("Sort Rules By", ["lift", "confidence", "support"])

filtered_rules = filter_rules(rules, min_support, min_confidence, min_lift, search, sort_by)

metric_cols = st.columns(4)
metric_cols[0].metric("Rules", f"{len(filtered_rules):,}")
metric_cols[1].metric("Products", f"{len(available_products(rules)):,}")
metric_cols[2].metric("Max Lift", f"{rules['lift'].max():.2f}")
metric_cols[3].metric("Avg Confidence", f"{filtered_rules['confidence'].mean():.2f}" if not filtered_rules.empty else "0.00")

tab_rules, tab_recommend, tab_network, tab_analysis = st.tabs(
    ["Rule Explorer", "Product Recommender", "Network Graph", "Analysis"]
)

with tab_rules:
    display_columns = [
        "antecedents_display",
        "consequents_display",
        "support",
        "confidence",
        "lift",
        "leverage",
        "conviction",
        "algorithm",
    ]
    existing_columns = [column for column in display_columns if column in filtered_rules.columns]
    table = filtered_rules[existing_columns].rename(
        columns={
            "antecedents_display": "antecedents",
            "consequents_display": "consequents",
        }
    )
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button(
        "Download filtered rules",
        data=table.to_csv(index=False).encode("utf-8"),
        file_name="filtered_rules.csv",
        mime="text/csv",
    )

with tab_recommend:
    products = available_products(rules)
    selected_items = st.multiselect("Basket Items", products)
    top_n = st.slider("Number of Recommendations", 1, 15, 5)

    recommendations = recommend_items(
        selected_items,
        filtered_rules,
        top_n=top_n,
        min_confidence=min_confidence,
        min_lift=min_lift,
    )

    if not selected_items:
        st.info("Select one or more basket items to see recommendations.")
    elif recommendations.empty:
        st.warning("No recommendations matched the selected basket and filters.")
    else:
        st.dataframe(
            recommendations[
                ["item", "score", "lift", "confidence", "support", "match_type", "matched_rule"]
            ],
            use_container_width=True,
            hide_index=True,
        )

with tab_network:
    max_edges = st.slider("Network Edges", 10, 150, 75, 5)
    st.plotly_chart(build_network_figure(filtered_rules, max_edges=max_edges), use_container_width=True)

with tab_analysis:
    comparison = load_optional_csv(COMPARISON_PATH)
    pairwise = load_optional_csv(PAIRWISE_PATH)

    if not comparison.empty:
        st.subheader("Apriori vs FP-Growth")
        st.dataframe(comparison, use_container_width=True, hide_index=True)

    if not pairwise.empty:
        st.subheader("Top Pairwise Statistics")
        st.dataframe(
            pairwise.head(20)[
                ["item_a", "item_b", "co_occurrences", "lift", "jaccard", "chi_squared"]
            ],
            use_container_width=True,
            hide_index=True,
        )
