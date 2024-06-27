import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.chosen_canzone = None
        self.chosen_genre = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_genre(self):
        for g in self.model.genres:
            self.view.dd_genre.options.append(ft.dropdown.Option(data=g, text=g.Name, on_click=self.choose_genre))

    def choose_genre(self, e):
        if e.control.data is None:
            self.chosen_genre = None
        self.chosen_genre = e.control.data

    def handle_crea_grafo(self, e):
        if self.chosen_genre is None:
            self.view.create_alert("Selezionare un genere")
            return
        graph = self.model.build_graph(self.chosen_genre.GenreId)
        self.view.btn_delta_max.disabled = False
        self.fill_dd_canzone(graph)
        self.view.btn_lista.disabled = False
        self.view.txt_memoria.disabled = False
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Grafo con {len(graph.nodes)} nodi e {len(graph.edges)} archi"))
        self.view.update_page()

    def fill_dd_canzone(self, graph):
        self.view.dd_canzone.options.clear()
        self.view.dd_canzone.disabled = False
        for n in graph.nodes:
            self.view.dd_canzone.options.append(ft.dropdown.Option(data=n, text=n, on_click=self.choose_canzone))

    def choose_canzone(self, e):
        if e.control.data is None:
            self.chosen_canzone = None
        self.chosen_canzone = e.control.data

    def handle_delta_max(self, e):
        delta_max_list = self.model.get_delta_max()
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Gli archi con delta massimo sono:"))
        for d in delta_max_list:
            self.view.txt_result.controls.append(ft.Text(f"{d[0][0]} --> {d[0][1]}: {d[1]}"))
        self.view.update_page()

    def handle_lista(self, e):
        if self.chosen_canzone is None:
            self.view.create_alert("Selezionare una canzone")
            return
        try:
            memoria = int(self.view.txt_memoria.value)*(10**6)
        except ValueError:
            self.view.create_alert("Inserire una memoria in byte")
            return
        lista = self.model.get_lista(self.chosen_canzone, memoria)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"La lista trovata include {len(lista)} canzoni:"))
        for track in lista:
            self.view.txt_result.controls.append(ft.Text(f"{track}"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
