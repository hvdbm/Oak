class NodeStyleConfig():
  def __init__(self,
    color_by: str | None = None,
    color_by_dict: dict = {},
    default_color: str = "white", # https://graphviz.org/doc/info/colors.html
    font: str = "Times-Roman",
    font_size: float = 14.0,
    shape: str = "box",
    style: str = "filled"
  ):
    self.color_by = color_by
    self.color_by_dict = color_by_dict

    self.font = font
    self.font_size = font_size
    self.default_color = default_color
    self.shape = shape
    self.style = style