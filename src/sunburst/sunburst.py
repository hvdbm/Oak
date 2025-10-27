import os

import plotly.graph_objects as go

from src.family import Family


def get_ancestors_sunburst_data(
    family: Family,
    person_id: str,
    depth_dict: dict[str] = {}
) -> tuple[list[str], list[str], dict[str]]:
    persons, parents = [], []

    if person_id not in family.members: return persons, parents, depth_dict
    
    person_data = family.members[person_id]
    
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

def write_image(fig: go.Figure, output_dir: str | None, output_filename: str, output_format: str) -> None:
    if output_dir is None: return

    if not os.path.exists(output_dir): os.makedirs(output_dir)
    full_output_path = os.path.join(output_dir, f"{output_filename}.{output_format}")

    if output_format in ["png", "jpg", "jpeg", "webp", "svg", "pdf"]:
        fig.write_image(full_output_path)
    elif output_format == "html":
        fig.write_html(full_output_path, auto_open=False)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

def draw_sunburst(
    family: Family,
    person_id: str,
    output_dir: str | None,
    output_filename: str,
    output_format: str,
    max_depth: int,
    no_interactive: bool,
    weighted: bool
) -> None:
    persons, parents, depth_dict = get_ancestors_sunburst_data(family, person_id)
    max_depth_dict = max(depth_dict.values()) if len(depth_dict) > 0 else 0

    fig = go.Figure(go.Sunburst(
        ids=persons,
        labels=[family.members[person].full_name() for person in persons],
        parents=parents,
        values=[pow(2, max_depth_dict - depth_dict.get(person, 0)) for person in persons] if weighted else None,
        branchvalues="total",
        maxdepth=max_depth,
    ))

    fig.update_layout(
        title_text=f"Ancestors of {family.members[person_id].full_name()}",
        title_subtitle_text=f"{len(persons)-1} ancestors found on {pow(2, max_depth_dict)} possible ancestors"
    )

    if not no_interactive: fig.show()

    write_image(fig, output_dir, output_filename, output_format)
