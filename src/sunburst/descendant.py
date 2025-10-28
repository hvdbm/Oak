from src.family import Family

def get_descendants_sunburst_data(
    family: Family,
    person_id: str,
    persons: list[str] = [],
    parents: list[str] = [],
    split_dict: dict[str, float] = {}
) -> tuple[list[str], list[str], dict[str, float]]:

    # TODO : throw an error ?
    if person_id not in family.members: return persons, parents, split_dict

    person_data = family.members[person_id]

    for child_id in person_data.childrens:
        if child_id not in family.members: continue
        # Add descendant
        persons.append(child_id)
        parents.append(person_id)

        split_dict[child_id] = split_dict.get(person_id, 1) / len(person_data.childrens)

        _, _, _ = get_descendants_sunburst_data(family, child_id, persons, parents, split_dict)
    
    return persons, parents, split_dict