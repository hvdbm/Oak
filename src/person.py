class Person():
  def __init__(self,
    first_name: str,
    last_name: str,
    sex: str,
    birth_year: str,
    parents: list[str],
    spouses: list[str],
    childrens: list[str],
    id: str | None = None,
    death_year: str | None = None,
    nickname: str | None = None,
  ):
    self.id = id if id != None else f"{first_name} {last_name} ({birth_year})"

    self.first_name = first_name
    self.last_name = last_name
    self.sex = sex
    self.birth_year = birth_year
    self.death_year = death_year
    self.nickname = nickname

    # Relationships
    self.parents = parents
    self.spouses = spouses
    self.childrens = childrens

    # Calculated properties
    self.n_ancestors = None
  
  @classmethod
  def from_obj(cls, obj):
    return cls(
      id=obj.get("id", None),
      first_name=obj["first_name"],
      last_name=obj["last_name"],
      sex=obj["sex"],
      birth_year=obj["birth_year"],
      death_year=obj.get("death_year", None),
      parents=obj["parents"],
      spouses=obj["spouses"],
      childrens=obj["childrens"],
      nickname=obj.get("nickname", None),
    )

  def get_label(self, show_nickname=False):
    label = f"{self.first_name} {self.last_name} \n"
    if show_nickname and self.nickname != None: label += f'"{self.nickname}" \n'
    label += f"{self.birth_year}"
    if self.death_year != None: label += f" - {self.death_year}"

    return label