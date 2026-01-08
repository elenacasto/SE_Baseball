import networkx as nx

from database.DB_connect import DBConnect
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()

        self.teams = []
        self.mappa_id = {}
        self.salaries = {}


    def load_year(self , min_year):
        return DAO.get_year(min_year)

    def load_teams(self, min_year):
        self.teams = DAO.get_teams(min_year)
        for t in self.teams:
            self.mappa_id[t['id']] = t

    def build_graph(self, year):

        self.G.clear()
        self.G.add_nodes_from(self.teams)

        self.salaries = DAO.get_salaries(year)

        for i, t1 in enumerate(self.teams):
            for t2 in self.teams[i+1:]:
                w = self.salaries.get(t1.id, 0) + self.salaries.get(t2.id, 0)
                self.G.add_edge(t1, t2, weight=w)
