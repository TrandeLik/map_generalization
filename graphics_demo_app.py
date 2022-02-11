import tkinter as tk
from create_polyline import *
from algorithm_params import params


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.cvs_graphics = tk.Canvas(self, background="white")
        self.fr_menu = tk.Frame(self)
        self.lbl_count = tk.Label(self.fr_menu, text="Количество звеньев ломаной:")
        self.ent_count = tk.Entry(self.fr_menu)
        self.btn_generate = tk.Button(self.fr_menu, text="Сгенерировать ломаную")
        self.btn_generate.bind("<Button-1>", self.run_generate_line)
        self.lbl_algo = tk.Label(self.fr_menu, text="Отображать следующие линии:")
        self.to_draw_main = tk.IntVar()
        self.cb_draw_main = tk.Checkbutton(self.fr_menu, text="Основная линия",
                                           variable=self.to_draw_main, command=self.run_main_algo)
        self.to_equidistant = tk.IntVar()
        self.cb_equidistant = tk.Checkbutton(self.fr_menu, text="Равнозвенная линия",
                                             variable=self.to_equidistant, command=self.run_main_algo)
        self.to_make_segmentation = tk.IntVar()
        self.cb_segmentation = tk.Checkbutton(self.fr_menu, text="Сегментированная линия",
                                              variable=self.to_make_segmentation, command=self.run_main_algo)
        self.to_simplify = tk.IntVar()
        self.cb_simplify = tk.Checkbutton(self.fr_menu, text="Упрощенная линия",
                                          variable=self.to_simplify, command=self.run_main_algo)
        self.to_smooth = tk.IntVar()
        self.cb_smoothing = tk.Checkbutton(self.fr_menu, text="Сглаженная линия",
                                           variable=self.to_smooth, command=self.run_main_algo)
        self.lbl_others = tk.Label(self.fr_menu, text="Другие опции")
        self.need_polygon = tk.IntVar()
        self.cb_polygon = tk.Checkbutton(self.fr_menu, text="Залитый многоугольник",
                                         variable=self.need_polygon, command=self.fill_polyline)
        self.lbl_vertexes_count = tk.Label(self.fr_menu, text="Количество вершин в \nупрощенной ломаной: ")

        self.lbl_count.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        self.ent_count.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        self.btn_generate.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        self.lbl_algo.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        self.cb_draw_main.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        self.cb_equidistant.grid(row=5, column=0, sticky="ew", padx=5, pady=10)
        self.cb_segmentation.grid(row=6, column=0, sticky="ew", padx=5, pady=10)
        self.cb_simplify.grid(row=7, column=0, sticky="ew", padx=5, pady=10)
        self.cb_smoothing.grid(row=8, column=0, sticky="ew", padx=5, pady=10)
        self.lbl_others.grid(row=9, column=0, sticky="ew", padx=5, pady=5)
        self.cb_polygon.grid(row=10, column=0, sticky="ew", padx=5, pady=10)
        self.lbl_vertexes_count.grid(row=11, column=0, sticky="ew", padx=5, pady=20)

        self.fr_menu.grid(row=0, column=0, sticky="ns")
        self.cvs_graphics.grid(row=0, column=1, sticky="nsew")

        self.main_line = None
        self.equidistant = None
        self.segmentation = None
        self.simplified = None
        self.smoothed = None

    def run_generate_line(self, _):
        self.to_draw_main.set(1)
        self.to_equidistant.set(0)
        self.to_make_segmentation.set(0)
        self.to_simplify.set(0)
        self.to_smooth.set(0)
        self.need_polygon.set(0)
        self.cvs_graphics.delete("all")
        self.main_line = generate_line(int(self.ent_count.get()))
        self.equidistant = equidistant_polyline(self.main_line)
        self.segmentation = make_segmentation(self.equidistant, params.N_INIT, params.N_P, params.N_S, params.F)
        self.simplified = simplify(copy.deepcopy(self.segmentation), params.C, params.k, params.m, params.c_h)
        self.smoothed = smoothed_polyline(self.simplified)
        self.lbl_vertexes_count["text"] = f"Количество вершин в \nупрощенной ломаной: {self.smoothed.elements_count}"
        self.main_line.draw(self.cvs_graphics)

    def fill_polyline(self):
        if self.need_polygon.get() == 0:
            self.run_main_algo()
        else:
            polygon = copy.deepcopy(self.main_line.polyline)
            polygon.append([self.main_line.polyline[0][0],
                            self.main_line.polyline[self.main_line.elements_count - 1][1]])
            self.cvs_graphics.create_polygon(polygon, outline="black", fill="black")

    def run_main_algo(self):
        self.cvs_graphics.delete("all")
        if self.to_draw_main.get() != 0:
            self.main_line.draw(self.cvs_graphics)
        if self.to_equidistant.get() != 0:
            self.equidistant.draw(self.cvs_graphics)
        if self.to_smooth.get() != 0:
            self.smoothed.draw(self.cvs_graphics)
        if self.to_make_segmentation.get() != 0:
            for segment in self.segmentation:
                segment.draw(self.cvs_graphics)
        if self.to_simplify.get() != 0:
            self.simplified.draw(self.cvs_graphics)


if __name__ == '__main__':
    app = App()
    app.title("Упрощение ломаных линий")
    app.rowconfigure(0, minsize=1080, weight=1)
    app.columnconfigure(1, minsize=1920, weight=1)
    app.mainloop()
