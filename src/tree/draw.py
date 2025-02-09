import pygraphviz as pgv

from src.tree.configuration import TreeConfiguration, NodeConfig
from src.person import Person
from src.family import Family

def get_union_name(parents: list[str]) -> str:
  """
  Get the union name of parents.

  Parameters:
    parents (list[str]): the list of ids of the parents of a person.

  Returns:
    str: the union name of the parents.
  """
  return " & ".join(sorted(parents))

def get_node_color(person: Person, node_config: NodeConfig) -> str:
  """
  Get the color of a node based on the node configuration. If no color_by is specified or used, the default color is returned.

  Parameters:
    person (Person): the person to get the color from.
    node_config (NodeConfig): the node configuration.

  Returns:
    str: the color of the node.
  """
  if node_config.color_by is None : return node_config.default_color
  
  if node_config.color_by in person.__dict__.keys():
    value = person.__dict__.get(node_config.color_by)
    return node_config.color_by_dict.get(value, node_config.default_color)
  
  return node_config.default_color

class Generation():
  def __init__(self, gen_id: int):
    self.id = gen_id
    self.members = []
  
  def add_member(self, person_id: str):
    self.members.append(person_id)
  
  def add_subgraph_to_tree(self, tree: pgv.AGraph):
    # Add subgraph
    tree.add_subgraph(self.members, rank="same")

    # Add invisible edges between the nodes of the subgraph to make sure their order is followed
    n_members = len(self.members)
    for n in range(n_members):
      if n+1 >= n_members: continue
      first, second = self.members[n], self.members[n+1]
      if (first, second) in tree.edges(): continue  # Don't replace an already existing edge with an invisible one
      tree.add_edge(first, second, style="invis")

class IntermediateGeneration():
  def __init__(self, group_id: str, gen_id: int):
    self.id = group_id
    self.gen_id = gen_id
    self.members = []
  
  def add_member(self, person_id: str):
    self.members.append(person_id)
  
  def get_order(self):
    n_member = len(self.members)
    return self.members[:n_member//2] + [self.id] + self.members[n_member//2:]

def is_only_child(parents: list[str], family: dict[Person]) -> bool:
  """
  Check if the person is the only child of the union of his parents.

  Parameters:
    parents (list[str]): the list of parents of the person.
    family (dict[Person]): all the family members.
  
  Returns:
    bool: True if the person is the only child of the union of his parents, False otherwise.
  """
  for parent in parents:
    if len(family[parent].childrens) == 1: return True
  
  return False

def add_parents_to_tree(
  person: Person,
  family: dict[Person],
  generations: dict[Generation],
  current_generation: int,
  already_seen: set[str],
  tree: pgv.AGraph,
  childrens_subgraphs: dict[IntermediateGeneration]
) -> None:
  """
  Add the parents of a person to the tree. The nodes of the parents are added to the previous generation and 
  the edges are drawn between the parents and the person, with the necessary intermediate nodes.

  Parameters:
    person (Person): the person to add the parents from.
    family (dict[Person]): all the family members.
    generations (dict[Generation]): all the generations of the family.
    current_generation (int): the current generation.
    already_seen (set[str]): the set of already seen persons.
    tree (pgv.AGraph): the graphviz tree to draw the parents nodes and edges to.
    childrens_subgraphs (dict[IntermediateGeneration]): the intermediate nodes between the parents and the childrens of the parents.
  
  Returns:
    None
  """
  if person.parents == []: return

  # Add parents intermediate node
  union_name = get_union_name(person.parents)
  parents_union_name_childrens = f"{union_name}/childrens"
  tree.add_node(parents_union_name_childrens, shape="point", group=union_name)

  # Prepare subgraph with all the middle childrens nodes align at the same rank
  if parents_union_name_childrens not in childrens_subgraphs.keys():
    childrens_subgraphs[parents_union_name_childrens] = IntermediateGeneration(parents_union_name_childrens, current_generation-1)

  # Add middle childrens nodes and edges
  if is_only_child(person.parents, family):
    # Special case : the person is the only child, no need to add intermediate nodes
    parents_union_name_w_child = parents_union_name_childrens
    tree.add_edge(parents_union_name_w_child, person.id)

    # Modify the group of the person node to union_name
    tree.get_node(parents_union_name_childrens).attr['group'] = person.id
    if f"{union_name}/union" in tree.nodes(): tree.get_node(f"{union_name}/union").attr['group'] = person.id
  else:
    parents_union_name_w_child = f"{parents_union_name_childrens}/{person.id}"
    tree.add_node(parents_union_name_w_child, shape="point", group=person.id)
    tree.add_edge(parents_union_name_w_child, person.id)
    childrens_subgraphs[parents_union_name_childrens].add_member(parents_union_name_w_child)

  # Add parents to the previous generation
  for parent in person.parents:
    generate_generations(family[parent], family, generations, current_generation-1, already_seen, tree, childrens_subgraphs)

def generate_generations(
  person: Person,
  family: dict[Person],
  generations: dict[Generation],
  current_generation: int,
  already_seen: set[str],
  tree: pgv.AGraph,
  childrens_subgraphs: dict[IntermediateGeneration]
) -> None:
  if current_generation not in generations.keys(): generations[current_generation] = Generation(current_generation)
  
  if person.id not in already_seen:
    generations[current_generation].add_member(person.id)
    already_seen.add(person.id)

    add_parents_to_tree(person, family, generations, current_generation, already_seen, tree, childrens_subgraphs)

    # Add spouses to the same generation
    for spouse in person.spouses:
      # Add intermediate node between spouses
      union_name = f"{get_union_name([person.id, spouse])}/union"
      tree.add_node(union_name, shape="point", group=get_union_name([person.id, spouse]))
        
      # Add intermediate node in generation
      generations[current_generation].add_member(union_name)

      # Add spouse to generation
      generations[current_generation].add_member(spouse)
      already_seen.add(spouse)

      tree.add_edge(person.id, union_name)
      tree.add_edge(union_name, spouse)
        
      if person.childrens != []:
        tree.add_edge(union_name, f"{get_union_name([person.id, spouse])}/childrens")

      # Add spouse's parents to the previous generation
      add_parents_to_tree(family[spouse], family, generations, current_generation, already_seen, tree, childrens_subgraphs)

    # Special case : if a person have childrens but no spouse
    if len(person.spouses) == 0 and len(person.childrens) != 0:
      tree.add_edge(person.id, f"{get_union_name([person.id])}/childrens")

    for children in person.childrens:
      generate_generations(family[children], family, generations, current_generation+1, already_seen, tree, childrens_subgraphs)

def draw_tree(
  family: Family,
  config: TreeConfiguration,
  output_file_path: str,
) -> None:
  # Order persons of the family by n_descendants descending order
  persons = list(family.members.values())
  persons.sort(key=lambda x : x.n_descendants)
  persons.reverse()

  # Init graph
  G = pgv.AGraph(
    splines="ortho",
    bgcolor=config.background_color,
    label=config.title_config.get_label(family.name),
    fontcolor=config.title_config.font_color,
    labelloc=config.title_config.location,
    fontname=config.title_config.font,
    fontsize=config.title_config.font_size
  )
  
  G.edge_attr['color'] = config.edge_config.color
  G.edge_attr['penwidth'] = config.edge_config.penwidth

  G.node_attr['shape'] = config.node_config.shape

  already_seen_members = set()
  generations = {}
  childrens_subgraphs = {}

  current_generation = 0

  # Add persons
  for person in persons:
    G.add_node(
      person.id,
      style=config.node_config.style,
      fillcolor=get_node_color(person, config.node_config),
      label=config.person_label_config.get_label(person),
      labelloc=config.node_config.labelloc if person.image != "" else "",
      group=person.id,
      fontname=config.node_config.font,
      fontsize=config.node_config.font_size,
      fontcolor=config.node_config.font_color,
      image=person.image,
      imagepos=config.node_config.imagepos if person.image != "" else "",
      height=config.node_config.height_w_img if person.image != "" else ""
    )
    generate_generations(
      person, family.members, generations, current_generation, already_seen_members, G, childrens_subgraphs
    )

  # Add edges and ranks of persons of the same generation
  for gen in generations.values(): gen.add_subgraph_to_tree(G)

  # Add intermediate nodes and edges between generations
  for n in range(len(generations)):
    n_order = []
    
    for v in childrens_subgraphs.values():
      if n != v.gen_id: continue
      v_order = v.get_order()
      
      if n_order != []:
        G.add_edge(n_order[-1], v_order[0], style="invis")

      n_order += v_order

    G.add_subgraph(n_order, rank="same")
    for n in range(len(n_order)):
      if n+1 >= len(n_order): continue
      if (n_order[n], n_order[n+1]) in G.edges(): continue
      G.add_edge(n_order[n], n_order[n+1])

  G.layout(prog='dot')
  G.draw(output_file_path)