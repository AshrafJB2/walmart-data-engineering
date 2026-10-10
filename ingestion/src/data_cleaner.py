import argparse
from pathlib import Path

import pandas as pd


INTEGER_COLUMNS = {
    "customer_id",
    "employee_id",
    "store_id",
    "product_id",
    "order_id",
    "order_item_id",
    "quantity",
}
DECIMAL_COLUMNS = {
    "price",
    "salary",
    "total_amount",
    "unit_price",
    "line_amount",
}
TIMESTAMP_COLUMNS = {
    "created_timestamp",
    "updated_timestamp",
    "order_timestamp",
}


TRUE_VALUES = {"YES", "Y", "TRUE", "T", "1"}
FALSE_VALUES = {"NO", "N", "FALSE", "F", "0"}

def to_boolean(series: pd.Series) -> pd.Series:
    s = series.astype("string").str.strip().str.upper()
    result = pd.Series(pd.NA, index=s.index, dtype="boolean")
    result[s.isin(TRUE_VALUES)] = True
    result[s.isin(FALSE_VALUES)] = False
    return result


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize text, apply known Walmart column types, and drop duplicate rows."""
    cleaned = df.copy()
    cleaned.columns = [str(column).strip() for column in cleaned.columns]
    if not cleaned.columns.is_unique:
        raise ValueError("Column names must be unique after trimming whitespace.")

    for column in cleaned.columns:
        if pd.api.types.is_object_dtype(cleaned[column].dtype) or isinstance(
            cleaned[column].dtype, pd.StringDtype
        ):
            cleaned[column] = cleaned[column].astype("string").str.strip()
            cleaned[column] = cleaned[column].replace("", pd.NA)

    for column in cleaned.columns:
        normalized_name = column.strip().lower()
        if normalized_name in INTEGER_COLUMNS:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce").astype(
                "Int64"
            )
        elif normalized_name in DECIMAL_COLUMNS:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce").astype(
                "Float64"
            )
        elif normalized_name in TIMESTAMP_COLUMNS:
            cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")
        elif normalized_name == "is_active":
            cleaned[column] = to_boolean(cleaned[column])


    return cleaned.drop_duplicates().reset_index(drop=True)


def clean_csv_directory(input_dir: Path, output_dir: Path) -> list[Path]:
    """Clean each CSV directly inside input_dir and write a copy to output_dir."""
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {input_dir}")

    csv_paths = sorted(input_dir.glob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = []
    for csv_path in csv_paths:
        dataframe = pd.read_csv(csv_path)
        cleaned = clean_dataframe(dataframe)
        output_path = output_dir / csv_path.name
        cleaned.to_csv(output_path, index=False)
        output_paths.append(output_path)

    return output_paths

