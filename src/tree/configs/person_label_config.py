import pycountry

from src.person import Person
from src.tree.label import bold, italic, newline

class LabelConfig():
  def __init__(self,
    enabled: bool = True,
    bold: bool = False,
    italic: bool = False,
    newline: bool = False
  ):
    self.enabled = enabled
    self.bold = bold
    self.italic = italic
    self.newline = newline

# class PersonLabelConfig2():
#   def __init__(self, transforms: dict[str, LabelConfig]):
#     self.transforms = transforms

#     # self.transforms.items()

#   def generate_str(self, text: str | list[str] , key: str) -> str:
#     config = self.transforms.get(key, LabelConfig())

#     if not config.enabled: return ""

#     # If the text is a list, join it with a space
#     if isinstance(text, list): text = " ".join(text)

#     if config.bold: text = bold(text)
#     if config.italic: text = italic(text)
#     if config.newline: text = newline(text)

#     return text
  
#   def get_names_label(self, person: Person):
#     person_dict = person.__dict__

#     names = ""

#     for key in ["first_name", "middle_names", "last_name", "suffix"]:
#       names += self.generate_str(person_dict[key], key)

#     return names

#   def get_nationalities_label(self, person: Person) -> str:
#     person_dict = person.__dict__

#     nationalities = self.generate_str(person_dict["nationalities"], "nationalities")

#     return nationalities

#   def get_label(self, person: Person) -> str:
#     get_names_label

class PersonLabelConfig():
  def __init__(self,
    bold_names: bool = True,
    show_nationalities: bool = True,
    show_nickname: bool = True,
    show_years: bool = True,
    split_names: bool = False,
    upper_last_name: bool = False
  ):
    self.bold_names = bold_names
    self.show_nationalities = show_nationalities
    self.show_nickname = show_nickname
    self.show_years = show_years
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
