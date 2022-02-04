from algorithm_params import params


def distance(a, b):
    return ((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])) ** 0.5


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
        if min(p_new[0], q_new[0]) - params.EPS <= dot[0] <= max(p_new[0], q_new[0]) + params.EPS and min(p_new[1], q_new[1]) - params.EPS <= dot[1] <= max(p_new[1], q_new[1]) + params.EPS:
            result.append(move_center(dot, [-centre[0], -centre[1]]))
    return result
