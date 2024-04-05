import pandas as pd
import glob
import os


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



def read_xlsx_files(directory_path):
    """
    Reads all .xlsx files from the specified directory path and returns a combined Pandas DataFrame.

    Args:
        directory_path (str): Path to the directory containing .xlsx files.

    Returns:
        pd.DataFrame: Combined DataFrame containing data from all .xlsx files.
    """
    # Initialize an empty list to store DataFrames from each file
    dfs = []

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(directory_path, filename)
            try:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(file_path)
                dfs.append(df)
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # Combine all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df


