from src.family import Family


def count_ancestors(n_generations: int) -> int:
  """
  Calculate the number of ancestors for a given number of generations.

  Parameters:
    n_generations (int): The number of generations.

  Returns:
    int: The number of ancestors.
  """
  total = 0
  for i in range(n_generations):
    if i == 0: total = 2
    else: total += pow(2, i + 1)
  return total

def get_ancestors_sunburst_data(
    family: Family,
    person_id: str,
    persons: list[str] = [],
    parents: list[str] = [],
    depth_dict: dict[str, int] = {},
) -> tuple[list[str], list[str], dict[str, int]]:
    """
    Get the sunburst data (ids, parents, depths) for the ancestors of a person recursively.

    Parameters:
        family (Family): The family object.
        person_id (str): The id of the person to get the ancestors for. Default to an empty list.
        persons (list[str]): List of the persons to plot. Default to an empty list.
        parents (list[str]): List of the parent of each persons. Default to an empty dict.
        depth_dict (dict[str, int]): A dictionary to store the depth of each person.

    Returns:
        tuple[list[str], list[str], dict[str]]: A tuple containing the list of person ids,
        the list of parent ids, and the depth dictionary.
    """
    if person_id not in family.members: return persons, parents, depth_dict
    
    person_data = family.members[person_id]

    for parent_id in person_data.parents:
        if parent_id not in family.members: continue

        # Add ancestor
        persons.append(parent_id)
        parents.append(person_id)

        # Update depth
        max_depth = 0
        for child in family.members[parent_id].childrens:
            if child in depth_dict: 
                max_depth = max(max_depth, depth_dict[child]+1)
        depth_dict[parent_id] = max_depth

        _, _, _ = get_ancestors_sunburst_data(family, parent_id, persons, parents, depth_dict)
 
    return persons, parents, depth_dict