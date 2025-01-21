from argparse import ArgumentParser
import os

from src.family import Family
from src.tree.draw import draw_tree, TreeConfiguration

def main(input_path: str, config_file_path: str | None, output_dir: str) -> None:
  if not os.path.exists(output_dir): os.makedirs(output_dir)

  family = Family.from_path(input_path)
  config = TreeConfiguration.from_path(config_file_path)
  output_file_path = os.path.join(output_dir, config.filename)

  draw_tree(family, config, output_file_path)

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_path", "-i", type=str, required=True, help="Path to the file containing the family data.")
  parser.add_argument("--config_file_path", type=str, default=".", help="Path to the YAML file containing configuration of the family tree. This file is optionnal.")
  parser.add_argument("--output_dir", "-o", type=str, help="Path to the output directory. Take current folder as default.")

  args = parser.parse_args()
  main(args.input_path, args.config_file_path, args.output_dir)