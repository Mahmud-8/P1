# Project Code Guide

This file explains the main files in the Market Basket Analysis project, what each part of the code does, and which tools/libraries are used.

## Project Goal

The project analyzes grocery transaction data to find products that are often bought together. It uses association rule mining to generate rules such as:

```text
whole milk, yogurt -> sausage
```

The project also includes a Streamlit dashboard where users can explore rules, view network relationships, and get product recommendations.

## Main Workflow

The project follows this pipeline:

```text
Raw grocery data
-> cleaning and preprocessing
-> transaction basket matrix
-> EDA and co-occurrence analysis
-> Apriori and FP-Growth mining
-> association rules
-> recommendation engine
-> Streamlit dashboard
-> final reports and output files
```

## Folder Structure

```text
market-basket-project/
  app/
    app.py
    requirements.txt
  data/
    groceries.csv
  notebooks/
    analysis.ipynb
  outputs/
    figures/
    *.csv
    *.md
    product_network.html
  scripts/
    run_analysis.py
  src/
    preprocessing.py
    models.py
    recommend.py
  FINAL_PROJECT_REPORT.md
  Market_Basket_Analysis_Report.docx
  README.md
  requirements.txt
```

## Important Source Files

### `data/groceries.csv`

This is the raw dataset. It contains grocery purchases with columns such as:

- `Member_number`
- `Date`
- `itemDescription`

The code combines `Member_number` and `Date` to create a transaction ID. Each transaction represents the items bought by one member on one date.

### `src/preprocessing.py`

This file contains the preprocessing and EDA helper functions.

Important functions:

- `clean_groceries_data(df)`
  - Removes missing values.
  - Converts dates to datetime format.
  - Converts item names to lowercase.
  - Removes duplicate item rows inside the same transaction.
  - Creates the `Transaction` column.

- `create_transactions(df)`
  - Groups products by transaction.
  - Produces a list of baskets.

- `create_basket_matrix(df, min_item_frequency=1, min_support=None)`
  - Converts transaction data into a binary basket matrix.
  - Rows are transactions.
  - Columns are products.
  - Values are `True` or `False`, meaning whether the product exists in the transaction.

- `item_frequency(basket_df)`
  - Counts how often each product appears.

- `transaction_size_summary(basket_df)`
  - Summarizes basket sizes.

- `co_occurrence_matrix(basket_df)`
  - Counts how often pairs of products appear together.

- `monthly_transaction_counts(cleaned_df)`
  - Counts transactions per month.

### `src/models.py`

This file contains the association rule mining logic.

Important functions:

- `_mine_frequent_itemsets(basket_df, algorithm, min_support)`
  - Uses Apriori or FP-Growth to find frequent itemsets.
  - Uses `mlxtend.frequent_patterns.apriori`.
  - Uses `mlxtend.frequent_patterns.fpgrowth`.

- `_rules_from_itemsets(frequent_itemsets, min_confidence, min_lift)`
  - Converts frequent itemsets into association rules.
  - Filters rules by confidence and lift.
  - Adds antecedent and consequent lengths.

- `mine_rules(...)`
  - Main function for mining frequent itemsets and rules.

- `run_apriori(...)`
  - Runs Apriori and returns rules.

- `run_fpgrowth(...)`
  - Runs FP-Growth and returns rules.

- `compare_algorithms(...)`
  - Compares Apriori and FP-Growth using different support thresholds.
  - Saves runtime, frequent itemset count, rule count, average lift, and average confidence.

- `prune_redundant_rules(rules)`
  - Removes duplicated rules with the same antecedents and consequents.

- `serialize_itemsets(df)`
  - Converts itemsets from Python `frozenset` format into readable text for CSV files.

### `src/recommend.py`

This file contains the recommendation engine.

Important functions:

- `normalize_item(value)`
  - Cleans item names by trimming spaces and converting to lowercase.

- `parse_itemset(value)`
  - Converts stored itemsets from text into Python sets.
  - Handles strings, sets, lists, tuples, and empty values.

- `format_itemset(value)`
  - Converts itemsets into readable display text.

- `recommend_items(cart_items, rules, top_n, min_confidence, min_lift)`
  - Takes selected basket items from the user.
  - Finds matching association rules.
  - Supports multi-item antecedents.
  - Prioritizes full antecedent matches over partial matches.
  - Removes items already in the basket.
  - Sorts recommendations by match quality, lift, confidence, and support.

Example:

```text
Input basket: whole milk, yogurt
Matched rule: whole milk, yogurt -> sausage
Recommended item: sausage
```

### `scripts/run_analysis.py`

This is the main analysis runner. Run this file to regenerate all outputs.

Command:

```powershell
python scripts\run_analysis.py
```

It performs:

- Data loading.
- Data cleaning.
- Basket matrix creation.
- EDA figure generation.
- Co-occurrence analysis.
- Pairwise statistics.
- Basket clustering.
- Apriori and FP-Growth comparison.
- Rule mining.
- Rule pruning.
- Network graph generation.
- Markdown report generation.
- CSV output generation.

Important thresholds currently used:

```text
MIN_ITEM_FREQUENCY = 10
MIN_LIFT = 1.2
ACTIONABLE_CONFIDENCE = 0.05
DASHBOARD_CONFIDENCE = 0.05
DASHBOARD_SUPPORT = 0.001
```

### `app/app.py`

This is the Streamlit dashboard.

Command:

```powershell
streamlit run app\app.py
```

Main dashboard sections:

- **Rule Explorer**
  - Shows mined association rules.
  - Allows filtering by support, confidence, lift, search text, and sort column.

- **Product Recommender**
  - Lets the user select basket items.
  - Returns top product recommendations based on matching rules.

- **Network Graph**
  - Shows product relationships as an interactive graph.
  - Uses Plotly.

- **Analysis**
  - Shows Apriori vs FP-Growth comparison.
  - Shows actionable rules.
  - Shows rules by antecedent category.
  - Shows category pair opportunities.
  - Shows pairwise statistics.

## Output Files

### `outputs/transaction_matrix.csv`

The binary transaction matrix used by Apriori and FP-Growth.

- Rows: transactions.
- Columns: products.
- Values: `0` or `1`.

### `outputs/co_occurrence_matrix.csv`

Shows how many times product pairs appear together in the same transaction.

### `outputs/pairwise_statistics.csv`

Contains pair-level metrics such as:

- Co-occurrences.
- Lift.
- Jaccard similarity.
- Chi-squared score.
- Product categories.

### `outputs/category_pair_statistics.csv`

Summarizes product-pair relationships by category, such as dairy to bakery or beverages to snacks.

### `outputs/cluster_summary.csv`

Contains simple basket segmentation results. It groups similar baskets based on product composition.

### `outputs/algorithm_comparison.csv`

Compares Apriori and FP-Growth.

Columns include:

- `algorithm`
- `min_support`
- `min_confidence`
- `min_lift`
- `runtime_seconds`
- `frequent_itemsets`
- `rules`
- `avg_lift`
- `avg_confidence`

### `outputs/frequent_itemsets_apriori.csv`

Frequent itemsets found by Apriori.

### `outputs/frequent_itemsets_fpgrowth.csv`

Frequent itemsets found by FP-Growth.

### `outputs/rules.csv`

Main rule database used by the dashboard.

Important columns:

- `antecedents`
- `consequents`
- `support`
- `confidence`
- `lift`
- `leverage`
- `conviction`
- `algorithm`

### `outputs/rules_actionable.csv`

Actionable rules generated using the selected actionable threshold.

Currently the project uses:

```text
confidence >= 0.05
lift >= 1.20
support >= 0.001
```

This threshold is used because the grocery dataset is sparse. A stricter confidence threshold of `0.50` produced no rules.

### `outputs/antecedent_rule_summary.csv`

Groups rules by antecedent product category.

### `outputs/eda_report.md`

Markdown report for exploratory data analysis.

### `outputs/co_occurrence_report.md`

Markdown report for co-occurrence and pairwise analysis.

### `outputs/mining_report.md`

Markdown report for Apriori, FP-Growth, rule mining, and algorithm comparison.

### `outputs/product_network.html`

Interactive HTML network visualization of product relationships.

### `outputs/figures/`

Contains generated EDA charts:

- `top_items.png`
- `transaction_size_histogram.png`
- `product_wordcloud.png`
- `monthly_transaction_trend.png`
- `co_occurrence_heatmap.png`

## Reports and Documentation

### `FINAL_PROJECT_REPORT.md`

Main final report in Markdown format.

### `Market_Basket_Analysis_Report.docx`

Word document version of the final report.

### `README.md`

Short project overview and setup instructions.

### `PROJECT_CODE_GUIDE.md`

This file. It explains the project code and files.

## Libraries Used

### Data Processing

- `pandas`
  - Reading CSV files.
  - Cleaning data.
  - Grouping transactions.
  - Creating output tables.

- `numpy`
  - Numerical support through the data science stack.

### Association Rule Mining

- `mlxtend`
  - Apriori.
  - FP-Growth.
  - Association rule generation.

### Visualization

- `matplotlib`
  - Static charts.

- `seaborn`
  - Heatmaps and statistical plots.

- `plotly`
  - Interactive network graph in the dashboard.

- `networkx`
  - Product network structure.

- `wordcloud`
  - Product word cloud visualization.

### Machine Learning and Statistics

- `scikit-learn`
  - Basket clustering.

### Dashboard

- `streamlit`
  - Interactive web dashboard.

### Reporting

- `tabulate`
  - Markdown table formatting.

## Key Metrics

### Support

Support measures how often an itemset appears in all transactions.

```text
support(A -> B) = transactions containing A and B / total transactions
```

### Confidence

Confidence measures how often the consequent appears when the antecedent appears.

```text
confidence(A -> B) = support(A and B) / support(A)
```

### Lift

Lift measures whether the relationship is stronger than random chance.

```text
lift(A -> B) = confidence(A -> B) / support(B)
```

Interpretation:

- `lift > 1`: positive association.
- `lift = 1`: independent relationship.
- `lift < 1`: negative association.

### Leverage

Leverage measures the difference between observed co-occurrence and expected co-occurrence.

### Conviction

Conviction measures rule direction strength and dependency.

## Why Confidence 0.05 Is Used

The dataset is sparse, meaning most baskets contain only a small number of items and product combinations do not repeat very often.

When using:

```text
confidence >= 0.50
lift >= 1.20
```

the project found no rules. This is why the dashboard uses:

```text
confidence >= 0.05
lift >= 1.20
```

This keeps the dashboard useful while still filtering for positive product associations.

## How to Run the Project

From the project folder:

```powershell
cd "D:\Semester 6\(AIE323) Data Mining (Spring 2026)\P1\market-basket-project"
python -m pip install -r requirements.txt
python scripts\run_analysis.py
streamlit run app\app.py
```

## What to Say When Explaining the Project

You can describe the project like this:

> This project builds a complete market basket analysis pipeline. It cleans grocery transaction data, converts it into a binary basket matrix, explores item frequencies and co-occurrences, mines frequent itemsets using Apriori and FP-Growth, generates association rules using support, confidence, and lift, and serves the results through a Streamlit dashboard with rule exploration, recommendations, and network visualization.

