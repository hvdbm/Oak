from src.tree.configs.font_config import FontConfig

class NodeConfig(FontConfig):
  def __init__(self,
    color_by: str | None = None,
    color_by_dict: dict = {},
    default_color: str = "white", # https://graphviz.org/doc/info/colors.html
    shape: str = "box",
    style: str = "filled",
    font: str | None = None,
    font_size: float | None = None,
    font_color: str | None = None
  ):
    self.color_by = color_by
    self.color_by_dict = color_by_dict
    self.default_color = default_color
    self.shape = shape
    self.style = style

    FontConfig.__init__(self, font, font_size, font_color)
  
    