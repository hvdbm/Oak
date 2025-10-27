# import plotly.express as px
import plotly.graph_objects as go

from src.family import Family


def get_ancestors_sunburst_data(
    family: Family,
    person_id: str,
    depth_dict: dict[str] = {}
) -> tuple[list[str], list[str], dict[str]]:    # Persons, Parents of persons, Depths
    if person_id not in family.members: return [], [], {}
    
    person_data = family.members[person_id]
    persons, parents = [], []

    if len(person_data.childrens) == 0:
        persons.append(person_id)
        parents.append("")
        depth_dict[person_id] = 0

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

        sub_persons, sub_parents, _ = get_ancestors_sunburst_data(family, parent_id, depth_dict)
        persons += sub_persons
        parents += sub_parents

    return persons, parents, depth_dict
    

def draw_sunburst(family: Family, person_id: str, max_depth: int, output_file_path: str) -> None:
    persons, parents, depth_dict = get_ancestors_sunburst_data(family, person_id)

    max_depth_dict = max(depth_dict.values()) if len(depth_dict) > 0 else 0

    fig = go.Figure(go.Sunburst(
        labels=persons,
        parents=parents,
        values=[pow(2, max_depth_dict - depth_dict.get(person, 0)) for person in persons],
        branchvalues="total",
        maxdepth=max_depth
    ))

    fig.show()

    # fig.write_html(f"{output_file_path}/first_figure.html", auto_open=True)
