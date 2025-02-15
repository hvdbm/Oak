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

def add_parents_to_tree(
  person: Person,
  family: Family,
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
    family (Family): the family object with all the relatives of the person.
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
  if family.is_only_child(person.id):
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
    generate_generations(family.members[parent], family, generations, current_generation-1, already_seen, tree, childrens_subgraphs)

def generate_generations(
  person: Person,
  family: Family,
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
      add_parents_to_tree(family.members[spouse], family, generations, current_generation, already_seen, tree, childrens_subgraphs)

    # Special case : if a person have childrens but no spouse
    if len(person.spouses) == 0 and len(person.childrens) != 0:
      tree.add_edge(person.id, f"{get_union_name([person.id])}/childrens")

    for children in person.childrens:
      generate_generations(family.members[children], family, generations, current_generation+1, already_seen, tree, childrens_subgraphs)

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
  tree = pgv.AGraph(
    splines="ortho",
    bgcolor=config.background_color,
    label=config.title_config.get_label(family.name),
    labelloc=config.title_config.location,
    fontcolor=config.title_config.fontcolor,
    fontname=config.title_config.fontname,
    fontsize=config.title_config.fontsize
  )

  already_seen_members = set()
  generations = {}
  childrens_subgraphs = {}

  current_generation = 0

  # Add persons
  for person in persons:
    tree.add_node(person.id, label=config.person_label_config.get_label(person), image=person.image, group=person.id)
  
    generate_generations(
      person, family, generations, current_generation, already_seen_members, tree, childrens_subgraphs
    )

  # Add edges and ranks of persons of the same generation
  for gen in generations.values(): gen.add_subgraph_to_tree(tree)

  # Add intermediate nodes and edges between generations
  for n in range(len(generations)):
    n_order = []
    
    for v in childrens_subgraphs.values():
      if n != v.gen_id: continue
      v_order = v.get_order()
      
      if n_order != []:
        tree.add_edge(n_order[-1], v_order[0], style="invis")

      n_order += v_order

    tree.add_subgraph(n_order, rank="same")
    for n in range(len(n_order)):
      if n+1 >= len(n_order): continue
      if (n_order[n], n_order[n+1]) in tree.edges(): continue
      tree.add_edge(n_order[n], n_order[n+1])

  apply_edges_style(tree, config)
  apply_node_style(tree, config, family)

  tree.layout(prog='dot')
  tree.draw(output_file_path)

def apply_dict(
  obj: dict,
  dict: dict
) -> None:
  for key, value in dict.items():
    obj[key] = value

def apply_node_style(
  tree: pgv.AGraph,
  config: TreeConfiguration,
  family: Family
) -> None:
  for node in tree.nodes():
    if node.attr['shape'] == "point": continue

    # Get the default node style dict
    apply_dict(node.attr, config.node_config.__dict__)

    person = family.members[node]
    # Apply conditional node style on the the previous dict
    for conditional_node in config.node_config.conditional_nodes:
      if conditional_node.key not in person.__dict__.keys(): continue

      if conditional_node.operator == "==":
        if person.__dict__[conditional_node.key] == conditional_node.value:
          apply_dict(node.attr, conditional_node.style_args)
      elif conditional_node.operator == "!=":
        if person.__dict__[conditional_node.key] != conditional_node.value:
          apply_dict(node.attr, conditional_node.style_args)

    # Apply node style by id on the previous dict
    if node in config.node_config.nodes.keys():
      apply_dict(node.attr, config.node_config.nodes[node].__dict__)

def apply_edges_style(
  tree: pgv.AGraph,
  config: TreeConfiguration
) -> None:
  for edge in tree.edges():
    if edge.attr['style'] == "invis": continue

    edge_config = config.edge_config.edges.get((edge[0], edge[1]), config.edge_config)
    apply_dict(edge.attr, edge_config.__dict__)
