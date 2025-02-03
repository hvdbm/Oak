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
    image: str = "",
    suffix: str | None = None
  ):
    self.id = id if id != None else f"{first_name} {last_name} ({birth_year})"

    self.first_name = first_name
    self.last_name = last_name
    self.sex = sex
    self.birth_year = birth_year
    self.death_year = death_year
    self.nickname = nickname
    self.nationalities = nationalities
    self.image = image
    self.suffix = suffix

    # Relationships
    self.parents = parents
    self.spouses = spouses
    self.childrens = childrens

    # Calculated properties
    self.n_descendants = None
