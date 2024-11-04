def dict_key_as_object(dict_config: dict, key: str, c):
  if key in dict_config.keys():
    dict_config[key] = c(**dict_config.get(key))

def get_union_name(parents):
  if len(parents) == 1:
     parents.append("???")
  try :
    sorted_id = sorted(parents)
    return f"{sorted_id[0]} & {sorted_id[1]}"
  except:
     print(parents)