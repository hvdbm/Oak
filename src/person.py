import pycountry

from src.tree.person_label_config import PersonLabelConfig
from src.label import bold, newline

class Person():
  def __init__(self,
    first_name: str,
    last_name: str,
    sex: str,
    birth_year: str,
    parents: list[str] = [],
    spouses: list[str] = [],
    childrens: list[str] = [],
    id: str | None = None,
    death_year: str | None = None,
    nickname: str | None = None,
    nationalities: list[str] = [],
  ):
    self.id = id if id != None else f"{first_name} {last_name} ({birth_year})"

    self.first_name = first_name
    self.last_name = last_name
    self.sex = sex
    self.birth_year = birth_year
    self.death_year = death_year
    self.nickname = nickname
    self.nationalities = nationalities

    # Relationships
    self.parents = parents
    self.spouses = spouses
    self.childrens = childrens

    # Calculated properties
    self.n_descendants = None

  def get_names_label(self, config: PersonLabelConfig) -> str:
    """
    Get the complete name (first name and last name) of a person.

    Parameters:
      config (PersonLabelConfig): configuration on how to process the different names parts.

    Returns:
      str: the complete name of a person.
    """
    names = self.first_name
    
    if config.split_names: names += newline()
    
    last_name = self.last_name.upper() if config.upper_last_name else self.last_name
    names += " " + last_name

    if config.bold_names: names = bold(names)

    return names

  def get_label(self, config: PersonLabelConfig) -> str:
    """
    Get the label (names, nickname, birth/death years and nationalities) of a person.
    
    Parameters:
      config (PersonLabelConfig): configuration on how to process the different label parts.

    Returns:
      str: the label with all the infos of a person.
    """
    names = self.get_names_label(config)

    nickname = f'"{self.nickname}" {newline()}' if config.show_nickname and self.nickname != None else ""
    death_year = f"- {self.death_year}" if self.death_year != None else ""
    nationalities = f"{newline()} {"  ".join([pycountry.countries.get(alpha_2=n).flag for n in self.nationalities])}" if self.nationalities != None and self.nationalities != [] and config.show_nationalities else ""

    return f"<{names} {newline()} {nickname} {self.birth_year} {death_year} {nationalities}>"
