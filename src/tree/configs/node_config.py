from pydantic import BaseModel

from src.tree.configs.font_config import FontConfig


class NodeStyle(FontConfig):
  id: str = ""
  color: str = "black"
  fillcolor: str = "white"
  height: str = ""
  imagepos: str = "tc"
  labelloc: str = ""
  shape: str = "box"
  style: str = "filled"

class ConditionalNodeStyle(BaseModel):
  key: str = ""
  value: str = ""
  operator: str = "=="
  style_args: dict = {}

  def __init__(self,
    **kwargs
  ):
    super().__init__(**kwargs)
    self.style_args = {**kwargs}

class NodeConfig(NodeStyle):
  nodes: dict[str, NodeStyle] = {}
  conditional_nodes: list[ConditionalNodeStyle] = []

  def __init__(self,
    conditional_nodes: list[dict] = [],
    nodes: list[dict] = [],
    **kwargs
  ):
    super().__init__(**kwargs)

    for node in nodes:
      # Check that the node has an id
      if "id" not in node: continue
      key = node["id"]
      node_style = {**kwargs, **node}
      self.nodes[key] = NodeStyle(**node_style)

    for conditional_node in conditional_nodes:
      self.conditional_nodes.append(ConditionalNodeStyle(**conditional_node))
    