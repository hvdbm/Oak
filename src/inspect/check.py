from src.family import Family

def check_errors(family: Family) -> None:
  """
  Check for errors in the family data and print them.
  Errors are:
  - A person has an unknown parent.
  - A person has an unknown spouse.
  - A person has an unknown child.

  Parameters:
    family (Family): The family object to check.

  Returns:
    None
  """
  errors = []

  for person in family.members.values():
    for parent in person.parents:
      if parent not in family.members.keys():
        errors.append(f'🚫  "{person.id}" has an unknown parent: "{parent}"')

    for spouse in person.spouses:
      if spouse not in family.members.keys():
        errors.append(f'🚫  "{person.id}" has an unknown spouse: "{spouse}"')

    for child in person.childrens:
      if child not in family.members.keys():
        errors.append(f'🚫  "{person.id}" has an unknown child: "{child}"')
  
  if len(errors) > 0:
    print(f"{len(errors)} errors:")
    for warning in errors:
      print(warning)
  else:
    print("No errors.")

def check_events(family: Family) -> None:
  """
  Check the oldest and most recent events in the family data and print them.
  
  Parameters:
    family (Family): The family object to check.

  Returns:
    None
  """
  events = []

  for person in family.members.values():
    try:
      events.append(int(person.birth_year))
      if person.death_year != None: events.append(int(person.death_year))
    except ValueError:
      continue
  
  if len(events) == 0: return

  events.sort()
  print(f"📅 Oldest event             : {events[0]}")
  print(f"📅 Most recent event        : {events[-1]}")

def check_nationalities(family: Family) -> None:
  """
  Check the number of nationalities in the family data and print them.

  Parameters:
    family (Family): The family object to check.

  Returns:
    None
  """
  nationalities_count: dict[str, int] = {}

  for person in family.members.values():
    for nationality in person.nationalities:
      if nationality not in nationalities_count.keys():
        nationalities_count[nationality] = 1
      else:
        nationalities_count[nationality] += 1

  print(f"🌐 Number of nationalities  : {len(nationalities_count)}")
  for nationality, count in nationalities_count.items():
    print(f"   - {nationality} : {count} persons ({count/len(family.members.keys())*100:.2f}%)")

def check_warnings(family: Family) -> None:
  """
  Check for warnings in the family data and print them.
  Warnings are:
  - A person has no relatives.
  - A person's death_year is before their birth_year.

  Parameters:
    family (Family): The family object to check.

  Returns:
    None
  """
  warnings = []
  
  for person in family.members.values():
    if len(person.parents) == 0 and len(person.spouses) == 0 and len(person.childrens) == 0:
      warnings.append(f'🚧  "{person.id}" has no relatives.')

    if person.death_year != None:
      try:
        if int(person.death_year) < int(person.birth_year):
          warnings.append(f'🚧  "{person.id}" has a death year before their birth year.')
      except ValueError:
        continue

  if len(warnings) > 0:
    print(f"{len(warnings)} warnings:")
    for warning in warnings:
      print(warning)
  else:
    print("No warnings.")