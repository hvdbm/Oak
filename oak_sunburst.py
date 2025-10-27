import os
from argparse import ArgumentParser

from src.family import Family
from src.sunburst.sunburst import draw_sunburst

def main(input_path: str, person_id: str, max_depth: int, output_dir: str) -> None:
  if not os.path.exists(output_dir): os.makedirs(output_dir)
  family = Family.from_path(input_path)
  draw_sunburst(family, person_id, max_depth, output_dir)

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_path", "-i", type=str, required=True, help="Path to the family data (a file or a folder).")
  parser.add_argument("--person_id", "-p", type=str, required=True, help="ID of the person to center the sunburst on.")
  parser.add_argument("--max_depth", "-d", type=int, default=-1, help="Maximum number of layer to renderer. Default to -1 to show the complete hiearchy.")
  parser.add_argument("--output_dir", "-o", type=str, default=".", help="Path to the output directory. Take current folder as default.")
  
  args = parser.parse_args()
  main(args.input_path, args.person_id, args.max_depth, args.output_dir)