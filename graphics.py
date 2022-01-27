import math
import tkinter as tk
from polyline import Polyline
import random

main_line = None


def generate(arr, max_depth, current, a_x, a_y, b_x, b_y):
    if current == max_depth:
        return
    current += 1
    eps = 0.25
    delta_x = int(eps * (max(a_x, b_x) - min(a_x, b_x)))
    c_x = random.randint(min(a_x, b_x) + delta_x, max(a_x, b_x) - delta_x)
    delta_y = int(eps * (max(a_y, b_y) - min(a_y, b_y)))
    c_y = random.randint(min(a_y, b_y) + delta_y, max(a_y, b_y) - delta_y)
    arr.append([c_x, c_y])
    generate(arr, max_depth, current, c_x, c_y, b_x, b_y)
    generate(arr, max_depth, current, a_x, a_y, c_x, c_y)


def generate_line(event):
    count = int(ent_count.get())
    global main_line
    global cvs_graphics
    height = int(math.log2(count)) + 1
    cvs_graphics.delete("all")
    main_line = Polyline("black", count)
    main_line.polyline.append([100, 100])
    main_line.polyline.append([1400, 1200])
    generate(main_line.polyline, height, 0, 100, 100, 1400, 1200)
    main_line.polyline.sort(key=lambda x: x[0])
    n = len(main_line.polyline)
    dist = [[0, i] for i in range(n)]
    for i in range(1, n - 1):
        dist[i][0] = (main_line.polyline[i][0] - main_line.polyline[i - 1][0]) ** 2 +\
                  (main_line.polyline[i][1] - main_line.polyline[i - 1][1]) ** 2
    dist.sort(key=lambda x: x[0])
    for_deletion = dist[:n - main_line.elements_count]
    for_deletion.sort(key=lambda x: x[1], reverse=True)
    for i in range(n - main_line.elements_count):
        main_line.polyline.pop(for_deletion[i][1])
    main_line.draw(cvs_graphics)



def main():
    window = tk.Tk()
    window.rowconfigure(0, minsize=1080, weight=1)
    window.columnconfigure(1, minsize=1920, weight=1)
    global cvs_graphics
    cvs_graphics = tk.Canvas(window, background="white")
    fr_menu = tk.Frame(window)
    lbl_count = tk.Label(fr_menu, text="Количество звеньев ломаной:")
    global ent_count
    ent_count = tk.Entry(fr_menu)
    btn_generate = tk.Button(fr_menu, text="Сгенерировать")
    btn_generate.bind("<Button-1>", generate_line)

    lbl_count.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    ent_count.grid(row=1, column=0, sticky="ew", padx=5)
    btn_generate.grid(row=2, column=0, sticky="ew", padx=5)

    fr_menu.grid(row=0, column=0, sticky="ns")
    cvs_graphics.grid(row=0, column=1, sticky="nsew")

    window.mainloop()


if __name__ == '__main__':
    main()

