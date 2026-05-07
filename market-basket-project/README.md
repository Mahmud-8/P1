# 🛒 Market Basket Analysis & Recommendation System

**Course:** Data Mining (AIE323)
**Project Type:** Association Rule Mining
**Team:** [Add Names]

---

# 📌 Project Overview

This project aims to analyze transactional retail data to uncover hidden purchasing patterns using **Association Rule Mining** techniques such as **Apriori** and **FP-Growth**.

The system identifies relationships between products (e.g., *customers who buy milk also buy bread*) and builds a **recommendation engine** to suggest products based on user input.

---

# 🎯 Objectives

* Discover frequent itemsets from transactional data
* Generate meaningful association rules
* Compare Apriori vs FP-Growth performance
* Build a product recommendation system
* Develop an interactive dashboard using Streamlit

---

# 📂 Dataset

We will use the **Groceries Dataset** (or Online Retail dataset).

### Dataset Features:

* Transaction ID
* Product names
* Purchase records

---

# 🧹 Data Preprocessing

Steps:

* Remove missing values
* Remove duplicate transactions
* Clean product names
* Convert dataset into **basket format (one-hot encoding)**
* Filter rare items using minimum support threshold

---

# 📊 Exploratory Data Analysis (EDA)

We will perform:

* Top-selling products visualization
* Basket size distribution
* Item frequency plots
* Product co-occurrence heatmap

---

# ⚙️ Methodology

## 🔹 1. Apriori Algorithm

* Generate frequent itemsets
* Use minimum support threshold
* Extract association rules

## 🔹 2. FP-Growth Algorithm

* Faster alternative to Apriori
* Efficient for large datasets

---

# 📏 Evaluation Metrics

We evaluate rules using:

* **Support** → Frequency of itemset
* **Confidence** → Rule reliability
* **Lift** → Strength of association

Rules will be filtered using:

* Confidence > 0.5
* Lift > 1.2

---

# 🤖 Recommendation System

We build a function that:

* Takes selected products as input
* Returns top-N recommended products
* Handles multiple-item input
* Handles edge cases (no rules found)

---

# 🌐 Streamlit Dashboard (Main Bonus Part 🚀)

## Features:

### 1. Rule Explorer

* Interactive table of association rules
* Filter by support, confidence, lift

### 2. Product Recommendation Tool

* User selects products
* System suggests related items

### 3. Network Graph Visualization

* Nodes = products
* Edges = associations

### 4. Dynamic Threshold Controls

* Sliders to adjust:

  * Support
  * Confidence
  * Lift

---

# 💡 Bonus Enhancements (To Get Extra Marks ⭐)

* Compare Apriori vs FP-Growth runtime
* Add **Conviction & Leverage metrics**
* Build **interactive network graph (Plotly / Pyvis)**
* Optimize performance for large datasets
* Add user-friendly UI design
* Allow CSV upload for real-time recommendations

---

# 📦 Deliverables

* ✔ Jupyter Notebook (clean + documented)
* ✔ Streamlit App (interactive dashboard)
* ✔ GitHub Repository
* ✔ Final Report

---

# ⚠️ Challenges

* Handling large datasets efficiently
* Choosing optimal support threshold
* Reducing redundant rules
* Improving recommendation accuracy

---

# 🔮 Future Work

* Integrate deep learning recommendation systems
* Real-time data streaming
* Personalized recommendations per user

---

# Structure

market-basket-project/
│
├── data/
│   └── groceries.csv
├── notebooks/
│   └── analysis.ipynb
├── src/
│   ├── preprocessing.py
│   ├── models.py
│   └── recommend.py
├── app/
│   └── app.py
├── outputs/
│   ├── rules.csv
│   └── figures/
├── README.md
├── requirements.txt
└── report.pdf

# 🧾 Conclusion

This project demonstrates how data mining techniques can uncover valuable insights from transactional data and improve business decision-making through intelligent recommendations.

---

# Reproducible Setup

From the `market-basket-project` folder:

```bash
python -m pip install -r requirements.txt
python scripts/run_analysis.py
streamlit run app/app.py
```

The analysis runner regenerates the main required deliverables:

* `outputs/transaction_matrix.csv` - cleaned binary basket matrix
* `outputs/co_occurrence_matrix.csv` - item co-occurrence matrix
* `outputs/pairwise_statistics.csv` - pairwise lift, chi-squared, and Jaccard
* `outputs/cluster_summary.csv` - simple basket composition clusters
* `outputs/algorithm_comparison.csv` - Apriori vs FP-Growth runtime comparison
* `outputs/rules.csv` - curated rule database for the dashboard
* `outputs/frequent_itemsets_apriori.csv` and `outputs/frequent_itemsets_fpgrowth.csv`
* `outputs/eda_report.md`, `outputs/co_occurrence_report.md`, and `outputs/mining_report.md`
* `outputs/product_network.html` and figures in `outputs/figures/`

# Dashboard Coverage

The Streamlit app includes the four required features from the project brief:

* Rule Explorer with searchable and filterable rules
* Product Recommender with multi-item basket input and top-N ranking
* Interactive Network Graph tab
* Dynamic support, confidence, and lift sliders
