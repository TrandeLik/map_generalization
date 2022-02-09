from algorithm_params import params
import numpy as np


def distance(a, b):
    return ((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])) ** 0.5


def is_dot_between(dot, first, second):
    return min(first[0], second[0]) - params.EPS <= dot[0] <= max(first[0], second[0]) + params.EPS and min(first[1], second[1]) - params.EPS <= dot[1] <= max(first[1], second[1]) + params.EPS

def line_equation(p, q):
    a = p[1] - q[1]
    b = q[0] - p[0]
    c = - a * p[0] - b * p[1]
    return a, b, c


def move_center(dot, new_center):
    return [dot[0] - new_center[0], dot[1] - new_center[1]]


def intersection_of_circle_and_line_centered(r, a, b, c):
    x0 = -a * c / (a * a + b * b)
    y0 = -b * c / (a * a + b * b)
    if c * c > r * r * (a * a + b * b) + params.EPS:
        return []
    if abs(c * c - r * r * (a * a + b * b)) < params.EPS:
        return [[x0, y0]]
    d = r * r - c * c / (a * a + b * b)
    mult = (d / (a * a + b * b)) ** 0.5
    ax = x0 + b * mult
    bx = x0 - b * mult
    ay = y0 - a * mult
    by = y0 + a * mult
    return [[ax, ay], [bx, by]]


def intersection_of_circle_and_segment(centre, r, p, q):
    p_new = move_center(p, centre)
    q_new = move_center(q, centre)
    a, b, c = line_equation(p_new, q_new)
    intersection_points = intersection_of_circle_and_line_centered(r, a, b, c)
    result = []
    for dot in intersection_points:
        if is_dot_between(dot, p_new, q_new):
            result.append(move_center(dot, [-centre[0], -centre[1]]))
    return result


def distance_between_dot_and_line(dot, a, b, c):
    return abs(a * dot[0] + b * dot[1] + c) / ((a * a + b * b) ** 0.5)


def douglas_packer_algorithm(dots, h, first, second):
    dots[first][2] = True
    dots[second][2] = True
    max_dist_idx = first
    a, b, c = line_equation(dots[first], dots[second])
    for i in range(first, second):
        if distance_between_dot_and_line(dots[i], a, b, c) > distance_between_dot_and_line(dots[max_dist_idx], a, b, c) + params.EPS:
            max_dist_idx = i
    if distance_between_dot_and_line(dots[max_dist_idx], a, b, c) > h + params.EPS:
        douglas_packer_algorithm(dots, h, first, max_dist_idx)
        douglas_packer_algorithm(dots, h, max_dist_idx, second)
    return dots


def det(a, b, c, d):
    return a * d - b * c


def lines_intersection(a1, b1, c1, a2, b2, c2):
    zn = det(a1, b1, a2, b2)
    if abs(zn) < params.EPS:
        return []
    x = -det(c1, b1, c2, b2) / zn
    y = -det(a1, c1, a2, c2) / zn
    return [x, y]


def are_lines_equivalent(a1, b1, c1, a2, b2, c2):
    return abs(det(a1, b1, a2, b2)) < params.EPS and abs(det(a1, c1, a2, c2)) < params.EPS and abs(det(b1, c1, b2, c2)) < params.EPS


def segments_intersection(first_p, first_q, second_p, second_q):
    a1, b1, c1 = line_equation(first_p, first_q)
    a2, b2, c2 = line_equation(second_p, second_q)
    if are_lines_equivalent(a1, b1, c1, a2, b2, c2):
        return True, []
    dot = lines_intersection(a1, b1, c1, a2, b2, c2)
    if len(dot) == 0:
        return False, []
    if is_dot_between(dot, first_p, first_q) and is_dot_between(dot, second_p, second_q):
        return False, dot
    return False, []


def least_square_method(dots):
    a = np.zeros(len(dots))
    b = np.zeros(len(dots))
    for i in range(len(dots)):
        a[i] = dots[i][0]
        b[i] = dots[i][1]
    a = np.vstack([a, np.ones(len(a))]).T
    k, _ = np.linalg.lstsq(a, b, rcond=None)[0]
    return k
