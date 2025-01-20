import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from . import FIG_SIZE

def plot_pie(value_counts: pd.Series, title: str, output_path: str) -> None:
  """
  Plot a pie chart of the repartition of a categorical variable.

  Parameters:
    value_counts (pd.Series): The value counts of the categorical variable.
    title (str): The title of the plot.
    output_path (str): The path to save the plot
  
  Returns:
    None
  """
  plt.subplots(figsize=FIG_SIZE)
  plt.pie(
    value_counts.values,
    labels=value_counts.keys(),
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('Set2'),
  )
  plt.title(title, weight='bold')
  plt.savefig(output_path)
  plt.close()

def plot_bar(value_counts: pd.Series, title: str, output_path: str, horizontal: bool = True) -> None:
  """
  Plot a bar chart of the repartition of a categorical variable.

  Parameters:
    value_counts (pd.Series): The value counts of the categorical variable.
    title (str): The title of the plot.
    output_path (str): The path to save the plot
    horizontal (bool): Whether to plot the bar chart horizontally or vertically
  
  Returns:
    None
  """
  plt.subplots(figsize=FIG_SIZE)

  # Sort by count 
  value_counts = value_counts.sort_values(ascending=True)

  if horizontal:
    plt.barh(
      value_counts.keys(),
      value_counts.values,
    )
  else:
    plt.bar(
      value_counts.keys(),
      value_counts.values,
    )

  plt.title(title, weight='bold')
  plt.savefig(output_path)
  plt.close()