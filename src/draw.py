
import pygraphviz as pgv

from src.tree_config.configuration import TreeConfiguration, NodeConfig
from src.label import bold, newline
from src.person import Person
from src.utils import get_union_name

def get_node_color(person: Person, node_config: NodeConfig) -> str:
  if node_config.color_by is None : return node_config.default_color
  
  if node_config.color_by in person.__dict__.keys():
    value = person.__dict__.get(node_config.color_by)
    return node_config.color_by_dict.get(value, node_config.default_color)
  
  return node_config.default_color

def generate_generations(
  person: Person,
  family,
  generations: dict,
  current_generation: int,
  already_seen: set,
  tree: pgv.AGraph,
  childrens_subgraphs: dict
  ):
  if current_generation not in generations.keys(): generations[current_generation] = []
  
  if person.id not in already_seen:
    generations[current_generation].append(person.id)
    already_seen.add(person.id)

    if person.parents != []:
      # Add parents intermediate node
      parents_union_name_childrens = f"{get_union_name(person.parents)}/childrens"
      tree.add_node(parents_union_name_childrens, shape="point", group=get_union_name(person.parents))
      
      # Add middle childrens nodes and edges
      parents_union_name_w_child = f"{parents_union_name_childrens}/{person.id}"
      tree.add_node(parents_union_name_w_child, shape="point", group=person.id)
      tree.add_edge(parents_union_name_w_child, person.id)

      # Prepare subgraph with all the middle childrens nodes align at the same rank
      if parents_union_name_childrens not in childrens_subgraphs.keys():
        childrens_subgraphs[parents_union_name_childrens] = [parents_union_name_w_child]
      else:
          childrens_subgraphs[parents_union_name_childrens].append(parents_union_name_w_child)

    # Add spouses to the same generation
    for spouse in person.spouses:
      if spouse not in already_seen:

        # Add intermediate node between spouses
        union_name = f"{get_union_name([person.id, spouse])}/union"
        tree.add_node(union_name, shape="point", group=get_union_name([person.id, spouse]))
        
        # Add intermediate node in generation
        generations[current_generation].append(union_name)

        # Add spouse to generation
        generations[current_generation].append(spouse)
        already_seen.add(spouse)


        tree.add_edge(person.id, union_name)
        tree.add_edge(union_name, spouse)
      
        if person.childrens != []:
          parents_union_name = f"{get_union_name([person.id, spouse])}/childrens"
          tree.add_edge(union_name, parents_union_name)

    for children in person.childrens:
      generate_generations(family[children], family, generations, current_generation+1, already_seen, tree, childrens_subgraphs)

def draw_tree(
  persons: list[Person],
  title: str, 
  config: TreeConfiguration,
  output_file_path: str,
  family = {}
) -> None:
  G = pgv.AGraph(
    splines="ortho",
    bgcolor=config.background_color,
    label=f"<{bold(title)} {newline()} >" if title != "" else "",
    labelloc=config.title_config.location,
    fontname=config.title_config.font,
    fontsize=config.title_config.font_size,
  )
  
  G.edge_attr['color'] = config.edge_config.color
  G.edge_attr['penwidth'] = config.edge_config.penwidth

  G.node_attr['shape'] = config.node_config.shape

  already_seen_members = set()
  generations = {}
  childrens_subgraphs = {}

  current_generation = 0

  for person in persons:
    G.add_node(
      person.id,
      style=config.node_config.style,
      fillcolor=get_node_color(person, config.node_config),
      label=person.get_label(config.person_label_config),
      group=person.id,
      fontname=config.node_config.font,
      fontsize=config.node_config.font_size,
    )
    generate_generations(
      person, family, generations, current_generation, already_seen_members, G, childrens_subgraphs
    )

  for k, v in generations.items():
    G.add_subgraph(v, rank="same")

    for n in range(len(v)):
      if n+1 >= len(v): continue
      first, second = v[n], v[n+1]
      if (first, second) in G.edges(): continue
      G.add_edge(v[n], v[n+1], style="invis")

  for k, v in childrens_subgraphs.items():
    order = v[:len(v)//2] + [k] + v[len(v)//2:]

    G.add_subgraph(order, rank="same")
    for n in range(len(order)):
      if n+1 >= len(order): continue
      G.add_edge(order[n], order[n+1])

  G.layout(prog='dot')
  G.draw(output_file_path)