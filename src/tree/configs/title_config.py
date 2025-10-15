from src.tree.configs.font_config import FontConfig
from src.tree.label import bold, newline


class TitleConfig(FontConfig):
  def __init__(self,
    enabled: bool = True,
    location: str = "t",
    title: str | None = None,
    **kwargs
  ):
    self.enabled = enabled
    self.location = location
    self.title = title

    FontConfig.__init__(self, **kwargs)

  def get_label(self) -> str:
    if not self.enabled: return ""
    if self.title is None: return ""

    return f"<{bold(self.title)} {newline()} >"
