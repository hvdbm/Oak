from src.family import Family

def get_descendants_sunburst_data(
    family: Family,
    person_id: str,
    persons: list[str] = [],
    parents: list[str] = [],
    repartition_dict: dict[str, float] = {}
) -> tuple[list[str], list[str], dict[str, float]]:
    """
    Get the sunburst data (ids, parents, values) for the descendants of a person recursively.

    Parameters:
        family (Family): The family object.
        person_id (str): The id of the person to get the descendants for. Default to an empty list.
        persons (list[str]): List of the persons to plot. Default to an empty list.
        parents (list[str]): List of the parent of each persons. Default to an empty dict.
        repartition_dict (dict[str, float]): A dictionary to store the % of the size of the sector of a person.
    """

    # TODO : throw an error ?
    if person_id not in family.members: return persons, parents, repartition_dict

    person_data = family.members[person_id]

    for child_id in person_data.childrens:
        if child_id not in family.members: continue
        # Add descendant
        persons.append(child_id)
        parents.append(person_id)

        repartition_dict[child_id] = repartition_dict.get(person_id, 1) / len(person_data.childrens)

        _, _, _ = get_descendants_sunburst_data(family, child_id, persons, parents, repartition_dict)
    
    return persons, parents, repartition_dict