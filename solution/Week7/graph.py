from pygraphviz import AGraph
from PIL import Image

class Graph(object):
    def __init__(self, graph_dict={}):
        self.__graph_dict = graph_dict
        self.__G = AGraph()

    def add_vertex(self, v):
        if( v not in self.__graph_dict):
            self.__graph_dict[v] = []
        self.__G.add_node(v)

    def add_edge(self, u, v):
        if( u not in self.__graph_dict):
            self.__graph_dict[u] = [v]
        else:
            self.__graph_dict[u].append(v)

        self.__G.add_edge(u, v)

    def draw(self, fn):
        print(self.__graph_dict)
        self.__G.draw(fn, prog="circo")
        Image.open(fn).show()

    def clear(self):
        self.__graph_dict = {}
        self.__G.clear()

    def isConnected(self, path=None, start_vertex=None):
        if path == None:
            path = set()
        vertices = list(self.__graph_dict.keys()) # "list" necessary in Python 3 
        if start_vertex == None:
            start_vertex = vertices[0]
        path.add(start_vertex)
        
        if len(path) == len(vertices):
            return True
        else:
            for v in self.__graph_dict[start_vertex]:
                if v not in path:
                    if self.isConnected(path, v):
                        return True
        return False