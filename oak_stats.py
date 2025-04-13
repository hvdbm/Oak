from argparse import ArgumentParser
import os

from src.family import Family
from src.stats.transform import convert_column_to_int
from src.stats.evolution import plot_swarm
from src.stats.repartition import plot_pie, plot_bar

def main(input_path: str, output_dir: str) -> None:
  output_dir += "/stats"
  if not os.path.exists(output_dir): os.makedirs(output_dir)
  
  family = Family.from_path(input_path)
  family_df = family.to_df()
  
  family_df["number_spouses"] = family_df["spouses"].map(len)
  family_df["number_childrens"] = family_df["childrens"].map(len)

  # Plot evolution
  plot_swarm(
    convert_column_to_int(family_df.explode("nationalities"), "birth_year"),
    "birth_year",
    "nationalities",
    f'Evolution of Nationalities \n of "{family.name}" in time',
    os.path.join(output_dir, "nationalities_evolution.png")
  )

  plot_swarm(
    convert_column_to_int(family_df[family_df["number_spouses"] > 0], "birth_year"),
    "birth_year",
    "number_spouses",
    f'Evolution of Number of Spouses \n of "{family.name}" in time',
    os.path.join(output_dir, "spouses_evolution.png")
  )

  plot_swarm(
    convert_column_to_int(family_df[family_df["number_childrens"] > 0], "birth_year"),
    "birth_year",
    "number_childrens",
    f'Evolution of Number of Childrens \n of "{family.name}" in time',
    os.path.join(output_dir, "childrens_evolution.png")
  )

  # Plot repartition
  plot_pie(
    family_df["sex"].value_counts(),
    f'Sex Repartition \n of "{family.name}"',
    os.path.join(output_dir, "sex_repartition.png")
  )

  plot_pie(
    family_df.explode("nationalities")["nationalities"].value_counts(),
    f'Nationalities Repartition \n of "{family.name}"',
    os.path.join(output_dir, "nationalities_repartition.png")
  )

  plot_bar(
    family_df["last_name"].value_counts(),
    f'Last Name Repartition \n of "{family.name}"',
    os.path.join(output_dir, "last_name_repartition.png")
  )

  plot_bar(
    family_df["first_name"].value_counts(),
    f'First Name Repartition \n of "{family.name}"',
    os.path.join(output_dir, "first_name_repartition.png")
  )

  plot_bar(
    family_df["number_spouses"].value_counts(),
    f'Number of Spouses Repartition \n of "{family.name}"',
    os.path.join(output_dir, "spouses_repartition.png")
  )

  plot_bar(
    family_df["number_childrens"].value_counts(),
    f'Number of Children Repartition \n of "{family.name}"',
    os.path.join(output_dir, "children_repartition.png")
  )

if __name__ == "__main__":
  parser = ArgumentParser()

  parser.add_argument("--input_path", "-i", type=str, required=True, help="Path to the file containing the family data.")
  parser.add_argument("--output_dir", "-o", type=str, default=".", help="Path to the output directory. Take current folder as default.")

  args = parser.parse_args()
  main(args.input_path, args.output_dir)