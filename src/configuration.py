import yaml

class PersonLabelOptions():
  def __init__(self,
    show_nickname: bool = True,
    uppercase_last_name: bool = False
  ):
    self.show_nickname = show_nickname
    self.uppercase_last_name = uppercase_last_name

class Configuration():
  def __init__(self,
    label_options: PersonLabelOptions,
    filename: str = "family_tree.png",
    node_shape: str = "box",
    graph_title: str = "",
  ):
    self.label_options = label_options
    self.filename = filename
    self.node_shape = node_shape
    self.graph_title = graph_title
  
  @classmethod
  def from_path(cls, path: str):
    with open(path, 'r') as file:
      dict_config = yaml.safe_load(file)
      dict_config["label_options"] = PersonLabelOptions(**dict_config.get("label_options", {}))
      return cls(**dict_config)
