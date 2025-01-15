import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_pie_repartition(value_counts: pd.Series, title: str, output_path: str) -> None:
  """
  Plot a pie chart of the repartition of a categorical variable.

  Parameters:
    value_counts (pd.Series): The value counts of the categorical variable.
    title (str): The title of the plot.
    output_path (str): The path to save the plot
  
  Returns:
    None
  """
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