from pydantic import BaseModel


class AncestorsOfConfig(BaseModel):
  of: str

class DescendantsOfConfig(BaseModel):
  of: str
  include_spouses: bool = True

class TrimConfig(BaseModel):
  ancestors_of: AncestorsOfConfig | None = None
  descendants_of: DescendantsOfConfig | None = None
  ignore: list[str] = []
  ignore_incomplete_relations: bool = False
