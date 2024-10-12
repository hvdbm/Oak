import os
from argparse import ArgumentParser
import json
from src.family import read_family, draw_family_tree

def load_config(file_path: str | None) -> dict:
  if file_path is None : return {}
  
  with open(file_path, 'r') as file:
    return json.load(file)
  
def main(csv_path: str, config_file_path: str | None, output_dir: str) -> None:
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  config = load_config(config_file_path)

  family_data = read_family(csv_path)

  output_file_path = os.path.join(output_dir, config.get("filename", "family_tree.png"))
  
  node_shape = config.get("node_shape", "box")
  graph_title = config.get("graph_title", "")
  show_nickname = config.get("show_nickname", False)

  draw_family_tree(family_data, node_shape, output_file_path, graph_title, show_nickname)

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_file_path", type=str, required=True, help="Path to the JSON file containing the family data")
  parser.add_argument("--config_file_path", type=str, default=None, help="Path to the JSON file containing configuration of the family tree")
  parser.add_argument("--output_dir", type=str, help="Path to the output directory")

  args = parser.parse_args()
  main(args.input_file_path, args.config_file_path, args.output_dir)