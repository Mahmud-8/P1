# 🛒 Project 2: Market Basket Analysis & Association Rule Mining
### Alamein University — Faculty of Computer Science & Engineering | AIE323

---

## Project Overview

Apply association rule mining to discover hidden purchasing patterns in transactional retail data. Implement **Apriori** and **FP-Growth** algorithms to uncover frequent itemsets and generate meaningful rules (e.g., *"customers who buy bread also buy butter"*). Deliver an interactive **Streamlit or Dash** dashboard for real-time product recommendations and rule exploration.

---

## 👥 Team Information

| Field | Details |
|---|---|
| Course | Data Mining — AIE323 |
| Faculty | Computer Science & Engineering |
| Team Size | 4–5 Students |
| Project | Project 2: Market Basket Analysis & Association Rule Mining |

---

## Milestone 1: Data Collection, Exploration, and Preprocessing

### Objectives
- Collect transactional retail data and prepare it in the correct basket format for association mining.

### Tasks

**1. Data Collection**
- Acquire transactional datasets from Kaggle (Online Retail II, Groceries Dataset, Instacart) or UCI Repository.
- Ensure the dataset contains: transaction IDs, product/item names, and quantities.

**2. Data Exploration**
- Perform EDA to understand product frequency distributions, transaction sizes, and seasonal trends.
- Identify top-selling items, rare items, and potential noise in the catalog.

**3. Data Preprocessing**
- Handle missing values, remove cancelled transactions, and clean item descriptions.
- Transform the dataset into a **binary transaction matrix** (basket format) required by association algorithms.
- Apply minimum frequency filtering to remove extremely rare items that add noise.

**4. EDA Visualizations**
- Create item frequency bar charts, transaction size histograms, and word clouds of product names.
- Visualize product co-occurrence matrices as heatmaps.

### Deliverables
- **EDA Report:** Summary of data distribution, quality issues, and preprocessing steps.
- **Transaction Matrix:** A clean binary basket matrix ready for association rule mining.
- **EDA Notebook:** Jupyter notebook with all visualizations.

---

## Milestone 2: Advanced Analysis and Pattern Discovery

### Objectives
- Perform deep analysis on co-purchase patterns and identify preliminary associations before formal mining.

### Tasks

**5. Co-occurrence Analysis**
- Build and visualize product co-occurrence matrices to preview strong relationships.
- Identify cross-category purchasing patterns (e.g., produce with dairy).

**6. Statistical Measures**
- Compute pairwise lift, chi-squared, and Jaccard similarity for top product pairs.
- Analyze which categories drive the most cross-selling opportunities.

**7. Segmentation by Basket**
- Group customers by basket composition using simple clustering before rule mining.

**8. Visualization**
- Develop network graphs showing product relationships (nodes = items, edges = co-purchases).
- Build interactive dashboards to explore product category interactions.

### Deliverables
- **Co-occurrence Analysis Report:** Statistical analysis of item relationships and preliminary findings.
- **Network Graph:** An interactive product relationship network visualization.

---

## Milestone 3: Association Rule Mining — Apriori & FP-Growth

### Objectives
- Implement Apriori and FP-Growth algorithms, mine frequent itemsets, and generate actionable rules.

### Tasks

**9. Algorithm Implementation**
- Implement **Apriori** using the `mlxtend` library. Experiment with different minimum support thresholds (0.01, 0.02, 0.05).
- Implement **FP-Growth** for efficient mining on larger datasets. Compare performance with Apriori.

**10. Rule Generation**
- Generate association rules with metrics: **Support**, **Confidence**, and **Lift**.
- Filter rules by minimum lift > 1.2 and confidence > 0.5 for actionable results.
- Optionally compute Conviction and Leverage as additional rule strength measures.

**11. Rule Analysis**
- Rank rules by lift to identify the strongest associations.
- Group rules by antecedent category (e.g., all rules where bread is an antecedent).
- Detect redundant rules and apply pruning strategies.

**12. Evaluation**
- Compare Apriori vs FP-Growth on runtime performance and rule quality.
- Validate discovered rules with domain knowledge or manual inspection.

### Deliverables
- **Mining Report:** Full analysis of frequent itemsets and rules, algorithm comparison, and business interpretations.
- **Rule Database:** A curated CSV/Excel file of the top rules with all metrics.
- **Algorithm Code:** Python notebooks for both Apriori and FP-Growth implementations.

---

## Milestone 4: Recommendation Engine & Dashboard Deployment

### Objectives
- Build a rule-based product recommendation engine and deploy it as an interactive Streamlit or Dash application.

### Tasks

**13. Recommendation Engine**
- Build a function: given a set of items in a cart → return the top-N recommended items ranked by lift.
- Handle multi-item antecedents and edge cases (no rules found, cold-start problem).

**14. Streamlit / Dash App — Required Features**

| Feature | Description |
|---|---|
| ✅ Rule Explorer | Searchable, filterable table of all mined rules |
| ✅ Product Recommender | User selects basket items → gets top recommendations |
| ✅ Network Graph Tab | Interactive product association clusters (Plotly or Pyvis) |
| ✅ Threshold Sliders | Dynamic sliders for support, confidence, and lift |

**15. Deployment**
- Deploy locally and optionally on Streamlit Cloud, Render, or a similar platform.
- Provide a `README.md` with setup instructions.

### Deliverables
- **Deployed App:** A live recommendation and rule exploration app built with Streamlit or Dash.

---

## Milestone 5: Final Documentation and Presentation

### Deliverables
- **Final Project Report:** End-to-end documentation covering methodology, rules discovered, business impact, and recommendations.

---

## 📋 Milestones Summary

| Milestone | Key Deliverables |
|---|---|
| 1. Data Collection & Preprocessing | EDA Report, Transaction Matrix, EDA Notebook |
| 2. Co-occurrence & Pattern Analysis | Co-occurrence Report, Network Graph Visualization |
| 3. Apriori & FP-Growth Mining | Mining Report, Rule Database, Algorithm Code |
| 4. Recommendation Engine & Dashboard | Deployed Streamlit/Dash App |
| 5. Final Documentation & Presentation | Final Project Report, Final Presentation |

---

## ✅ Deliverables Checklist

- [ ] EDA Report + EDA Notebook (Jupyter)
- [ ] Cleaned Transaction Matrix (binary basket format)
- [ ] Co-occurrence Analysis Report + Network Graph
- [ ] Mining Report (Apriori & FP-Growth comparison)
- [ ] Rule Database (CSV/Excel with all metrics)
- [ ] Algorithm Code (Python notebooks)
- [ ] Deployed Streamlit/Dash App (all 4 required features)
- [ ] `README.md` with setup instructions
- [ ] Final Project Report
- [ ] GitHub Repository (clean, commented, reproducible)

---

## 🛠️ Suggested Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.9+ |
| Data / EDA | Pandas, NumPy, Matplotlib, Seaborn, Plotly |
| Association Mining | `mlxtend` (Apriori, FP-Growth) |
| Network Graphs | NetworkX, Pyvis |
| Dashboard | Streamlit or Dash |
| Deployment | Streamlit Cloud / Render / Heroku |
| Version Control | GitHub |

---

*Alamein University — Faculty of Computer Science & Engineering | Data Mining AIE323*
