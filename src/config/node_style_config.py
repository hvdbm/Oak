class NodeStyleConfig():
  def __init__(self,
    color_by: str | None = None,
    color_by_dict: dict = {},
    default_color: str = "white", # https://graphviz.org/doc/info/colors.html
    shape: str = "box",
    style: str = "filled"
  ):
    self.color_by = color_by
    self.color_by_dict = color_by_dict

    self.default_color = default_color
    self.shape = shape
    self.style = style