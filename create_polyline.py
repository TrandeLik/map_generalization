from polyline import Polyline
import random
import math
import copy
from geometry import *

MIN_X = 100
MIN_Y = 100
MAX_X = 1400
MAX_Y = 1200
C = 0.5
GENERATION_COEF = 0.25


def generate(arr, max_depth, current, a_x, a_y, b_x, b_y):
    if current == max_depth:
        return
    current += 1
    delta_x = int(GENERATION_COEF * (max(a_x, b_x) - min(a_x, b_x)))
    c_x = random.randint(min(a_x, b_x) + delta_x, max(a_x, b_x) - delta_x)
    delta_y = int(GENERATION_COEF * (max(a_y, b_y) - min(a_y, b_y)))
    c_y = random.randint(min(a_y, b_y) + delta_y, max(a_y, b_y) - delta_y)
    arr.append([c_x, c_y])
    generate(arr, max_depth, current, c_x, c_y, b_x, b_y)
    generate(arr, max_depth, current, a_x, a_y, c_x, c_y)


def generate_line(count):
    height = int(math.log2(count)) + 1
    main_line = Polyline("black", count, 3)
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
    return main_line


def equidistant_polyline(polyline):
    equidistant = Polyline("green", polyline.elements_count, 3)
    equidistant.polyline.append(copy.deepcopy(polyline.polyline[0]))
    r = polyline.step(C)
    current_center_pos = 0
    current_segment_number = 1
    corresponding_segment = 1
    while current_segment_number != polyline.elements_count:
        contenders = intersection_of_circle_and_segment(
                            equidistant.polyline[current_center_pos], r,
                            polyline.polyline[current_segment_number - 1],
                            polyline.polyline[current_segment_number])
        if len(contenders) == 0:
            current_segment_number += 1
        if len(contenders) == 1:
            if corresponding_segment == current_segment_number:
                d1 = distance(contenders[0], polyline.polyline[current_segment_number - 1])
                d2 = distance(equidistant.polyline[current_center_pos], polyline.polyline[current_segment_number - 1])
                if d1 > d2 + EPS:
                    equidistant.polyline.append(copy.deepcopy(contenders[0]))
                    current_center_pos += 1
                else:
                    current_segment_number += 1
            else:
                equidistant.polyline.append(copy.deepcopy(contenders[0]))
                current_center_pos += 1
                corresponding_segment = current_segment_number
        if len(contenders) == 2:
            d1 = distance(contenders[0], polyline.polyline[current_segment_number - 1])
            d2 = distance(contenders[1], polyline.polyline[current_segment_number - 1])
            if d1 > d2 + EPS:
                equidistant.polyline.append(copy.deepcopy(contenders[0]))
            else:
                equidistant.polyline.append(copy.deepcopy(contenders[1]))
            current_center_pos += 1
            corresponding_segment = current_segment_number

    if distance(equidistant.polyline[current_center_pos], polyline.polyline[polyline.elements_count - 1]) > EPS:
        equidistant.polyline.append(copy.deepcopy(polyline.polyline[polyline.elements_count - 1]))

    equidistant.elements_count = len(equidistant.polyline)
    return equidistant


def smoothed_polyline(polyline):
    smoothed = Polyline("red", polyline.elements_count, 3)
    smoothed.polyline.append(copy.deepcopy(polyline.polyline[0]))
    for i in range(1, polyline.elements_count - 1):
        x = (polyline.polyline[i - 1][0] + 4 * polyline.polyline[i][0] + polyline.polyline[i + 1][0]) / 6
        y = (polyline.polyline[i - 1][1] + 4 * polyline.polyline[i][1] + polyline.polyline[i + 1][1]) / 6
        smoothed.polyline.append([x, y])
    smoothed.polyline.append(copy.deepcopy(polyline.polyline[polyline.elements_count - 1]))
    return smoothed
