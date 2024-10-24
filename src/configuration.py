import yaml

class PersonLabelOptions():
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
    graph_title: str = "",
    label_options: PersonLabelOptions = PersonLabelOptions(**{}),
  ):
    self.filename = filename
    self.node_shape = node_shape
    self.graph_title = graph_title
    self.label_options = label_options
  
  @classmethod
  def from_path(cls, path: str | None):
    dict_config = {}
    
    if path is not None:
      with open(path, 'r') as file:
        dict_config = yaml.safe_load(file)
    
    dict_config["label_options"] = PersonLabelOptions(**dict_config.get("label_options", {}))
    return cls(**dict_config)
