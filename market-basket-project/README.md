# Market Basket Analysis and Recommendation System

Course: Data Mining (AIE323)

This project analyzes grocery transactions with association rule mining. It prepares a binary basket matrix, compares Apriori and FP-Growth, computes co-purchase statistics, builds a rule-based recommender, and serves the results in a Streamlit dashboard.

## Requirements Covered

- Data cleaning, transaction construction, rare-item filtering, and binary basket matrix output
- EDA figures: top items, basket-size histogram, product word cloud, co-occurrence heatmap, and monthly transaction trend
- Pairwise co-occurrence statistics: lift, chi-squared, and Jaccard similarity
- Basket segmentation with simple clustering
- Apriori and FP-Growth comparison at support thresholds 0.01, 0.02, and 0.05
- Association rules with support, confidence, lift, leverage, and conviction
- Rule pruning and grouping by antecedent category
- Product recommender that returns top-N items ranked by lift
- Streamlit app with Rule Explorer, Product Recommender, Network Graph, and threshold sliders

## Project Structure

```text
market-basket-project/
  app/app.py
  data/groceries.csv
  notebooks/analysis.ipynb
  outputs/
  scripts/run_analysis.py
  src/preprocessing.py
  src/models.py
  src/recommend.py
  requirements.txt
```

## Setup

From the `market-basket-project` folder:

```bash
python -m pip install -r requirements.txt
python scripts/run_analysis.py
streamlit run app/app.py
```

For Streamlit Cloud, use `market-basket-project/app/app.py` as the main file path. The repository-root `requirements.txt` is intentionally minimal for deployment and installs only the packages needed by the dashboard.

## Generated Deliverables

The analysis runner regenerates:

- `FINAL_PROJECT_REPORT.md`
- `outputs/transaction_matrix.csv`
- `outputs/co_occurrence_matrix.csv`
- `outputs/pairwise_statistics.csv`
- `outputs/category_pair_statistics.csv`
- `outputs/cluster_summary.csv`
- `outputs/algorithm_comparison.csv`
- `outputs/rules.csv`
- `outputs/rules_actionable.csv`
- `outputs/frequent_itemsets_apriori.csv`
- `outputs/frequent_itemsets_fpgrowth.csv`
- `outputs/eda_report.md`
- `outputs/co_occurrence_report.md`
- `outputs/mining_report.md`
- `outputs/product_network.html`
- figures in `outputs/figures/`

Note: the strict project threshold `confidence >= 0.50` and `lift >= 1.20` produces no actionable rules on this sparse Groceries transaction definition. The dashboard keeps an exploratory rule database at `confidence >= 0.05` and `lift >= 1.20`, while the strict audit output is saved separately in `outputs/rules_actionable.csv`.
