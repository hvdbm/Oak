import os

import plotly.graph_objects as go

from src.family import Family
from src.sunburst.ancestor import count_ancestors, get_ancestors_sunburst_data
from src.sunburst.descendant import get_descendants_sunburst_data


def write_image(fig: go.Figure, output_dir: str | None, output_filename: str, output_format: str) -> None:
    """
    Write the figure to an image file.

    Parameters:
      fig (go.Figure): The figure to write.
      output_dir (str | None): The output directory. If None, no file is saved.
      output_filename (str): The name of the output file.
      output_format (str): The format of the output file. Accepted formats: 'png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'html'.

    Returns:
        None
    """
    if output_dir is None: return

    if not os.path.exists(output_dir): os.makedirs(output_dir)
    full_output_path = os.path.join(output_dir, f"{output_filename}.{output_format}")

    if output_format in ["png", "jpg", "jpeg", "webp", "svg", "pdf"]:
        fig.write_image(full_output_path)
    elif output_format == "html":
        fig.write_html(full_output_path, auto_open=False)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

def generate_sunburst_config(
    type: str,
    family: Family,
    person_id: str,
    weighted: bool
):
    if type == "ancestors":
        persons, parents, depth_dict = get_ancestors_sunburst_data(family, person_id, [person_id], [""], {person_id: 0})

        # Values
        max_depth_dict = max(depth_dict.values()) if len(depth_dict) > 0 else 0
        values = [pow(2, max_depth_dict - depth_dict.get(person, 0)) for person in persons] if weighted else None
        
        # Layout field
        title = f"Ancestors of {family.members[person_id].full_name()}"
        subtitle = f"{len(persons)-1} ancestors found on {count_ancestors(max_depth_dict)} possible ancestors"

        return persons, parents, values, title, subtitle
    elif type == "descendants":
        persons, parents, split_dict = get_descendants_sunburst_data(family, person_id, [person_id], [""], {person_id: 1})
        
        # Values
        n_descendants = len(persons)-1
        values = [n_descendants * split_dict.get(person, 0) for person in persons] if weighted else None

        # Layout field
        title = f"Descendants of {family.members[person_id].full_name()}"
        subtitle = f"{n_descendants} descendants found"

        return persons, parents, values, title, subtitle
    else:
        raise ValueError(f"Unsupported sunburst type : {type}")

def draw_sunburst(
    family: Family,
    person_id: str,
    output_dir: str | None,
    output_filename: str,
    output_format: str,
    max_depth: int,
    no_interactive: bool,
    weighted: bool,
    type: str
) -> None:
    """
    Draw a sunburst chart of the ancestors of a person in the family.

    Parameters:
        family (Family): The family object.
        person_id (str): The id of the person to draw the sunburst for.
        output_dir (str | None): The output directory. If None, no file is saved.
        output_filename (str): The name of the output file.
        output_format (str): The format of the output file.
        max_depth (int): The maximum depth to display in the sunburst. -1 for no limit.
        no_interactive (bool): If True, do not show the interactive sunburst window.
        weighted (bool): If True, use the real number of ancestors as width for each sector.
        type (str): ...
    """
    ids, parents, values, title, subtitle = generate_sunburst_config(type, family, person_id, weighted)

    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=[family.members[person].full_name() for person in ids],
        parents=parents,
        values=values,
        branchvalues="total",
        maxdepth=max_depth,
    ))

    fig.update_layout(
        title_text=title,
        title_subtitle_text=subtitle
    )

    if not no_interactive: fig.show()

    write_image(fig, output_dir, output_filename, output_format)
