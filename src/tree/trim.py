from src.family import Family
from src.tree.configs.trim_config import TrimConfig

def keep_only_descendants(family: Family, descendants_of: str) -> None:
  """
  Remove the persons which are not the descendants of the specified id "descendants_of". 

  Paremeters:
    family (Family): the family object with all the persons.
    descendants_of (str): the ID of the persons to keep the descendants.

  Returns:
    None
  """

  descendants, spouses = family.get_descendants(descendants_of, True)
  new_family_ids = descendants + spouses + [descendants_of] + family.members[descendants_of].spouses
  ids_to_remove = set(family.members.keys()).difference(new_family_ids)
  family.remove_persons(ids_to_remove)

def trim(family: Family, config: TrimConfig) -> None:
  """
  Trim the family tree.
  
  Parameters:
    family (Family): the family object with all the persons.
    config (TrimConfig): the trim configuration to remove unwanted persons.
  
  Returns:
    None
  """
  # Remove ignored persons
  family.remove_persons(config.ignore)

  # Keep only descendants if specified
  if config.descendants_of is not None: keep_only_descendants(family, config.descendants_of)
