from argparse import ArgumentParser

from src.family import Family

def main(input_path: str) -> None:
  family = Family.from_path(input_path)

  print("="*100)
  print("Files informations:")
  print("="*100)
  print(f"📦 Path     : {input_path}")
  print(f"💾 Type     : {'Directory' if family.path_info.is_dir else 'File'}")
  print(f"📁 Number of files    : {len(family.path_info.files)}")
  for file in family.path_info.files: print(f"  - {file.split('/')[-1]}")
  print()

  print("="*100)
  print(f"Family informations:")
  print("="*100)
  print(f"👥 Number of persons        : {len(family.members.keys())}")
  check_nationalities(family)
  check_events(family)
  print()

  print("="*100)
  print(f"Validation:")
  print("="*100)
  check_warnings(family)
  print()

def check_warnings(family: Family) -> None:
  warnings = []

  for person in family.members.values():

    for parent in person.parents:
      if parent not in family.members.keys():
        warnings.append(f'🚫  "{person.id}" has an unknown parent: "{parent}")')

    for spouse in person.spouses:
      if spouse not in family.members.keys():
        warnings.append(f'🚫  "{person.id}" has an unknown spouse: "{spouse}")')

    for child in person.childrens:
      if child not in family.members.keys():
        warnings.append(f'🚫  "{person.id}" has an unknown child: "{child}")')
  
  if len(warnings) > 0:
    print(f"{len(warnings)} warnings:")
    for warning in warnings:
      print(warning)
  else:
    print("No warnings.")

def check_nationalities(family: Family) -> int:
  nationalities_count = {}

  for person in family.members.values():
    for nationality in person.nationalities:

      if nationality not in nationalities_count.keys():
        nationalities_count[nationality] = 1
      else:
        nationalities_count[nationality] += 1

  print(f"🌐 Number of nationalities  : {len(nationalities_count)}")
  for nationality, count in nationalities_count.items():
    print(f"   - {nationality} : {count} persons ({count/len(family.members.keys())*100:.2f}%)")

def check_events(family: Family) -> None:
  events = []

  for person in family.members.values():
    events.append(person.birth_year)
    if person.death_year != None: events.append(person.death_year)

  if len(events) == 0: return

  events.sort()
  print(f"📅 Oldest event             : {events[0]}")
  print(f"📅 Most recent event        : {events[-1]}")

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--input_path", "-i", type=str, required=True, help="Path to the family data.")

  args = parser.parse_args()
  main(args.input_path)