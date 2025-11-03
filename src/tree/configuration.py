from pydantic import BaseModel

from src.tree.configs.edge_config import EdgeConfig
from src.tree.configs.node_config import NodeConfig
from src.tree.configs.person_label_config import PersonLabelConfig
from src.tree.configs.title_config import TitleConfig
from src.tree.configs.trim_config import TrimConfig
from src.utils import read_file_as_dict

class TreeConfiguration(BaseModel):
  background_color: str = ""
  edge_config: EdgeConfig = EdgeConfig()
  filename: str = "family_tree.png"
  node_config: NodeConfig = NodeConfig()
  person_label_config: PersonLabelConfig = PersonLabelConfig()
  title_config: TitleConfig = TitleConfig()
  trim_config: TrimConfig = TrimConfig()
  start_person: str | None = None
  
  @classmethod
  def from_dict(cls, dict_config: dict):
    return cls(**dict_config)

  @classmethod
  def from_path(cls, path: str | None):
    if path is None: dict_config = {}
    else:
      dict_config = read_file_as_dict(path)
    
    return cls.from_dict(dict_config)