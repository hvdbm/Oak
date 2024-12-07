import json

import pandas as pd

from src.tree_config.configuration import TreeConfiguration
from src.person import Person
from src.draw import draw_tree

class Family():
  def __init__(self,
    name: str = "",
    members: dict[str, Person] = {}
  ):
    self.name = name
    self.members = members

    for value in members.values():
      value.n_descendants = self.find_n_descendants(value)

  @classmethod
  def from_path(cls, path: str):
    with open(path, 'r') as file:
      family = json.load(file)
      members_dict = {}
      for m in family["members"]:
        person = Person(**m)
        members_dict[person.id] = person

    family["members"] = members_dict
    
    return cls(**family)
    
  def find_n_descendants(self, person: Person) -> int:
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

  def draw_family_tree(self,
    config: TreeConfiguration,
    output_file_path: str
  ) -> None:
    persons = list(self.members.values())
    persons.sort(key=lambda x : x.n_descendants)
    persons.reverse()

    draw_tree(persons, self.name, config, output_file_path, self.members)
