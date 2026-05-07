# Co-occurrence Analysis Report

The table below ranks top product pairs by lift, with chi-squared and Jaccard similarity included for statistical context.

| item_a            | item_b            |   co_occurrences |   support_a |   support_b |   pair_support |    lift |   jaccard |   chi_squared |
|:------------------|:------------------|-----------------:|------------:|------------:|---------------:|--------:|----------:|--------------:|
| pastry            | napkins           |               26 |   0.0517276 |   0.0221212 |     0.00173762 | 1.51853 | 0.0240964 |      4.96453  |
| sausage           | curd              |               44 |   0.0603489 |   0.0336831 |     0.00294059 | 1.44662 | 0.0322817 |      6.6816   |
| canned beer       | white bread       |               23 |   0.0469157 |   0.0239925 |     0.00153712 | 1.36557 | 0.022158  |      2.41979  |
| canned beer       | brown bread       |               36 |   0.0469157 |   0.0376261 |     0.00240593 | 1.36294 | 0.0292921 |      3.79327  |
| beef              | frozen vegetables |               19 |   0.0339504 |   0.0280024 |     0.0012698  | 1.33566 | 0.0209251 |      1.7068   |
| frankfurter       | margarine         |               24 |   0.0377598 |   0.0322128 |     0.00160396 | 1.31866 | 0.0234604 |      1.98464  |
| frozen vegetables | cream cheese      |               13 |   0.0280024 |   0.0236584 |     0.00086881 | 1.31143 | 0.0171053 |      1.01309  |
| beef              | margarine         |               21 |   0.0339504 |   0.0322128 |     0.00140346 | 1.2833  | 0.0216718 |      1.40474  |
| newspapers        | beef              |               25 |   0.0388959 |   0.0339504 |     0.00167079 | 1.26524 | 0.0234742 |      1.49716  |
| curd              | dessert           |               15 |   0.0336831 |   0.0235915 |     0.00100247 | 1.26155 | 0.0178147 |      0.862079 |
| coffee            | hamburger meat    |               13 |   0.0316113 |   0.0218539 |     0.00086881 | 1.25763 | 0.0165184 |      0.724323 |
| butter            | margarine         |               21 |   0.0352202 |   0.0322128 |     0.00140346 | 1.23703 | 0.0212551 |      1.0215   |
| frankfurter       | coffee            |               22 |   0.0377598 |   0.0316113 |     0.00147029 | 1.23178 | 0.0216535 |      1.02966  |
| sausage           | frozen vegetables |               31 |   0.0603489 |   0.0280024 |     0.00207178 | 1.22597 | 0.0240124 |      1.41364  |
| sausage           | bottled beer      |               50 |   0.0603489 |   0.0453118 |     0.00334158 | 1.222   | 0.0326584 |      2.2479   |

## Basket Segments

|   cluster |   transactions |   avg_basket_size | top_items                                                        |
|----------:|---------------:|------------------:|:-----------------------------------------------------------------|
|         0 |           8637 |              2.37 | yogurt, root vegetables, tropical fruit, bottled water, sausage  |
|         1 |           3382 |              2.71 | whole milk, other vegetables, yogurt, tropical fruit, sausage    |
|         2 |           1508 |              2.83 | rolls/buns, whole milk, other vegetables, yogurt, tropical fruit |
|         3 |           1436 |              2.88 | soda, whole milk, other vegetables, rolls/buns, yogurt           |