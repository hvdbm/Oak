from argparse import ArgumentParser
import os

from src.family import Family
from src.stats.repartition import plot_pie_repartition

def main(input_file_path: str, output_dir: str) -> None:
  if output_dir is not None and not os.path.exists(output_dir): os.makedirs(output_dir)

  family = Family.from_path(input_file_path)
  family_df = family.to_df()

  plot_pie_repartition(
    family_df["nationalities"].value_counts(),
    f'Nationalities Repartition of "{family.name}"',
    os.path.join(output_dir, "nationalities_repartition.png")
  )
  
  plot_pie_repartition(
    family_df["sex"].value_counts(),
    f'Sex Repartition of "{family.name}"',
    os.path.join(output_dir, "sex_repartition.png")
  )


if __name__ == "__main__":
  parser = ArgumentParser()

  parser.add_argument("--input_file_path", type=str, required=True, help="Path to the file containing the family data.")
  parser.add_argument("--output_dir", type=str, help="Path to the output directory. Take current folder as default.")

  args = parser.parse_args()
  main(args.input_file_path, args.output_dir)