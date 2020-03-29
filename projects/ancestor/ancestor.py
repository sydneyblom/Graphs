
# import graph and util
from graph import Graph
from util import Queue

def earliest_ancestor(ancestors, starting_node):
    # build graph
    g = Graph()
    # for parents and children in ancestors...
    for (parent, child) in ancestors:
        # Add verteces for parent and child
        g.add_vertex(parent)
        g.add_vertex(child)
        # Add edge for parent, child
        g.add_edge(parent, child)

    # create empty list for new path
    new_path = []

    # for each parent, child...
    for (parent, child) in ancestors:
        # find path to starting node (using dfs)
        path = g.dfs(parent, starting_node)
        # check if new path is longer than previous...
        if path is not None and len(path) > len(new_path):
            # if not, new path will replace old path
            new_path = path.copy()

    # check if new path has no parents...
    if len(new_path) <= 1:
        # if yes, return -1
        return -1
    # otherwise, return new path at 0 index
    return new_path[0]