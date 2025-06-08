import json
import yaml

ACCEPTED_EXTENSIONS = ["json", "yaml", "yml"]

def apply_dict(obj: dict, dict: dict) -> None:
  for key, value in dict.items():
    obj[key] = value

def dict_key_as_object(dict_config: dict, key: str, c) -> None:
  if key in dict_config:
    dict_config[key] = c(**dict_config.get(key))

def read_file_as_dict(file_path: str) -> dict:
  extentions = file_path.split(".")[-1]
    
  with open(file_path, 'r') as file:
    if extentions == "json": return json.load(file)
    elif extentions in ["yaml", "yml"]: return yaml.safe_load(file)
    else:
      raise Exception(f'File extension not supported: "{extentions}". Supported extensions: {ACCEPTED_EXTENSIONS}.')
