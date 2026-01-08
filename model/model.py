import networkx as nx

from database.DB_connect import DBConnect
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()

        self.teams = []
        self.teams_map = {}
        self.salaries = {}


    def get_years(self):
        return DAO.get_year()

    def load_teams(self, year):
        self.teams = DAO.get_teams(year)
        return self.teams

    def build_graph(self, year):

        self.G.clear()
        self.salaries = DAO.get_salaries(year)

        for i, t1 in enumerate(self.teams):
            for t2 in self.teams[i+1:]:
                w = self.salaries.get(t1.id, 0) + self.salaries.get(t2.id, 0)
                self.G.add_edge(t1, t2, weight=w)

        self.teams_map = {t.id: t for t in self.teams}

    def get_vicini(self, team):
        vicini = []
        for n in self.G.neighbors(team):
            w = self.G[team][n]['weight']
            vicini.append((n,w))
        return sorted(vicini, key=lambda x: x[1], reverse=True)

    def jk(self):
        pass

    def jk2(self):
        pass
