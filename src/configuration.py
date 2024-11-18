import yaml

from src.tree_config.node_style_config import NodeStyleConfig
from src.tree_config.person_label_config import PersonLabelConfig
from src.tree_config.title_config import TitleConfig
from src.utils import dict_key_as_object

class Configuration():
  def __init__(self,
    background_color: str = "",
    edge_color: str = "",
    filename: str = "family_tree.png",
    node_style_config: NodeStyleConfig = NodeStyleConfig(**{}),
    person_label_config: PersonLabelConfig = PersonLabelConfig(**{}),
    title_config: TitleConfig = TitleConfig(**{}),
  ):
    self.background_color = background_color
    self.edge_color = edge_color
    self.filename = filename
    self.node_style_config = node_style_config
    self.person_label_config = person_label_config
    self.title_config = title_config
  
  @classmethod
  def from_path(cls, path: str | None):
    if path is None: dict_config = {}
    else:
      with open(path, 'r') as file:
        dict_config = yaml.safe_load(file)

    dict_key_as_object(dict_config, "node_style_config", NodeStyleConfig)
    dict_key_as_object(dict_config, "person_label_config", PersonLabelConfig)
    dict_key_as_object(dict_config, "title_config", TitleConfig)
    
    return cls(**dict_config)
