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
      key = (edge.get("start_node"), edge.get("end_node"))
      self.edges[key] = EdgeStyle(**edge_style)

