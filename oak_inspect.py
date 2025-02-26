from argparse import ArgumentParser

from src.family import Family
from src.inspect.check import check_errors, check_events, check_nationalities, check_warnings

def splitter(len: int = 100) -> None:
  print("="*len)

def main(input_path: str) -> None:
  family = Family.from_path(input_path)

  splitter()
  print("Files informations :")
  splitter()
  print(f"📦 Path             : {input_path}")
  print(f"🔖 Type             : {'Directory' if family.path_info.is_dir else 'File'}")
  print(f"📁 Number of files  : {len(family.path_info.files)}")
  for file in family.path_info.files: print(f"  - {file.split('/')[-1]}")
  print()

  splitter()
  print(f"Family informations :")
  splitter()
  print(f"👥 Number of persons        : {len(family.members.keys())}")
  check_nationalities(family)
  check_events(family)
  print()

  splitter()
  print(f"Validation :")
  splitter()
  check_warnings(family)
  print()
  check_errors(family)
  print()

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_path", "-i", type=str, required=True, help="Path to the family data.")

  args = parser.parse_args()
  main(args.input_path)