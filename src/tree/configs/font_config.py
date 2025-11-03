from pydantic import BaseModel


class FontConfig(BaseModel):
  fontcolor: str = "black"
  fontname: str = "Times-Roman"
  fontsize: float = 12