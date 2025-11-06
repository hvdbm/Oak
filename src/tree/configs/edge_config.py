from pydantic import BaseModel


class EdgeStyle(BaseModel):
  color: str = "black"
  dir: str = "none"
  minlen: int = 1
  penwidth: float = 1.0
  style: str = "solid"
  start_node: str = ""
  end_node: str = ""

class EdgeConfig(EdgeStyle):
  edges: dict[tuple[str, str], EdgeStyle] = {}
  
  def __init__(self,
    edges: list[dict] = [],
    **kwargs
  ):
    super().__init__(**kwargs)

    for edge in edges:
      edge_style = {**kwargs, **edge}
      if "start_node" not in edge or "end_node" not in edge:
        continue
      key = (edge["start_node"], edge["end_node"])
      self.edges[key] = EdgeStyle(**edge_style)

