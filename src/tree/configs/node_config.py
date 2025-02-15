from src.tree.configs.font_config import FontConfig

class NodeStyle():
  def __init__(self,
    id: str = "",
    color: str = "black",
    fillcolor: str = "white",
    imagepos: str = "tc",
    labelloc: str = "",
    shape: str = "box",
    style: str = "filled",
    **kwargs
  ):
    self.id = id

    self.color = color
    self.fillcolor = fillcolor
    self.imagepos = imagepos
    self.labelloc = labelloc
    self.shape = shape
    self.style = style

    for key, value in kwargs.items():
      print(f"NodeStyle : unknown key: {key}, value: {value}")

class NodeConfig(NodeStyle):
  def __init__(self,
    nodes: list[dict] = [],
    **kwargs
  ):
    super().__init__(**kwargs)

    self.nodes = {}

    for node in nodes:
      node_style = {**kwargs, **node}
      key = node.get("id")
      self.nodes[key] = NodeStyle(**node_style)

# class NodeConfig(FontConfig):
#   def __init__(self,
#     color_by: str | None = None,
#     color_by_dict: dict = {},
#     default_color: str = "white", # https://graphviz.org/doc/info/colors.html
#     height_w_img: str = "",
#     imagepos: str = "tc",
#     labelloc: str = "",
#     shape: str = "box",
#     style: str = "filled",
#     **kwargs
#   ):
#     self.color_by = color_by
#     self.color_by_dict = color_by_dict
#     self.default_color = default_color
#     self.height_w_img = height_w_img
#     self.imagepos = imagepos
#     self.labelloc = labelloc
#     self.shape = shape
#     self.style = style

#     super().__init__(self, **kwargs)
  
    