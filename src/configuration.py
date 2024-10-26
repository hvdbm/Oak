import yaml

from src.config.title_config import TitleConfig
from src.config.person_label_config import PersonLabelConfig
from src.utils import dict_key_as_object

class Configuration():
  def __init__(self,
    filename: str = "family_tree.png",
    node_shape: str = "box",
    title_config: TitleConfig = TitleConfig(**{}),
    person_label_config: PersonLabelConfig = PersonLabelConfig(**{}),
  ):
    self.filename = filename
    self.node_shape = node_shape
    self.title_config = title_config
    self.person_label_config = person_label_config
  
  @classmethod
  def from_path(cls, path: str | None):
    dict_config = {}
    
    if path is not None:
      with open(path, 'r') as file:
        dict_config = yaml.safe_load(file)

    dict_key_as_object(dict_config, "title_config", TitleConfig)
    dict_key_as_object(dict_config, "person_label_config", PersonLabelConfig)
    
    return cls(**dict_config)
