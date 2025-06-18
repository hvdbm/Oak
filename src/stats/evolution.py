import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from . import FIG_SIZE


def plot_swarm(data: pd.DataFrame, x: str, y: str, title: str, output_path: str) -> None:
  """
  Plot a swarmplot of the repartition of two variables.

  Parameters:
    data (pd.DataFrame): The data to plot.
    x (str): The column name of the x-axis variable.
    y (str): The column name of the y-axis variable.
    title (str): The title of the plot.
    output_path (str): The path to save the plot
  
  Returns:
    None
  """
  plt.subplots(figsize=FIG_SIZE)
  sns.set_palette("Set2")
  sns.swarmplot(x=x, y=y, data=data, hue=y)
  plt.title(title, weight='bold')
  plt.savefig(output_path)
  plt.close()