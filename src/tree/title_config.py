from src.tree.font_config import FontConfig

class TitleConfig(FontConfig):
  def __init__(self,
    location: str = "t",
    font: str | None = None,
    font_size: float | None = None,
    font_color: str | None = None
  ):
    self.location = location

    FontConfig.__init__(self, font, font_size, font_color)