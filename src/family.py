import glob
import os

import pandas as pd

from src.person import Person
from src.utils import ACCEPTED_EXTENSIONS, read_file_as_dict

class FamilyPathInfos():
  def __init__(self, path: str):
    self.path = path
    self.is_dir = os.path.isdir(path)
    if self.is_dir:
      self.files = []
      for extension in ACCEPTED_EXTENSIONS:
        self.files += glob.glob(f'{path}/*.{extension}')
    else:
      self.files = [path]

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
        family = read_file_as_dict(file)
        for m in family["members"]:
          person = Person(**m)
          members[person.id] = person
        if "name" in family : names.append(family["name"])
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
      if children not in self.members: continue
      n += self.find_n_descendants(self.members[children])+1
    return n
  
  def is_only_child(self, id: str) -> bool:
    """
    Check if a person is an only child. Doesn't count half-siblings.

    Parameters:
      id (str): The id of the person to check.

    Returns:
      bool: If the person is an only child.
    """
    if id not in self.members: return False

    for parent in self.members[id].parents:
      if parent not in self.members: continue
      if len(self.members[parent].childrens) == 1: return True

    return False

  def remove_person(self, id: str) -> None:
    """
    Remove a person from the family.

    Parameters:
      id (str): The id of the person to remove.

    Returns:
      None
    """
    if id in self.members:
      del self.members[id]

    for person in self.members.values():
      person.n_descendants = None

      if id in person.parents: 
        person.parents = [i for i in person.parents if i != id]
      if id in person.spouses:
        person.spouses = [i for i in person.spouses if i != id]
      if id in person.childrens:
        person.childrens = [i for i in person.childrens if i != id]
    
    for person in self.members.values():
      person.n_descendants = self.find_n_descendants(person)

  def to_df(self) -> pd.DataFrame:
    """
    Convert the list of members of the family as a Pandas dataframe with the properties of a Person as columns.
    
    Returns:
      pd.DataFrame: the list of members as a dataframe.
    """
    return pd.DataFrame([vars(x) for x in self.members.values()])
