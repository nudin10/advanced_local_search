# Travelling Sales Person
import random
import yaml
import matplotlib.pyplot as plt
import networkx as nx
import itertools
from src.misc.exceptions import GraphNotInitialisedError
from src.data.cities import malaysian_cities
from src.misc.tools.common import get_graph_conf_path, write_to_graph_json

class TspGraph:
    def __init__(self) -> None:
        self._G = nx.Graph()
        self.nodes: list[str] = []
        self.w_nodes: list[tuple[str, str, int]] = []
    
    def construct(self):
        p = get_graph_conf_path()
        with open(p) as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
        try:
            if not conf['nodes']:
                raise GraphNotInitialisedError("Graph is not yet initialised!")
            else:
                self.nodes = conf['nodes']
                self.w_nodes = conf['w_nodes']
                self._G.add_weighted_edges_from(conf['w_nodes'])
        except KeyError:
            raise KeyError("Unable to construct graph nodes with given config")

    def show_graph(self):
        if not self.w_nodes:
            raise GraphNotInitialisedError("Graph is not yet initialised!")
        pos = nx.spring_layout(self._G)
        nx.draw(self._G, pos, with_labels=True, font_weight='bold', node_size=650, node_color='skyblue', edge_color='black')
        edge_labels = nx.get_edge_attributes(self._G, 'weight')
        nx.draw_networkx_edge_labels(self._G, pos, edge_labels=edge_labels)
        plt.show()
        
    def get_graph(self):
        return self._G
    
    
def init_graph(min, max) -> None:
    p = get_graph_conf_path()
    if min != max:
        city_count = random.randrange(min, max, 1)
    elif min > max:
        raise ValueError("Min should be lower than max")
    else:
        city_count = max
    cities = random.sample(malaysian_cities, city_count)
    nodes = [(u, v, random.randint(5,20)) for (u, v) in itertools.permutations(cities, 2)]
    write_to_graph_json(cities, nodes)

def get_tsp_graph() -> TspGraph:
    with open(get_graph_conf_path()) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    if not conf['nodes']:
        raise GraphNotInitialisedError("Graph is not yet initialised!")
    else:
        G = TspGraph()
        G.construct()
        return G

def show_graph() -> None:
    with open(get_graph_conf_path()) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    try:
        if not conf['nodes']:
            raise GraphNotInitialisedError("Graph is not yet initialised!")
        else:
            G = TspGraph()
            G.construct()
            G.show_graph()
    except KeyError:
        raise

def reset_graph() -> None:
    '''
    Resets graph config file
    '''
    write_to_graph_json([], [])