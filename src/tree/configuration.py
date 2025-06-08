from src.utils import dict_key_as_object, read_file_as_dict
from src.tree.configs.edge_config import EdgeConfig
from src.tree.configs.node_config import NodeConfig
from src.tree.configs.person_label_config import PersonLabelConfig
from src.tree.configs.title_config import TitleConfig

class TreeConfiguration():
  def __init__(self,
    background_color: str = "",
    edge_config: EdgeConfig = EdgeConfig(**{}),
    filename: str = "family_tree.png",
    node_config: NodeConfig = NodeConfig(**{}),
    person_label_config: PersonLabelConfig = PersonLabelConfig(**{}),
    title_config: TitleConfig = TitleConfig(**{}),
    ignore: list[str] = [],
    start_person: str | None = None,
  ):
    self.background_color = background_color
    self.edge_config = edge_config
    self.filename = filename
    self.node_config = node_config
    self.person_label_config = person_label_config
    self.title_config = title_config
    self.ignore = ignore
    self.start_person = start_person
  
  @classmethod
  def from_path(cls, path: str | None):
    if path is None: dict_config = {}
    else:
      dict_config = read_file_as_dict(path)
    
    dict_key_as_object(dict_config, "edge_config", EdgeConfig)
    dict_key_as_object(dict_config, "node_config", NodeConfig)
    dict_key_as_object(dict_config, "person_label_config", PersonLabelConfig)
    dict_key_as_object(dict_config, "title_config", TitleConfig)
    
    return cls(**dict_config)
