import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def populate_years(self):
        self.list_years = self._model.load_years()

        for year in self.list_years:
            self._view.dd_anno.options.append(ft.dropdown.Option(year))
        self._view.update()

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""

        try:
            year = int(self._view.dd_anno.value)
        except AttributeError:
            self._view.show_alert("Selezionare l'anno")
            return

        self._model.build_graph(year)


    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        team_id = int(self._view.dd_squadra.value)

        self._view.txt_risultato.controls.clear()
        for n, w in self._model.get_neighbours(self._model.team_map[team_id]):
            self._view.txt_risultato.controls.append(
                ft.Text(f"{n} - peso {w}")
            )
        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        team_id = self._view.dd_squadra.value
        start = next(t for t in self._model.teams if t.id == int(team_id))
        path, weight = self._model.compute_path(start)

        self._view.txt_risultato.controls.clear()
        for i in range(len(path) - 1):
            w = self._model.G[path[i]][path[i + 1]]['weight']
            self._view.txt_risultato.controls.append(
                ft.Text(f"{path[i]} -> {path[i + 1]} (peso {w})")
            )

        self._view.txt_risultato.controls.append(
            ft.Text(f"Peso totale: {weight}")
        )
        self._view.update()

    """ Altri possibili metodi per gestire di dd_anno """""
    def get_years(self):
        return self._model.load_years()

    def handle_year_change(self, e):
        year = int(self._view.dd_anno.value)
        teams = self._model.load_teams(year)

        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(
            ft.Text(f"Numero squadre: {len(teams)}")
        )
        for t in teams:
            self._view.txt_out_squadre.controls.append(
                ft.Text(f"{t}")
            )

        self._view.dd_squadra.options = [
            ft.dropdown.Option(key=str(t.id), text=t)
            for t in teams
        ]
        self._view.update()