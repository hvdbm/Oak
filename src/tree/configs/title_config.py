from src.tree.configs.font_config import FontConfig

class TitleConfig(FontConfig):
  def __init__(self, location: str = "t", **kwargs):
    self.location = location

    FontConfig.__init__(self, **kwargs)