from src.tree.configs.edge_config import EdgeConfig
from src.tree.configs.node_config import NodeConfig
from src.tree.configs.person_label_config import PersonLabelConfig
from src.tree.configs.title_config import TitleConfig
from src.tree.configs.trim_config import TrimConfig
from src.utils import dict_key_as_object, read_file_as_dict


class TreeConfiguration():
  def __init__(self,
    background_color: str = "",
    edge_config: EdgeConfig = EdgeConfig(**{}),
    filename: str = "family_tree.png",
    node_config: NodeConfig = NodeConfig(**{}),
    person_label_config: PersonLabelConfig = PersonLabelConfig(**{}),
    title_config: TitleConfig = TitleConfig(**{}),
    start_person: str | None = None,
    trim_config: TrimConfig = TrimConfig(**{})
  ):
    self.background_color = background_color
    self.edge_config = edge_config
    self.filename = filename
    self.node_config = node_config
    self.person_label_config = person_label_config
    self.title_config = title_config
    self.start_person = start_person
    self.trim_config = trim_config
  
  @classmethod
  def from_path(cls, path: str | None):
    if path is None: dict_config = {}
    else:
      dict_config = read_file_as_dict(path)
    
    dict_key_as_object(dict_config, "edge_config", EdgeConfig)
    dict_key_as_object(dict_config, "node_config", NodeConfig)
    dict_key_as_object(dict_config, "person_label_config", PersonLabelConfig)
    dict_key_as_object(dict_config, "title_config", TitleConfig)
    dict_key_as_object(dict_config, "trim_config", TrimConfig)
    
    return cls(**dict_config)
