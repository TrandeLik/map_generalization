from polyline import Polyline
import random
import math
from geometry import *

MIN_X = 100
MIN_Y = 100
MAX_X = 1400
MAX_Y = 1200


def generate(arr, max_depth, current, a_x, a_y, b_x, b_y):
    if current == max_depth:
        return
    current += 1
    EPS = 0.25
    delta_x = int(EPS * (max(a_x, b_x) - min(a_x, b_x)))
    c_x = random.randint(min(a_x, b_x) + delta_x, max(a_x, b_x) - delta_x)
    delta_y = int(EPS * (max(a_y, b_y) - min(a_y, b_y)))
    c_y = random.randint(min(a_y, b_y) + delta_y, max(a_y, b_y) - delta_y)
    arr.append([c_x, c_y])
    generate(arr, max_depth, current, c_x, c_y, b_x, b_y)
    generate(arr, max_depth, current, a_x, a_y, c_x, c_y)


def generate_line(count):
    height = int(math.log2(count)) + 1
    main_line = Polyline("black", count)
    main_line.polyline.append([MIN_X, MIN_Y])
    main_line.polyline.append([MAX_X, MAX_Y])
    generate(main_line.polyline, height, 0, MIN_X, MIN_Y, MAX_X, MAX_Y)
    main_line.polyline.sort(key=lambda x: x[0])
    n = len(main_line.polyline)
    dist = [[0, i] for i in range(n)]
    for i in range(1, n - 1):
        dist[i][0] = distance(main_line.polyline[i], main_line.polyline[i - 1])
    dist.sort(key=lambda x: x[0])
    for_deletion = dist[:n - main_line.elements_count]
    for_deletion.sort(key=lambda x: x[1], reverse=True)
    for i in range(n - main_line.elements_count):
        main_line.polyline.pop(for_deletion[i][1])
    main_line.update_limits()
    return main_line

