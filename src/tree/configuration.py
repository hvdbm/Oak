import yaml

from src.tree.edge_config import EdgeConfig
from src.tree.node_config import NodeConfig
from src.tree.person_label_config import PersonLabelConfig
from src.tree.title_config import TitleConfig
from src.utils import dict_key_as_object

class TreeConfiguration():
  def __init__(self,
    background_color: str = "",
    edge_config: EdgeConfig = EdgeConfig(**{}),
    filename: str = "family_tree.png",
    node_config: NodeConfig = NodeConfig(**{}),
    person_label_config: PersonLabelConfig = PersonLabelConfig(**{}),
    title_config: TitleConfig = TitleConfig(**{}),
  ):
    self.background_color = background_color
    self.edge_config = edge_config
    self.filename = filename
    self.node_config = node_config
    self.person_label_config = person_label_config
    self.title_config = title_config
  
  @classmethod
  def from_path(cls, path: str | None):
    if path is None: dict_config = {}
    else:
      with open(path, 'r') as file:
        dict_config = yaml.safe_load(file)

    dict_key_as_object(dict_config, "edge_config", EdgeConfig)
    dict_key_as_object(dict_config, "node_config", NodeConfig)
    dict_key_as_object(dict_config, "person_label_config", PersonLabelConfig)
    dict_key_as_object(dict_config, "title_config", TitleConfig)
    
    return cls(**dict_config)
