class EdgeStyle():
  def __init__(self,
    color: str = "black",
    dir: str = "none",
    minlen: int = 1,
    penwidth: float = 1.0,
    style: str = "solid",
    start_node: str = "",
    end_node: str = "",
  ):
    # Style
    self.color = color
    self.dir = dir
    self.minlen = minlen
    self.penwidth = penwidth
    self.style = style

    # Position
    self.start_node = start_node
    self.end_node = end_node

class EdgeConfig(EdgeStyle):
  def __init__(self,
    edges: list[dict] = [],
    **kwargs
  ):
    super().__init__(**kwargs)

    self.edges = {}

    for edge in edges:
      edge_style = {**kwargs, **edge}
      key = (edge.get("start_node"), edge.get("end_node"))
      self.edges[key] = EdgeStyle(**edge_style)

