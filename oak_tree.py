import os
from argparse import ArgumentParser

from src.family import Family
from src.tree.draw import TreeConfiguration, draw_tree


def main(input_path: str, config_file_path: str | None, output_dir: str) -> None:
  if not os.path.exists(output_dir): os.makedirs(output_dir)

  config = TreeConfiguration.from_path(config_file_path)
  family = Family.from_path(input_path, config.trim_config.ignore_incomplete_relations)
  output_file_path = os.path.join(output_dir, config.filename)

  draw_tree(family, config, output_file_path)

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_path", "-i", type=str, required=True, help="Path to the family data (a file or a folder).")
  parser.add_argument("--config_file_path", "-c", type=str, default=None, help="Path to the YAML file containing configuration of the family tree. This file is optionnal.")
  parser.add_argument("--output_dir", "-o", type=str, default=".", help="Path to the output directory. Take current folder as default.")

  args = parser.parse_args()
  main(args.input_path, args.config_file_path, args.output_dir)