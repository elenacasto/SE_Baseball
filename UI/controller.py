import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""

        try:
            year = self._view.dd_anno.value
        except AttributeError:
            self._view.show_alert("Selezionare l'anno")
            return
        self._model.build_graph(year)



    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO

    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO