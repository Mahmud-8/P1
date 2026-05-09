# EDA Report

- Raw rows after cleaning: 38,006
- Transactions: 14,963
- Unique products after rare-item filtering: 154
- Rare products removed with min frequency 10: 13
- Average basket size: 2.54
- Median basket size: 2.00
- Date range: 2014-01-01 to 2015-12-30
- Busiest month: 2014-05 (711 transactions)

## Top Products

| itemDescription   |   transactions |
|:------------------|---------------:|
| whole milk        |           2363 |
| other vegetables  |           1827 |
| rolls/buns        |           1646 |
| soda              |           1453 |
| yogurt            |           1285 |
| root vegetables   |           1041 |
| tropical fruit    |           1014 |
| bottled water     |            908 |
| sausage           |            903 |
| citrus fruit      |            795 |

## Seasonal Trend

Monthly transaction counts range from 539 to 711; the busiest month is 2014-05.

Figures are saved in `outputs/figures/`, including item frequency, basket size, co-occurrence heatmap, word cloud, and monthly transaction trend.