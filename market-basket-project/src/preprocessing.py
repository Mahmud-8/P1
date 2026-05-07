from __future__ import annotations

import re
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = {"Member_number", "Date", "itemDescription"}


def clean_groceries_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the Groceries dataset into one row per transaction item."""
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=list(REQUIRED_COLUMNS))
    cleaned["Member_number"] = cleaned["Member_number"].astype(str).str.strip()
    cleaned["Date"] = pd.to_datetime(cleaned["Date"], dayfirst=True, errors="coerce")
    cleaned["itemDescription"] = (
        cleaned["itemDescription"]
        .astype(str)
        .str.lower()
        .str.strip()
        .map(lambda value: re.sub(r"\s+", " ", value))
    )
    cleaned = cleaned.dropna(subset=["Date"])
    cleaned = cleaned[cleaned["itemDescription"] != ""]
    cleaned = cleaned.drop_duplicates(subset=["Member_number", "Date", "itemDescription"])
    cleaned["Transaction"] = (
        cleaned["Member_number"] + "_" + cleaned["Date"].dt.strftime("%Y-%m-%d")
    )
    return cleaned.reset_index(drop=True)


def create_transactions(df: pd.DataFrame) -> list[list[str]]:
    cleaned = clean_groceries_data(df) if "Transaction" not in df.columns else df.copy()
    baskets = cleaned.groupby("Transaction")["itemDescription"].apply(list)
    return baskets.tolist()


def create_basket_matrix(
    df: pd.DataFrame,
    min_item_frequency: int = 1,
    min_support: float | None = None,
) -> pd.DataFrame:
    cleaned = clean_groceries_data(df) if "Transaction" not in df.columns else df.copy()
    basket = pd.crosstab(cleaned["Transaction"], cleaned["itemDescription"])
    basket = basket.astype(bool)

    if min_item_frequency > 1:
        frequent_items = basket.sum(axis=0) >= min_item_frequency
        basket = basket.loc[:, frequent_items]

    if min_support is not None:
        supported_items = basket.mean(axis=0) >= min_support
        basket = basket.loc[:, supported_items]

    return basket


def item_frequency(basket_df: pd.DataFrame) -> pd.Series:
    return basket_df.sum(axis=0).sort_values(ascending=False)


def transaction_size_summary(basket_df: pd.DataFrame) -> pd.Series:
    return basket_df.sum(axis=1).describe()


def co_occurrence_matrix(
    basket_df: pd.DataFrame,
    items: Iterable[str] | None = None,
    top_n: int | None = 25,
) -> pd.DataFrame:
    if items is None:
        ranked_items = item_frequency(basket_df)
        selected_items = ranked_items.head(top_n).index if top_n else ranked_items.index
    else:
        selected_items = [item for item in items if item in basket_df.columns]

    selected = basket_df.loc[:, selected_items].astype(int)
    matrix = selected.T.dot(selected)
    for item in matrix.index:
        matrix.loc[item, item] = 0
    return matrix


def monthly_transaction_counts(cleaned_df: pd.DataFrame) -> pd.Series:
    if "Transaction" not in cleaned_df.columns:
        cleaned_df = clean_groceries_data(cleaned_df)
    monthly = cleaned_df.drop_duplicates("Transaction").set_index("Date")
    return monthly.resample("ME")["Transaction"].count()
