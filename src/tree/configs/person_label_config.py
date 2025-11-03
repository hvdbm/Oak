import pycountry
from pydantic import BaseModel

from src.person import Person
from src.tree.label import bold, newline


class PersonLabelConfig(BaseModel):
  bold_names: bool = True
  show_nationalities: bool = True
  show_nickname: bool = True
  show_years: bool = True
  split_names: bool = False
  upper_last_name: bool = False  

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

    if person.suffix is not None: names += f" {person.suffix}"

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
    if not self.show_nationalities or person.nationalities == []: return ""

    flags = [pycountry.countries.get(alpha_2=n).flag for n in person.nationalities]
    
    return f"{newline()}{" ".join(flags)}"
  
  def get_years_label(self, person: Person) -> str:
    if not self.show_years: return ""

    death_year = f" - {person.death_year}" if person.death_year is not None else ""
    return f"{newline()}{person.birth_year}{death_year}"

  def get_label(self, person: Person) -> str:
    """
    Get the label (names, nickname, birth/death years and nationalities) of a person.
    
    Parameters:
      person (Person): the person to get the label from.

    Returns:
      str: the label with all the infos of a person.
    """
    names = self.get_names_label(person)

    nickname = f'{newline()}"{person.nickname}"' if self.show_nickname and person.nickname is not None else ""
    years = self.get_years_label(person)
    nationalities = self.get_nationalities_label(person)

    return f"<{names}{nickname}{years}{nationalities}>"