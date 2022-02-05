from polyline import Polyline
import random
import math
import copy
from geometry import *
from algorithm_params import params


def generate(arr, max_depth, current, a_x, a_y, b_x, b_y):
    if current == max_depth:
        return
    current += 1
    delta_x = int(params.GENERATION_RATIO * (max(a_x, b_x) - min(a_x, b_x)))
    c_x = random.randint(min(a_x, b_x) + delta_x, max(a_x, b_x) - delta_x)
    delta_y = int(params.GENERATION_RATIO * (max(a_y, b_y) - min(a_y, b_y)))
    c_y = random.randint(min(a_y, b_y) + delta_y, max(a_y, b_y) - delta_y)
    arr.append([c_x, c_y])
    generate(arr, max_depth, current, c_x, c_y, b_x, b_y)
    generate(arr, max_depth, current, a_x, a_y, c_x, c_y)


def generate_line(count):
    height = int(math.log2(count)) + 1
    main_line = Polyline("black", count, 3)
    main_line.polyline.append([params.MIN_X, params.MIN_Y])
    main_line.polyline.append([params.MAX_X, params.MAX_Y])
    generate(main_line.polyline, height, 0, params.MIN_X, params.MIN_Y, params.MAX_X, params.MAX_Y)
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
    r = polyline.step(params.C)
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
                if d1 > d2 + params.EPS:
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
            if d1 > d2 + params.EPS:
                equidistant.polyline.append(copy.deepcopy(contenders[0]))
            else:
                equidistant.polyline.append(copy.deepcopy(contenders[1]))
            current_center_pos += 1
            corresponding_segment = current_segment_number

    if distance(equidistant.polyline[current_center_pos], polyline.polyline[polyline.elements_count - 1]) > params.EPS:
        equidistant.polyline.append(copy.deepcopy(polyline.polyline[polyline.elements_count - 1]))

    equidistant.elements_count = len(equidistant.polyline)
    return equidistant


def make_segmentation(polyline, n, n_p, n_s, f):
    segmentation = polyline.split(n)
    min_len_index = 0
    for i in range(len(segmentation)):
        segmentation[i].update_integral_characteristic(f)
        if len(segmentation[i].polyline) < len(segmentation[min_len_index].polyline):
            min_len_index = i
    while len(segmentation[min_len_index].polyline) < n_p or len(segmentation) > n_s:
        min_ch_diff_idx = 0
        for i in range(len(segmentation) - 1):
            if abs(segmentation[i].integral_characteristic - segmentation[i + 1].integral_characteristic) < abs(segmentation[min_ch_diff_idx].integral_characteristic - segmentation[min_ch_diff_idx + 1].integral_characteristic):
                min_ch_diff_idx = i
        segmentation[min_ch_diff_idx].merge(segmentation[min_ch_diff_idx + 1], f)
        segmentation.pop(min_ch_diff_idx + 1)
        min_len_index = 0
        for i in range(len(segmentation)):
            print(len(segmentation[i].polyline))
            if len(segmentation[i].polyline) < len(segmentation[min_len_index].polyline):
                min_len_index = i
    return segmentation


def smoothed_polyline(polyline):
    smoothed = Polyline("red", polyline.elements_count, 3)
    smoothed.polyline.append(copy.deepcopy(polyline.polyline[0]))
    for i in range(1, polyline.elements_count - 1):
        x = (polyline.polyline[i - 1][0] + 4 * polyline.polyline[i][0] + polyline.polyline[i + 1][0]) / 6
        y = (polyline.polyline[i - 1][1] + 4 * polyline.polyline[i][1] + polyline.polyline[i + 1][1]) / 6
        smoothed.polyline.append([x, y])
    smoothed.polyline.append(copy.deepcopy(polyline.polyline[polyline.elements_count - 1]))
    return smoothed
