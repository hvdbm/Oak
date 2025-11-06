from src.family import Family
from src.tree.configs.trim_config import (AncestorsOfConfig,
                                          DescendantsOfConfig, TrimConfig)


def keep_only_ancestors(family: Family, config: AncestorsOfConfig) -> None:
  """
  Remove the persons which are not the ancestors of the person specified in the config.

  Paremeters:
    family (Family): the family object with all the persons.
    config (AncestorsOfConfig): the config of the persons to keep the ancestors.

  Returns:
    None
  """
  ancestors = family.get_ancestors(config.of)
  new_family_ids = ancestors + [config.of]
  ids_to_remove = set(family.members.keys()).difference(new_family_ids)
  family.remove_persons(ids_to_remove)

def keep_only_descendants(family: Family, config: DescendantsOfConfig) -> None:
  """
  Remove the persons which are not the descendants of the person specified in the config.

  Paremeters:
    family (Family): the family object with all the persons.
    config (DescendantsOfConfig): the config of the persons to keep the descendants.

  Returns:
    None
  """
  descendants, spouses = family.get_descendants(config.of, config.include_spouses)
  new_family_ids = descendants + spouses + [config.of] + family.members[config.of].spouses
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

  # Keep only ancestors if specified
  if config.ancestors_of is not None: keep_only_ancestors(family, config.ancestors_of)

  # Keep only descendants if specified
  if config.descendants_of is not None: keep_only_descendants(family, config.descendants_of)
