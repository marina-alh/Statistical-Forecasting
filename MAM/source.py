import pandas as pd


def convert_columns_to_numeric(df, columns_to_convert):
    """
    Converts specified columns in a DataFrame to numeric (float) type.
    Non-numeric values are replaced with ASCII zero.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns_to_convert (list): List of column names to convert.

    Returns:
        pd.DataFrame: Modified DataFrame with specified columns converted to numeric.
    """
    for col in columns_to_convert:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna("0")
    return df