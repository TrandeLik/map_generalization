import copy
import tkinter as tk
from create_polyline import *


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.cvs_graphics = tk.Canvas(self, background="white")
        self.fr_menu = tk.Frame(self)
        self.lbl_count = tk.Label(self.fr_menu, text="Количество звеньев ломаной:")
        self.ent_count = tk.Entry(self.fr_menu)
        self.btn_generate = tk.Button(self.fr_menu, text="Сгенерировать")
        self.btn_generate.bind("<Button-1>", self.run_generate_line)
        self.lbl_algo = tk.Label(self.fr_menu, text="Этапы генерализации")
        self.to_equidistant = tk.IntVar()
        self.cb_equidistant = tk.Checkbutton(self.fr_menu, text="Привести к равнозвенной", variable=self.to_equidistant,
                                             command=self.run_main_algo)
        self.to_smooth = tk.IntVar()
        self.cb_smoothing = tk.Checkbutton(self.fr_menu, text="Сгладить", variable=self.to_smooth,
                                           command=self.run_main_algo)
        self.need_polygon = tk.IntVar()
        self.cb_polygon = tk.Checkbutton(self.fr_menu, text="Залить", variable=self.need_polygon,
                                         command=self.fill_polyline)

        self.lbl_count.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.ent_count.grid(row=1, column=0, sticky="ew", padx=5)
        self.btn_generate.grid(row=2, column=0, sticky="ew", padx=5)
        self.lbl_algo.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.cb_equidistant.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        self.cb_smoothing.grid(row=5, column=0, sticky="ew", padx=5, pady=10)
        self.cb_polygon.grid(row=6, column=0, sticky="ew", padx=5, pady=10)

        self.fr_menu.grid(row=0, column=0, sticky="ns")
        self.cvs_graphics.grid(row=0, column=1, sticky="nsew")

        self.main_line = None

    def run_generate_line(self, event):
        self.need_polygon.set(0)
        self.to_smooth.set(0)
        self.to_equidistant.set(0)
        self.cvs_graphics.delete("all")
        self.main_line = generate_line(int(self.ent_count.get()))
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
        self.main_line.draw(self.cvs_graphics)
        equidistant = equidistant_polyline(self.main_line)
        smoothed = smoothed_polyline(equidistant)
        if self.to_equidistant.get() != 0:
            equidistant.draw(self.cvs_graphics)
        if self.to_smooth.get() != 0:
            smoothed.draw(self.cvs_graphics)


if __name__ == '__main__':
    app = App()
    app.title("Polyline generalization")
    app.rowconfigure(0, minsize=1080, weight=1)
    app.columnconfigure(1, minsize=1920, weight=1)
    app.mainloop()
