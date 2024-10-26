def dict_key_as_object(dict_config: dict, key: str, c):
  if key in dict_config.keys():
    dict_config[key] = c(**dict_config.get(key))