class TrimConfig():
  def __init__(self,
    ancestors_of: str | None = None,
    descendants_of: str | None = None,
    ignore: list[str] = [],
    ignore_incomplete_relations: bool = False
  ):
    self.ancestors_of = ancestors_of
    self.descendants_of = descendants_of
    self.ignore = ignore
    self.ignore_incomplete_relations = ignore_incomplete_relations