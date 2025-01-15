import pandas as pd

def convert_column_to_int(data: pd.DataFrame, column: str) -> pd.DataFrame:
  """
  Convert a column to integer type.

  Parameters:
    data (pd.DataFrame): The data to convert.
    column (str): The column to convert.
  
  Returns:
    pd.DataFrame: The converted data.
  """
  data = data[data[column].str.isnumeric()] # Drop row if column is not a number
  data[column] = data[column].astype(int)

  return data