import os
from argparse import ArgumentParser

from src.family import Family
from src.configuration import Configuration

def main(csv_path: str, config_file_path: str | None, output_dir: str) -> None:
  if not os.path.exists(output_dir): os.makedirs(output_dir)

  config = Configuration.from_path(config_file_path)
  output_file_path = os.path.join(output_dir, config.filename)

  Family.from_path(csv_path).draw_family_tree(config, output_file_path)

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_file_path", type=str, required=True, help="Path to the file containing the family data.")
  parser.add_argument("--config_file_path", type=str, default=None, help="Path to the YAML file containing configuration of the family tree. This file is optionnal.")
  parser.add_argument("--output_dir", type=str, help="Path to the output directory. Take current folder as default.")

  args = parser.parse_args()
  main(args.input_file_path, args.config_file_path, args.output_dir)