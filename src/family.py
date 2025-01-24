import glob
import json
import os

import pandas as pd

from src.person import Person

class FamilyPathInfos():
  def __init__(self, path: str):
    self.path = path
    self.is_dir = os.path.isdir(path)
    self.files = glob.glob(f'{path}/*.json') if self.is_dir else [path]

class Family():
  def __init__(self,
    name: str | None = None,
    members: dict[str, Person] = {},
    path_info: FamilyPathInfos = None
  ):
    self.name = name
    self.members = members
    self.path_info = path_info

    for value in members.values():
      value.n_descendants = self.find_n_descendants(value)

  @classmethod
  def from_path(cls, path: str):
    """
    Read a family from a path. If the path is a directory containing multiple files, the family will be the union of all the families in the files.

    Parameters:
      path (str): The path to the file or directory containing the family data.

    Returns:
      Family: The family object.
    """

    path_info = FamilyPathInfos(path)

    members = {}
    names = []

    try:
      for file in path_info.files:
        with open(file, 'r') as f:
          family = json.load(f)
          for m in family["members"]:
            person = Person(**m)
            members[person.id] = person
          if "name" in family.keys() : names.append(family["name"])
    except Exception as e:
      print(f'Error: Could not read the family from file "{file}": {e}')
    
    names = " / ".join(names) if len(names) > 0 else None
    return cls(names, members, path_info)
    
  def find_n_descendants(self, person: Person) -> int:
    """
    Find the number of descendants of a person. This number is calculated recursively.

    Parameters:
      person (Person): The person to find the number of descendants.

    Returns:
      int: The number of descendants of the person.
    """

    if person.childrens == []: return 0
    if person.n_descendants != None: return person.n_descendants

    n = 0
    for children in person.childrens:
      if children not in self.members.keys(): continue
      n += self.find_n_descendants(self.members[children])+1
    return n

  def to_df(self) -> pd.DataFrame:
    """
    Convert the list of members of the family as a Pandas dataframe with the properties of a Person as columns.
    """
    return pd.DataFrame([vars(x) for x in self.members.values()])
