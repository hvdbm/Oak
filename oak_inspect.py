from argparse import ArgumentParser
import os

def main(input_path: str) -> None:
  is_dir = os.path.isdir(input_path)

  print("="*100)
  print(f"📦 Path     : {input_path}")
  print(f"💾 Type     : {'Directory' if is_dir else 'File'}")
  print(f"📁 Files    : TODO")
  print()
  print(f"👥 Number of persons        : TODO")
  print(f"🌐 Number of nationalities  : TODO")
  print(f"📅 Oldest event             : TODO")
  print(f"📅 Most recent event        : TODO")
  print()
  print(f"📝 Last edit : TODO")

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_path", type=str, required=True, help="Path to the family data.")

  args = parser.parse_args()
  main(args.input_path)