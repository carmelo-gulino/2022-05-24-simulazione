import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.soluzioni = None
        self.best_sol = None
        self.genres = DAO.get_all_genres()
        self.graph = nx.Graph()

    def build_graph(self, genreId):
        self.graph.clear()
        tracks = DAO.get_tracks(genreId)
        self.graph.add_nodes_from(tracks)
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                if u != v and u.MediaTypeId == v.MediaTypeId:
                    peso = abs(u.Milliseconds - v.Milliseconds)
                    self.graph.add_edge(u, v, weight=peso)
        return self.graph

    def get_delta_max(self):
        edges_list = [(edge, self.graph[edge[0]][edge[1]]['weight']) for edge in self.graph.edges]
        edges_list.sort(key=lambda x: x[1], reverse=True)
        result = [(edge, self.graph[edge[0]][edge[1]]['weight'])
                  for edge in self.graph.edges if self.graph[edge[0]][edge[1]]['weight'] == edges_list[0][1]]
        return result

    def get_lista(self, canzone, memoria):
        self.best_sol = None
        self.soluzioni = []
        connessa = list(nx.node_connected_component(self.graph, canzone))
        self.ricorsione({canzone}, canzone, memoria, [], connessa, 0)
        self.soluzioni.sort(key=lambda x: x[1], reverse=True)
        self.best_sol = self.soluzioni[0][0]
        return self.best_sol

    def ricorsione(self, parziale, canzone, memoria, memoria_cum, connessa, pos):
        if pos == len(connessa):
            memoria_sol = memoria_cum[-1]
            if memoria_sol <= memoria:
                self.soluzioni.append((copy.deepcopy(parziale), len(parziale)))
                print(parziale)
        p = connessa[pos]
        try:
            memoria_sol = memoria_cum[-1]
        except IndexError:
            memoria_sol = 0
        pos += 1
        if p not in parziale:
            parziale.add(p)
            memoria_cum.append(memoria_sol + p.Bytes)
            self.ricorsione(parziale, canzone, memoria, memoria_cum, connessa, pos)
            parziale.remove(p)
            memoria_cum.pop()
