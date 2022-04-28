import tkinter as tk
from logic.create_polyline import *
from settings.algorithm_params import params


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.cvs_graphics = tk.Canvas(self, background="white")
        self.fr_menu = tk.Frame(self)
        self.lbl_count = tk.Label(self.fr_menu, text="Number of vertexes in\nthe generated polyline:")
        self.ent_count = tk.Entry(self.fr_menu)
        self.btn_generate = tk.Button(self.fr_menu, text="Generate polyline")
        self.btn_generate.bind("<Button-1>", self.run_generate_line)
        self.lbl_algo = tk.Label(self.fr_menu, text="Display the following lines:")
        self.to_draw_main = tk.IntVar()
        self.cb_draw_main = tk.Checkbutton(self.fr_menu, text="Main line",
                                           variable=self.to_draw_main, command=self.draw_polylines)
        self.to_equidistant = tk.IntVar()
        self.cb_equidistant = tk.Checkbutton(self.fr_menu, text="Equidistant",
                                             variable=self.to_equidistant, command=self.draw_polylines)
        self.to_make_segmentation = tk.IntVar()
        self.cb_segmentation = tk.Checkbutton(self.fr_menu, text="Segmentation",
                                              variable=self.to_make_segmentation, command=self.draw_polylines)
        self.to_simplify = tk.IntVar()
        self.cb_simplify = tk.Checkbutton(self.fr_menu, text="Simplified polyline",
                                          variable=self.to_simplify, command=self.draw_polylines)
        self.to_smooth = tk.IntVar()
        self.cb_smoothing = tk.Checkbutton(self.fr_menu, text="Smoothed polyline",
                                           variable=self.to_smooth, command=self.draw_polylines)
        self.need_polygon = tk.IntVar()
        self.lbl_vertexes_count = tk.Label(self.fr_menu, text="Number of vertices in\n simplified polyline: ")
        self.lbl_others = tk.Label(self.fr_menu, text="Other options")
        self.file_name = tk.Entry(self.fr_menu)
        self.btn_file = tk.Button(self.fr_menu, text="Read polyline from file")
        self.btn_file.configure(command=self.line_from_file)

        self.lbl_count.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        self.ent_count.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
        self.btn_generate.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        self.lbl_algo.grid(row=3, column=0, sticky="ew", padx=5, pady=10)
        self.cb_draw_main.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        self.cb_equidistant.grid(row=5, column=0, sticky="ew", padx=5, pady=10)
        self.cb_segmentation.grid(row=6, column=0, sticky="ew", padx=5, pady=10)
        self.cb_simplify.grid(row=7, column=0, sticky="ew", padx=5, pady=10)
        self.cb_smoothing.grid(row=8, column=0, sticky="ew", padx=5, pady=10)
        self.lbl_vertexes_count.grid(row=11, column=0, sticky="ew", padx=5, pady=20)
        self.lbl_others.grid(row=12, column=0, sticky="ew", padx=5, pady=5)
        self.file_name.grid(row=14, column=0, sticky="ew", padx=5, pady=10)
        self.btn_file.grid(row=15, column=0, sticky="ew", padx=5, pady=10)
        self.fr_menu.grid(row=0, column=0, sticky="ns")
        self.cvs_graphics.grid(row=0, column=1, sticky="nsew")
        self.is_from_file = False
        self.main_line = None
        self.equidistant = None
        self.segmentation = None
        self.simplified = None
        self.smoothed = None

    def line_from_file(self):
        self.is_from_file = True
        f = open(self.file_name.get(), 'r')
        polyline_main = Polyline("black", 0, 3)
        for line in f:
            dot = line.split()
            polyline_main.polyline.append([2 * float(dot[0]), 1550 - 2 * float(dot[1])])
        polyline_main.elements_count = len(polyline_main.polyline)
        self.main_line = polyline_main
        self.run()

    def run_generate_line(self, _):
        self.is_from_file = False
        self.run()

    def run(self):
        self.to_draw_main.set(1)
        self.to_equidistant.set(0)
        self.to_make_segmentation.set(0)
        self.to_simplify.set(0)
        self.to_smooth.set(0)
        self.cvs_graphics.delete("all")
        if not self.is_from_file:
            self.main_line = generate_line(int(self.ent_count.get()))
        self.equidistant = equidistant_polyline(self.main_line)
        self.segmentation = make_segmentation(self.equidistant, params.N_INIT, params.N_P, params.N_S, params.F)
        self.simplified = simplify(copy.deepcopy(self.segmentation), params.C, params.k, params.m, params.c_h)
        self.smoothed = smoothed_polyline(self.simplified)
        self.lbl_vertexes_count["text"] = f"Number of vertices in\n simplified polyline: {self.smoothed.elements_count}"
        self.main_line.draw(self.cvs_graphics)

    def draw_polylines(self):
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
    app.title("Polyline simplification")
    app.rowconfigure(0, minsize=1080, weight=1)
    app.columnconfigure(1, minsize=1920, weight=1)
    app.mainloop()
