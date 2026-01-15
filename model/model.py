import networkx as nx
from networkx.classes import neighbors

from database.DB_connect import DBConnect
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()

        self.teams = []
        self.salaries_map = {}
        self.team_map = {}
        self.K = 7
        self.best_path = []
        self.best_weight = 0


    def load_years(self):
        return DAO.get_years()

    def load_teams(self, year):
        self.teams = DAO.get_teams(year)
        return self.teams

    def build_graph(self, year):
        self.G.clear()

        self.salaries_map = DAO.get_salaries(year)

        for i, t1 in enumerate(self.teams):
            for t2 in self.teams[i+1:]:
                peso = self.salaries_map.get(t1.id, 0) + self.salaries_map.get(t2.id, 0)
                self.G.add_edge(t1, t2, weight=peso)

        self.team_map = {t.id: t for t in self.teams}

    def get_neighbours(self, team):
        vicini = []
        for n in self.G.neighbors(team):
            w = self.G[team][n]['weight']
            vicini.append((n, w))
        return sorted(vicini, key=lambda x: x[1], reverse=True)

    def compute_path(self, start):
        self.best_path = []
        self.best_weight = 0

        self._ricorsione([start], 0, float("inf"))

        return self.best_path, self.best_weight

    def _ricorsione(self, path, weight, last_edge_weight):
        last = path[-1]
        if weight > last_edge_weight:
            self.best_weight = weight
            self.best_path = path.copy()

        vicini = self.get_neighbours(last)
        neighbors = []
        counter = 0
        for node, edge_w in vicini:
            if node in path:
                continue
            if edge_w <= last_edge_weight:
                neighbors.append((node, edge_w))
                counter += 1
                if counter == self.K:
                    break

        for node, edge_w in neighbors:
            path.append(node)
            self._ricorsione(path, weight + edge_w, edge_w)
            path.pop()