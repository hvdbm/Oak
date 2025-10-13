class TrimConfig():
  def __init__(self,
    descendants_of: str | None = None,
    ignore: list[str] = [],
    ignore_incomplete_relations: bool = False
  ):
    self.descendants_of = descendants_of
    self.ignore = ignore
    self.ignore_incomplete_relations = ignore_incomplete_relations