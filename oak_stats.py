from argparse import ArgumentParser
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.family import Family

def main(input_file_path: str, output_dir: str) -> None:
  if output_dir is not None and not os.path.exists(output_dir): os.makedirs(output_dir)

  family = Family.from_path(input_file_path)

  plot_sex_repartition(family.to_df(), f'Sex Repartition of "{family.name}"', output_dir)


def plot_sex_repartition(df: pd.DataFrame, title: str, output_dir: str):
  values_count = df["sex"].value_counts()

  plt.pie(
    values_count.values,
    labels=values_count.keys(),
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('Set2'),
  )
  plt.title(title, weight='bold')
  plt.savefig(os.path.join(output_dir, "sex_repartition.png"))

if __name__ == "__main__":
  parser = ArgumentParser()

  parser.add_argument("--input_file_path", type=str, required=True, help="Path to the file containing the family data.")
  parser.add_argument("--output_dir", type=str, help="Path to the output directory. Take current folder as default.")

  args = parser.parse_args()
  main(args.input_file_path, args.output_dir)