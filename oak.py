import os
from argparse import ArgumentParser
from src.family import read_family, draw_family_tree

def main(csv_path: str, output_dir: str) -> None:
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  family_data = read_family(csv_path)
  draw_family_tree(family_data, output_dir)

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_file", type=str, required=True, help="Path to the csv file containing the family data")
  parser.add_argument("--output_dir", type=str, help="Path to the output directory")

  args = parser.parse_args()
  main(args.input_file, args.output_dir)