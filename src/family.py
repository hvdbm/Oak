from src.person import Person
import pygraphviz as pgv
import json
from src.configuration import Configuration

Family = dict[Person]

def read_family(file_path: str) -> Family:
  family = {}
  with open(file_path, 'r') as file:
    for p in json.load(file):
      person = Person(**p)
      family[person.id] = person
  
  for _, value in family.items():
    value.n_ancestors = find_n_ancestors(value, family)

  return family

def get_union_name(parents):
  if len(parents) == 1:
     parents.append("???")
  try :
    sorted_id = sorted(parents)
    return f"{sorted_id[0]} & {sorted_id[1]}"
  except:
     print(parents)
        
def find_n_ancestors(person: Person, family: Family) -> int:
  if person.parents == []: return 0
  if person.n_ancestors != None: return person.n_ancestors
  
  n = 1
  for parent in person.parents:
    if parent not in family.keys(): continue
    n += find_n_ancestors(family[parent], family)
  
  return n

def draw_family_tree(
  family: Family, 
  config: Configuration,
  output_file_path: str
) -> None:
  G = pgv.AGraph(splines="ortho", label=config.graph_title)
  G.node_attr['shape'] = config.node_shape

  values = list(family.values())
  values.sort(key=lambda x: x.birth_year)
  values.reverse()
  values.sort(key=lambda x: x.n_ancestors)
  values.reverse()

  subgraphs = {}

  for person in values:
    G.add_node(person.id, label=person.get_label(config.label_options), group=person.id)

    if person.parents != []:
      # Add central childrens nodes
      parents_union_name = f"{get_union_name(person.parents)}/childrens"
      G.add_node(parents_union_name, shape="point", style="invis", group=get_union_name(person.parents))

      # Add middle childrens nodes and edges
      parents_union_name_w_child = f"{parents_union_name}/{person.id}"
      G.add_node(parents_union_name_w_child, shape="point", style="invis", group=person.id)
      G.add_edge(parents_union_name_w_child, person.id, minlen=1)

      # Prepare subgraph with all the middle childrens nodes align at the same rank
      if parents_union_name not in subgraphs.keys():
        subgraphs[parents_union_name] = [parents_union_name_w_child]
      else:
        subgraphs[parents_union_name].append(parents_union_name_w_child)

    for spouse in person.spouses:
      union_name = f"{get_union_name([person.id, spouse])}/union"
      G.add_node(union_name, shape="point", style="invis", group=get_union_name([person.id, spouse]))
      
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