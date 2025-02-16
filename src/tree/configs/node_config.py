from src.tree.configs.font_config import FontConfig

class NodeStyle(FontConfig):
  def __init__(self,
    id: str = "",
    color: str = "black",
    fillcolor: str = "white",
    height: str = "",
    imagepos: str = "tc",
    labelloc: str = "",
    shape: str = "box",
    style: str = "filled",
    **kwargs
  ):
    self.id = id

    self.color = color
    self.fillcolor = fillcolor
    self.height = height
    self.imagepos = imagepos
    self.labelloc = labelloc
    self.shape = shape
    self.style = style

    super().__init__(**kwargs)

class ConditionalNodeStyle():
  def __init__(self,
    key: str = "",
    value: str = "",
    operator: str = "==",
    **kwargs
  ):
    self.key = key
    self.value = value
    self.operator = operator

    self.style_args = {**kwargs}

class NodeConfig(NodeStyle):
  def __init__(self,
    conditional_nodes: list[dict] = [],
    nodes: list[dict] = [],
    **kwargs
  ):
    super().__init__(**kwargs)

    self.nodes = {}
    for node in nodes:
      node_style = {**kwargs, **node}
      key = node.get("id")
      self.nodes[key] = NodeStyle(**node_style)

    self.conditional_nodes = []
    for conditional_node in conditional_nodes:
      self.conditional_nodes.append(ConditionalNodeStyle(**conditional_node))
    