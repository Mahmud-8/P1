# Co-occurrence Analysis Report

The table below ranks top product pairs by lift, with chi-squared and Jaccard similarity included for statistical context.

| item_a            | item_b            | category_a       | category_b       | category_pair                | cross_category   |   co_occurrences |   support_a |   support_b |   pair_support |    lift |   jaccard |   chi_squared |
|:------------------|:------------------|:-----------------|:-----------------|:-----------------------------|:-----------------|-----------------:|------------:|------------:|---------------:|--------:|----------:|--------------:|
| pastry            | napkins           | bakery           | household        | bakery + household           | True             |               26 |   0.0517276 |   0.0221212 |     0.00173762 | 1.51853 | 0.0240964 |      4.96453  |
| sausage           | curd              | meat and seafood | dairy            | dairy + meat and seafood     | True             |               44 |   0.0603489 |   0.0336831 |     0.00294059 | 1.44662 | 0.0322817 |      6.6816   |
| canned beer       | white bread       | beverages        | bakery           | bakery + beverages           | True             |               23 |   0.0469157 |   0.0239925 |     0.00153712 | 1.36557 | 0.022158  |      2.41979  |
| canned beer       | brown bread       | beverages        | bakery           | bakery + beverages           | True             |               36 |   0.0469157 |   0.0376261 |     0.00240593 | 1.36294 | 0.0292921 |      3.79327  |
| beef              | frozen vegetables | meat and seafood | produce          | meat and seafood + produce   | True             |               19 |   0.0339504 |   0.0280024 |     0.0012698  | 1.33566 | 0.0209251 |      1.7068   |
| frankfurter       | margarine         | other            | other            | other                        | False            |               24 |   0.0377598 |   0.0322128 |     0.00160396 | 1.31866 | 0.0234604 |      1.98464  |
| frozen vegetables | cream cheese      | produce          | dairy            | dairy + produce              | True             |               13 |   0.0280024 |   0.0236584 |     0.00086881 | 1.31143 | 0.0171053 |      1.01309  |
| beef              | margarine         | meat and seafood | other            | meat and seafood + other     | True             |               21 |   0.0339504 |   0.0322128 |     0.00140346 | 1.2833  | 0.0216718 |      1.40474  |
| newspapers        | beef              | other            | meat and seafood | meat and seafood + other     | True             |               25 |   0.0388959 |   0.0339504 |     0.00167079 | 1.26524 | 0.0234742 |      1.49716  |
| curd              | dessert           | dairy            | dairy            | dairy                        | False            |               15 |   0.0336831 |   0.0235915 |     0.00100247 | 1.26155 | 0.0178147 |      0.862079 |
| coffee            | hamburger meat    | beverages        | meat and seafood | beverages + meat and seafood | True             |               13 |   0.0316113 |   0.0218539 |     0.00086881 | 1.25763 | 0.0165184 |      0.724323 |
| butter            | margarine         | dairy            | other            | dairy + other                | True             |               21 |   0.0352202 |   0.0322128 |     0.00140346 | 1.23703 | 0.0212551 |      1.0215   |
| frankfurter       | coffee            | other            | beverages        | beverages + other            | True             |               22 |   0.0377598 |   0.0316113 |     0.00147029 | 1.23178 | 0.0216535 |      1.02966  |
| sausage           | frozen vegetables | meat and seafood | produce          | meat and seafood + produce   | True             |               31 |   0.0603489 |   0.0280024 |     0.00207178 | 1.22597 | 0.0240124 |      1.41364  |
| sausage           | bottled beer      | meat and seafood | beverages        | beverages + meat and seafood | True             |               50 |   0.0603489 |   0.0453118 |     0.00334158 | 1.222   | 0.0326584 |      2.2479   |

## Cross-category Opportunities

| category_pair                 | cross_category   |   pairs |   total_co_occurrences |   avg_lift |   max_lift |   avg_jaccard |   max_chi_squared |
|:------------------------------|:-----------------|--------:|-----------------------:|-----------:|-----------:|--------------:|------------------:|
| meat and seafood + other      | True             |      20 |                    347 |      0.909 |      1.283 |        0.016  |             5.106 |
| bakery + meat and seafood     | True             |      20 |                    509 |      0.885 |      1.203 |        0.0175 |            21.156 |
| beverages + snacks and sweets | True             |       5 |                     86 |      0.884 |      0.98  |        0.0144 |             2.849 |
| household + other             | True             |       8 |                    131 |      0.867 |      1.12  |        0.0151 |             2.979 |
| dairy + meat and seafood      | True             |      35 |                    977 |      0.867 |      1.447 |        0.0174 |             6.682 |
| beverages + other             | True             |      20 |                    516 |      0.866 |      1.232 |        0.0187 |             9.439 |
| bakery + snacks and sweets    | True             |       4 |                     73 |      0.862 |      1.082 |        0.0138 |             3.117 |
| produce + snacks and sweets   | True             |       7 |                    122 |      0.859 |      1.155 |        0.014  |             6.173 |
| bakery + other                | True             |      16 |                    408 |      0.849 |      1.126 |        0.0176 |             6.608 |
| bakery + household            | True             |       8 |                    191 |      0.833 |      1.519 |        0.0162 |             8.515 |

## Basket Segments

|   cluster |   transactions |   avg_basket_size | top_items                                                        |
|----------:|---------------:|------------------:|:-----------------------------------------------------------------|
|         0 |           8637 |              2.36 | yogurt, root vegetables, tropical fruit, bottled water, sausage  |
|         1 |           3382 |              2.7  | whole milk, other vegetables, yogurt, tropical fruit, sausage    |
|         2 |           1508 |              2.82 | rolls/buns, whole milk, other vegetables, yogurt, tropical fruit |
|         3 |           1436 |              2.88 | soda, whole milk, other vegetables, rolls/buns, yogurt           |