
import pygraphviz as pgv

from src.configuration import Configuration, NodeStyleConfig
from src.label import bold, newline
from src.person import Person
from src.utils import get_union_name

def get_node_color(person: Person, node_style_config: NodeStyleConfig) -> str:
  if node_style_config.color_by is None : return node_style_config.default_color
  
  if node_style_config.color_by in person.__dict__.keys():
    value = person.__dict__.get(node_style_config.color_by)
    return node_style_config.color_by_dict.get(value, node_style_config.default_color)
  
  return node_style_config.default_color

def draw_tree(
  persons: list[Person],
  title: str, 
  config: Configuration,
  output_file_path: str
) -> None:
  G = pgv.AGraph(
    splines="ortho",
    bgcolor=config.background_color,
    label=f"<{bold(title)} {newline()} >",
    labelloc=config.title_config.location,
    fontname=config.title_config.font,
    fontsize=config.title_config.font_size
  )
  
  G.edge_attr['color'] = config.edge_color
  G.node_attr['shape'] = config.node_style_config.shape

  subgraphs = {}

  for person in persons:
    G.add_node(
      person.id,
      style=config.node_style_config.style,
      fillcolor=get_node_color(person, config.node_style_config),
      label=person.get_label(config.person_label_config),
      group=person.id,
      fontname=config.node_style_config.font,
      fontsize=config.node_style_config.font_size
    )

    if person.parents != []:
      # Add central childrens nodes
      parents_union_name = f"{get_union_name(person.parents)}/childrens"
      G.add_node(parents_union_name, shape="point", style="invis", width="0", group=get_union_name(person.parents))

      # Add middle childrens nodes and edges
      parents_union_name_w_child = f"{parents_union_name}/{person.id}"
      G.add_node(parents_union_name_w_child, shape="point", style="invis", width="0", group=person.id)
      G.add_edge(parents_union_name_w_child, person.id, minlen=1)

      # Prepare subgraph with all the middle childrens nodes align at the same rank
      if parents_union_name not in subgraphs.keys():
        subgraphs[parents_union_name] = [parents_union_name_w_child]
      else:
        subgraphs[parents_union_name].append(parents_union_name_w_child)

    for spouse in person.spouses:
      union_name = f"{get_union_name([person.id, spouse])}/union"
      G.add_node(union_name, shape="point", style="invis", width="0", group=get_union_name([person.id, spouse]))
      
      if union_name not in subgraphs.keys():
        subgraphs[union_name] = [person.id, spouse]

      if person.childrens != []:
        parents_union_name = f"{get_union_name([person.id, spouse])}/childrens"
        G.add_edge(union_name, parents_union_name, minlen=1)

  for k, v in subgraphs.items():
    order = v[:len(v)//2] + [k] + v[len(v)//2:]

    G.add_subgraph(order, rank="same")
    for n in range(len(order)):
      if n+1 >= len(order): continue
      G.add_edge(order[n], order[n+1], minlen=1)

  G.layout(prog='dot')
  G.draw(output_file_path)