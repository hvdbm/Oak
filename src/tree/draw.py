import pygraphviz as pgv

from src.family import Family
from src.person import Person
from src.tree.configuration import TreeConfiguration
from src.tree.trim import trim
from src.utils import apply_dict


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
    self.members: list[str] = []
  
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
    self.members: list[str] = []
  
  def add_member(self, person_id: str):
    self.members.append(person_id)
  
  def get_order(self):
    n_member = len(self.members)
    return self.members[:n_member//2] + [self.id] + self.members[n_member//2:]

def add_parents_to_tree(
  person: Person,
  family: Family,
  generations: dict[int, Generation],
  current_generation: int,
  already_seen: set[str],
  tree: pgv.AGraph,
  childrens_subgraphs: dict[str, IntermediateGeneration]
) -> None:
  """
  Add the parents of a person to the tree. The nodes of the parents are added to the previous generation and 
  the edges are drawn between the parents and the person, with the necessary intermediate nodes.

  Parameters:
    person (Person): the person to add the parents from.
    family (Family): the family object with all the relatives of the person.
    generations (dict[int, Generation]): all the generations of the family, where the key is the depth.
    current_generation (int): the current generation.
    already_seen (set[str]): the set of already seen persons.
    tree (pgv.AGraph): the graphviz tree to draw the parents nodes and edges to.
    childrens_subgraphs (dict[str, IntermediateGeneration]): the intermediate nodes between the parents and the childrens of the parents.
  
  Returns:
    None
  """
  if person.parents == []: return

  # Add parents intermediate node
  union_name = get_union_name(person.parents)
  parents_union_name_childrens = f"{union_name}/childrens"
  
  tree.add_node(parents_union_name_childrens, group=union_name, shape="point", style="invis", height=0, width=0)

  # Add edge between a parent union and their childrens
  if (union_name, parents_union_name_childrens) not in tree.edges():
    parents_node = person.parents[0] if len(person.parents) == 1 else f"{union_name}/union"
    tree.add_edge(parents_node, parents_union_name_childrens)

  # Prepare subgraph with all the middle childrens nodes align at the same rank
  if parents_union_name_childrens not in childrens_subgraphs:
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
    tree.add_node(parents_union_name_w_child, group=person.id, shape="point", style="invis", height=0, width=0)
    tree.add_edge(parents_union_name_w_child, person.id)
    childrens_subgraphs[parents_union_name_childrens].add_member(parents_union_name_w_child)

  # Add parents to the previous generation
  for parent in person.parents:
    generate_generations(family.members[parent], family, generations, current_generation-1, already_seen, tree, childrens_subgraphs)


def generate_generations(
  person: Person,
  family: Family,
  generations: dict[int, Generation],
  current_generation: int,
  already_seen: set[str],
  tree: pgv.AGraph,
  childrens_subgraphs: dict[str, IntermediateGeneration]
) -> None:
  if current_generation not in generations: generations[current_generation] = Generation(current_generation)
  
  if person.id not in already_seen:
    generations[current_generation].add_member(person.id)
    already_seen.add(person.id)

    add_parents_to_tree(person, family, generations, current_generation, already_seen, tree, childrens_subgraphs)

    # Add spouses to the same generation
    for spouse in person.spouses:
      # Add intermediate node between spouses
      union_name = f"{get_union_name([person.id, spouse])}/union"
      tree.add_node(union_name, group=get_union_name([person.id, spouse]), shape="point", style="invis", height=0, width=0)
        
      # Add intermediate node in generation
      generations[current_generation].add_member(union_name)

      # Add spouse to generation
      generations[current_generation].add_member(spouse)
      already_seen.add(spouse)

      # Add edge between the spouses and their union node
      tree.add_edge(person.id, union_name)
      tree.add_edge(union_name, spouse)

      # Add spouse's parents to the previous generation
      add_parents_to_tree(family.members[spouse], family, generations, current_generation, already_seen, tree, childrens_subgraphs)

    # Special case : if a person have childrens but no spouse
    if len(person.spouses) == 0 and len(person.childrens) != 0:
      tree.add_edge(person.id, f"{get_union_name([person.id])}/childrens")

    for children in person.childrens:
      generate_generations(family.members[children], family, generations, current_generation+1, already_seen, tree, childrens_subgraphs)

def get_persons_list(family: Family, config: TreeConfiguration) -> list[Person]:
  """
  Get the list of persons to draw in the tree, ordered by number of descendants.
  The persons are filtered by the ignore list in the configuration.
  If a start person is defined, it will be moved to the first position.

  Parameters:
    family (Family): the family object with all the relatives of the person.
    config (TreeConfiguration): the configuration of the tree.
  Returns:
    list[Person]: the list of persons to draw in the tree.
  """
  # Trim the family tree by removing unwanted members
  trim(family, config.trim_config)

  # Order remaining members of the family by n_descendants descending order
  persons = list(family.members.values())
  persons.sort(key=lambda x : family.n_descendants.get(x.id, 0))
  persons.reverse()

  # If a start person is defined, move it to the first position
  if config.start_person is not None:
    start_person = family.members.get(config.start_person)
    if start_person is None:
      raise ValueError(f"Start person with id '{config.start_person}' not found in the family tree.")

    # Find index of the start person
    idx = persons.index(start_person)
    if idx == -1:
      raise ValueError(f"Start person with id '{config.start_person}' not found in the family tree.")
    
    # Move the start person to the first position
    persons.insert(0, persons.pop(idx))
  
  return persons

def draw_tree(
  family: Family,
  config: TreeConfiguration,
  output_file_path: str,
) -> None:
  # List of persons to draw
  persons = get_persons_list(family, config)

  # Init graph
  tree = pgv.AGraph(
    splines="ortho",
    bgcolor=config.background_color,
    label=config.title_config.get_label(),
    labelloc=config.title_config.location,
    fontcolor=config.title_config.fontcolor,
    fontname=config.title_config.fontname,
    fontsize=config.title_config.fontsize
  )

  already_seen_members: set[str] = set()
  generations: dict[int, Generation] = {}
  childrens_subgraphs: dict[str, IntermediateGeneration] = {}

  current_generation = 0

  # Add persons
  for person in persons:
    tree.add_node(
      person.id,
      label=config.person_label_config.get_label(person),
      image=person.image,
      group=person.id
    )
  
    generate_generations(
      person,
      family,
      generations,
      current_generation,
      already_seen_members,
      tree,
      childrens_subgraphs
    )

  # Add edges and ranks of persons of the same generation
  for gen in generations.values(): gen.add_subgraph_to_tree(tree)

  # Add intermediate nodes and edges between generations
  for n in range(len(generations)):
    n_order: list[str] = []
    
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

def apply_node_style(
  tree: pgv.AGraph,
  config: TreeConfiguration,
  family: Family
) -> None:
  for node in tree.nodes():
    if node.attr['shape'] == "point" and node not in config.node_config.nodes: continue

    # Get the default node style dict
    apply_dict(node.attr, config.node_config.__dict__)

    person = family.members[node]
    # Apply conditional node style on the the previous dict
    for conditional_node in config.node_config.conditional_nodes:
      if conditional_node.key not in person.__dict__: continue

      if conditional_node.operator == "==":
        if person.__dict__[conditional_node.key] == conditional_node.value:
          apply_dict(node.attr, conditional_node.style_args)
      elif conditional_node.operator == "!=":
        if person.__dict__[conditional_node.key] != conditional_node.value:
          apply_dict(node.attr, conditional_node.style_args)

    # Apply node style by id on the previous dict
    if node in config.node_config.nodes:
      apply_dict(node.attr, config.node_config.nodes[node].__dict__)

def apply_edges_style(
  tree: pgv.AGraph,
  config: TreeConfiguration
) -> None:
  edges_config = config.edge_config
  for edge in tree.edges():
    edge_id = (edge[0], edge[1])
    if edge.attr['style'] == "invis" and edge_id not in edges_config.edges: continue

    edge_config = edges_config.edges.get(edge_id, edges_config)
    apply_dict(edge.attr, edge_config.__dict__)
