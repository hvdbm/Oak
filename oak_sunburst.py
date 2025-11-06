from argparse import ArgumentParser

from src.family import Family
from src.sunburst.sunburst import draw_sunburst


def main(
  input_path: str,
  person_id: str,
  output_dir: str | None,
  output_filename: str,
  output_format: str,
  max_depth: int,
  no_interactive: bool,
  equally_weighted: bool,
  sunburst_type: str
) -> None:
  family = Family.from_path(input_path)

  draw_sunburst(
    family,
    person_id,
    output_dir,
    output_filename,
    output_format,
    max_depth,
    no_interactive,
    equally_weighted,
    sunburst_type
  )

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_path", "-i", type=str, required=True, help="Path to the family data (a file or a folder).")
  parser.add_argument("--person_id", "-p", type=str, required=True, help="ID of the person to center the sunburst on.")
  parser.add_argument("--output_dir", "-o",  default=None, help="Path to the output directory. Default to None, no file is saved.")
  parser.add_argument("--output_filename", "-fi", type=str, default="sunburst", help="Name of the file. Default to 'suburst'.")
  parser.add_argument("--output_format", "-fo", type=str, default="html", help="Extension of the output file. Accepted format : 'png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'html'. Default to 'html'.")
  parser.add_argument("--max_depth", "-d", type=int, default=-1, help="Maximum number of layer to renderer. Default to -1 to show the complete hiearchy.")
  parser.add_argument("--no_interactive", "-ni", action="store_true", help="Don't show the interactive sunburst window with Plotly.")
  parser.add_argument("--equally_weighted", "-ew", action="store_true", help="Weight all sectors at the same depth equally.")
  parser.add_argument("--type", "-t", type=str, default="ancestors", choices=["ancestors", "descendants"], help="Type of sunburst to draw: 'ancestors' or 'descendants'. Default to 'ancestors'.")

  args = parser.parse_args()
  main(
    args.input_path,
    args.person_id,
    args.output_dir,
    args.output_filename,
    args.output_format,
    args.max_depth,
    args.no_interactive,
    args.equally_weighted,
    args.type
  )