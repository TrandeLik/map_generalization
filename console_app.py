from create_polyline import *
from algorithm_params import params
import copy
from polyline import Polyline


def write_polyline_to_file(polyline, filename):
    f = open(filename, 'w')
    for dot in polyline.polyline:
        f.write(f'({dot[0]}, {dot[1]})\n')
    f.close()


def read_polyline_from_file(filename):
    f = open(filename, 'r')
    polyline_main = Polyline("black", 0, 3)
    for line in f:
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace(',', '')
        dot = line.split()
        polyline_main.polyline.append([float(dot[0]), float(dot[1])])
    polyline_main.elements_count = len(polyline_main.polyline)
    return polyline_main


print("Здравстуйте! Это приложение по упрощению ломаных.\n "
      "Убедитесь, что Вы правильно настроили файл generalization_settings.ini, иначе программа может не сработать "
      "или сработать некорректно")
print("============================================================")
print("Введите 1, чтобы считать ломаную из файла, 2, чтобы сгенерировать случайную ломаную:")
input_type = -1
while input_type != 1 and input_type != 2:
    input_type = int(input())
main_line = None
if input_type == 1:
    print("Убедитесь, что файл заполнен корректно и введите название файла:")
    input_filename = input()
    main_line = read_polyline_from_file(input_filename)
else:
    print("Введите количество звеньев в ломаной:")
    n = int(input())
    main_line = generate_line(n)
print("Введите имя выходного файла:")
output_filename = input()
print("Ожидайте завершение алгоритма!")
equidistant = equidistant_polyline(main_line)
segmentation = make_segmentation(equidistant, params.N_INIT, params.N_P, params.N_S, params.F)
simplified = simplify(copy.deepcopy(segmentation), params.h)
smoothed = smoothed_polyline(simplified)
write_polyline_to_file(smoothed, output_filename)
print(f"Работа завершена! В исходной ломаной - {len(main_line.polyline)} звеньев, в упрощенной - "
      f"{len(smoothed.polyline)}\n"
      f"Полученная ломаная сохранена в файле {output_filename}")
