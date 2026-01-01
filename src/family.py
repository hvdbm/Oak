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
  n_descendants: dict[str, int] = {}

  def __init__(self,
    name: str | None = None,
    members: dict[str, Person] = {},
    path_info: FamilyPathInfos | None = None,
    ignore_incomplete_relations: bool = False
  ):
    self.name = name
    self.members = members
    self.path_info = path_info

    if ignore_incomplete_relations:
      for value in members.values():
        value.parents = [parent for parent in value.parents if parent in members.keys()]
        value.spouses = [spouse for spouse in value.spouses if spouse in members.keys()]
        value.children = [children for children in value.children if children in members.keys()]

    # Count the number of descendants for each member
    for person in members.values():
      self.n_descendants[person.id] = self.__count_n_descendants(person)

  @classmethod
  def from_path(cls, path: str, ignore_incomplete_relations: bool = False):
    """
    Read a family from a path. If the path is a directory containing multiple files, the family will be the union of all the families in the files.

    Parameters:
      path (str): The path to the file or directory containing the family data.
      ignore_incomplete_relations (bool): Ignore the incomplete relations between members. Default at False.

    Returns:
      Family: The family object.
    """
    path_info = FamilyPathInfos(path)

    members: dict[str, Person] = {}
    names: list[str] = []

    try:
      for file in path_info.files:
        family = read_file_as_dict(file)
        for m in family["members"]:
          person = Person(**m)
          members[person.id] = person
        if "name" in family : names.append(family["name"])
    except Exception as e:
      print(f'Error: Could not read the family from file "{file}": {e}')
    
    family_name = " / ".join(names) if len(names) > 0 else None
    return cls(family_name, members, path_info, ignore_incomplete_relations)
    
  def __count_n_descendants(self, person: Person) -> int:
    """
    Count the number of descendants of a person. This number is calculated recursively.

    Parameters:
      person (Person): The person to find the number of descendants.

    Returns:
      int: The number of descendants of the person.
    """
    if person.id in self.n_descendants: return self.n_descendants[person.id]
    if person.children == []: return 0

    n = 0
    for children in person.children:
      if children not in self.members: continue
      n += self.__count_n_descendants(self.members[children])+1
    return n
  
  def get_ancestors(self, id: str) -> list[str]:
    if id not in self.members: return []

    ancestors = []

    for parent in self.members[id].parents:
      if parent not in self.members: continue
      ancestors.append(parent)
      ancestors += self.get_ancestors(parent)
    
    return ancestors

  def get_descendants(self, id: str, include_spouses: bool = False) -> tuple[list[str], list[str]]:
    """
    Get all the descendants ids of a person.

    Parameters:
      id (str): The id of the person to get the descendants.
      include_spouses (bool): Include descendants's spouses in the list.

    Returns:
      list[str]: The ids of the descendants of the person.
      list[str]: The ids of the descendants's spouses of the person.
    """
    if id not in self.members: return ([], [])

    descendants = []
    spouses = []

    for child in self.members[id].children:
      descendants.append(child)
      if child not in self.members: continue
      if include_spouses:
        spouses += self.members[child].spouses

      tmp_descendants, tmp_spouses = self.get_descendants(child, include_spouses)
      descendants += tmp_descendants
      spouses += tmp_spouses

    return descendants, spouses

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
      if len(self.members[parent].children) == 1: return True

    return False

  def remove_persons(self, ids: list | set | None) -> None:
    """
    Remove a list of persons from the family.

    Parameters :
      ids (list): The ids of the persons to remove.

    Returns:
      None
    """
    if ids is None: return

    for id in ids:
      if id in self.members: del self.members[id]

    for person in self.members.values():
      self.n_descendants.pop(person.id)

      person.parents = [i for i in person.parents if i not in ids]
      person.spouses = [i for i in person.spouses if i not in ids]
      person.children = [i for i in person.children if i not in ids]
    
    for person in self.members.values():
      self.n_descendants[person.id] = self.__count_n_descendants(person)

  def to_df(self) -> pd.DataFrame:
    """
    Convert the list of members of the family as a Pandas dataframe with the properties of a Person as columns.
    
    Returns:
      pd.DataFrame: the list of members as a dataframe.
    """
    return pd.DataFrame([vars(x) for x in self.members.values()])
