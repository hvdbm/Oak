
import json

from src.configuration import Configuration
from src.person import Person
from src.draw import draw_tree

class Family():
  def __init__(self,
    name: str = "",
    members: dict[str, Person] = {}
  ):
    self.name = name
    self.members = members

    for _, value in members.items():
      value.n_ancestors = self.find_n_ancestors(value)

  def find_n_ancestors(self, person: Person) -> int:
    if person.parents == []: return 0
    if person.n_ancestors != None: return person.n_ancestors
    
    n = 1
    for parent in person.parents:
      if parent not in self.members.keys(): continue
      n += self.find_n_ancestors(self.members[parent])
    
    return n

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
  
  def draw_family_tree(self,
    config: Configuration,
    output_file_path: str
  ) -> None:
    persons = list(self.members.values())
    persons.sort(key=lambda x: x.birth_year)
    persons.reverse()
    persons.sort(key=lambda x: x.n_ancestors)
    persons.reverse()

    draw_tree(persons, self.name, config, output_file_path)



