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

  def get_label(self, label: str | None = None) -> str:
    if not self.enabled: return ""
    if self.title is None and label is None: return ""

    # Override the label if a title is provided
    text = self.title if self.title is not None else label
    if text is None: return ""

    return f"<{bold(text)} {newline()} >"
