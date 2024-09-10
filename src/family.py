from src.person import Person
import pygraphviz as pgv
import json

Family = list[Person]

def read_family(file_path: str) -> Family:
  with open(file_path, 'r') as file:
    return [Person.from_obj(person) for person in json.load(file)]

def draw_family_tree(family: Family, output_dir: str) -> None:
  G = pgv.AGraph(directed=True)
  G.node_attr['shape'] = 'box'

  for person in family:
    G.add_node(person.id, style='filled', label=person.get_label())

    # Add edge to parents
    for parent in person.parents:
      G.add_edge(parent, person.id)

    # Add subgraph for spouses
    for spouse in person.spouses:
      G.add_subgraph([person.id, spouse], rank='same')

    for child in person.childrens:
      G.add_edge(person.id, child)

  G.layout(prog='dot')

  G.draw(f"{output_dir}/family_tree.png")