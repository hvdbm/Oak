import pycountry

from src.person import Person
from src.tree.label import bold, newline

class PersonLabelConfig():
  def __init__(self,
    bold_names: bool = True,
    show_nationalities: bool = True,
    show_nickname: bool = True,
    split_names: bool = False,
    upper_last_name: bool = False
  ):
    self.bold_names = bold_names
    self.show_nationalities = show_nationalities
    self.show_nickname = show_nickname
    self.split_names = split_names
    self.upper_last_name = upper_last_name

  def get_names_label(self, person: Person) -> str:
    """
    Get the complete name (first name and last name) of a person.

    Parameters:
      person (Person): the person to get the name from.

    Returns:
      str: the complete name of a person.
    """
    names = person.first_name
    
    if self.split_names: names += newline()
    
    last_name = person.last_name.upper() if self.upper_last_name else person.last_name
    names += f" {last_name}"

    if person.suffix != None: names += f" {person.suffix}"

    if self.bold_names: names = bold(names)

    return names
  
  def get_nationalities_label(self, person: Person) -> str:
    """
    Get the list of nationalities of a person.
    
    Parameters:
      person (Person): the person to get the nationalities from.

    Returns:
      str: the nationalities of a person.
    """
    if person.nationalities == []: return ""

    flags = [pycountry.countries.get(alpha_2=n).flag for n in person.nationalities]
    
    return f"{newline()}{" ".join(flags)}"
  
  def get_label(self, person: Person) -> str:
    """
    Get the label (names, nickname, birth/death years and nationalities) of a person.
    
    Parameters:
      person (Person): the person to get the label from.

    Returns:
      str: the label with all the infos of a person.
    """
    names = self.get_names_label(person)

    nickname = f'"{person.nickname}"{newline()}' if self.show_nickname and person.nickname != None else ""
    death_year = f" - {person.death_year}" if person.death_year != None else ""
    nationalities = self.get_nationalities_label(person)

    return f"<{names}{newline()}{nickname}{person.birth_year}{death_year}{nationalities}>"