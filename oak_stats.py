import os
from argparse import ArgumentParser

from src.family import Family
from src.stats.evolution import plot_swarm
from src.stats.repartition import plot_bar, plot_pie
from src.stats.transform import convert_column_to_int
from src.stats.configuration import StatsConfiguration


def main(input_path: str, config_file_path: str | None, output_dir: str) -> None:
  config = StatsConfiguration.from_path(config_file_path)

  # Create folder with all the stats figures
  output_dir += f"/{config.folder_name}"
  if not os.path.exists(output_dir): os.makedirs(output_dir)
  
  family_df = Family.from_path(input_path).to_df()

  # Plot evolution
  print("nationalities_evolution")
  plot_swarm(
    convert_column_to_int(family_df.explode("nationalities"), "birth_year"),
    "birth_year",
    "nationalities",
    f'Evolution of nationalities in time',
    os.path.join(output_dir, "nationalities_evolution.png")
  )

  # Plot repartition
  print("sex_repartition")
  plot_pie(
    family_df["sex"].value_counts(),
    f'Sex repartition',
    os.path.join(output_dir, "sex_repartition.png")
  )

  print("nationalities_repartition")
  plot_bar(
    family_df.explode("nationalities")["nationalities"].value_counts(),
    f'Nationalities repartition',
    os.path.join(output_dir, "nationalities_repartition.png")
  )

  print("last_name_repartition")
  plot_bar(
    family_df["last_name"].value_counts(),
    f'Last name repartition',
    os.path.join(output_dir, "last_name_repartition.png")
  )

  print("first_name_repartition")
  plot_bar(
    family_df["first_name"].value_counts(),
    f'First name repartition',
    os.path.join(output_dir, "first_name_repartition.png")
  )

if __name__ == "__main__":
  parser = ArgumentParser()

  parser.add_argument("--input_path", "-i", type=str, required=True, help="Path to the family data (a file or a folder).")
  parser.add_argument("--config_file_path", "-c", type=str, default=None, help="Path to the YAML file containing configuration of the stats. This file is optionnal.")
  parser.add_argument("--output_dir", "-o", type=str, default=".", help="Path to the output directory. Take current folder as default.")

  args = parser.parse_args()
  main(args.input_path, args.config_file_path, args.output_dir)