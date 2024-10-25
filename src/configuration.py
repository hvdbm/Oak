import yaml

class TitleConfig():
  def __init__(self,
    title: str = "",
    font_size: float = 20,
    location: str = "t"
  ):
    self.title = title
    self.font_size = font_size
    self.location = location

class PersonLabelConfig():
  def __init__(self,
    show_nationalities: bool = False,
    show_nickname: bool = True,
    upper_last_name: bool = False
  ):
    self.show_nationalities = show_nationalities
    self.show_nickname = show_nickname
    self.upper_last_name = upper_last_name

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

def dict_key_as_object(dict_config: dict, key: str, c):
  if key in dict_config.keys():
    dict_config[key] = c(**dict_config.get(key))