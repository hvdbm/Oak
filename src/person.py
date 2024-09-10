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
  ):
    self.id = id if id != None else f"{first_name} {last_name} ({birth_year})"

    self.first_name = first_name
    self.last_name = last_name
    self.sex = sex
    self.birth_year = birth_year
    self.death_year = death_year
    self.parents = parents
    self.spouses = spouses
    self.childrens = childrens
  
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
    )

  def get_label(self):
    full_name = f"{self.first_name} {self.last_name}"
    death = f" - {self.death_year}" if self.death_year != None else ""

    return f"{full_name} \n {self.birth_year}{death}"