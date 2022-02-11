import copy

from geometry import *
import math


class Polyline:
    def __init__(self, color, elements_count, width):
        self.color = color
        self.elements_count = elements_count
        self.polyline = []
        self.width = width
        self.integral_characteristic = 0

    def draw(self, canvas):
        for i in range(0, self.elements_count - 1):
            canvas.create_line(int(self.polyline[i][0]), int(self.polyline[i][1]),
                               int(self.polyline[i + 1][0]), int(self.polyline[i + 1][1]),
                               fill=self.color, width=self.width)
        self.draw_vertex(0, canvas)
        self.draw_vertex(self.elements_count - 1, canvas)

    def draw_vertex(self, i, canvas):
        canvas.create_oval(self.polyline[i][0] - 4, self.polyline[i][1] - 4,
                           self.polyline[i][0] + 4, self.polyline[i][1] + 4, fill=self.color, width=1)

    def step(self, c):
        d_in = 0
        for i in range(self.elements_count - 1):
            d_in += distance(self.polyline[i], self.polyline[i - 1])
        d_in /= self.elements_count - 1
        return c * d_in

    def angle_adittion(self, i, p):
        if i == 0 or i == self.elements_count - 1:
            return 0
        tmp = (self.polyline[i + 1][0] - self.polyline[i][0]) * (self.polyline[i][0] - self.polyline[i - 1][0])
        tmp += (self.polyline[i + 1][1] - self.polyline[i][1]) * (self.polyline[i][1] - self.polyline[i - 1][1])
        return math.acos(round(tmp / p, params.DIGITS_COUNT))

    def full_variation(self):
        c = 0
        p = distance(self.polyline[0], self.polyline[1]) ** 2
        for i in range(self.elements_count):
            c += self.angle_adittion(i, p)
        return c / (2 * math.pi)

    def is_vertex_extremal(self, i, p):
        if 0 < i < self.elements_count - 1:
            if (self.angle_adittion(i, p) > self.angle_adittion(i - 1, p)
                and self.angle_adittion(i, p) > self.angle_adittion(i + 1, p)) \
                    or (self.angle_adittion(i, p) < self.angle_adittion(i - 1, p)
                        and self.angle_adittion(i, p) < self.angle_adittion(i + 1, p)):
                return True
        return False

    def extremal_vertexes(self):
        e = 0
        p = distance(self.polyline[0], self.polyline[1]) ** 2
        for i in range(1, self.elements_count - 1):
            if self.is_vertex_extremal(i, p):
                e += 1
        return e

    def update_integral_characteristic(self, f):
        self.integral_characteristic = self.full_variation() + f * self.extremal_vertexes()

    def merge(self, second_polyline, f):
        last_dot = self.elements_count - 1
        p = distance(self.polyline[0], self.polyline[1]) ** 2
        self.elements_count += second_polyline.elements_count - 1
        self.polyline += copy.deepcopy(second_polyline.polyline[1:])
        if self.is_vertex_extremal(last_dot - 1, p):
            self.integral_characteristic -= f
        self.integral_characteristic += second_polyline.integral_characteristic
        if second_polyline.is_vertex_extremal(second_polyline.elements_count - 2, p):
            self.integral_characteristic -= f
        for dot in range(last_dot - 1, last_dot + 1):
            if 1 <= dot < self.elements_count - 1:
                if self.is_vertex_extremal(dot, p):
                    self.integral_characteristic += f

    def split(self, n):
        splitted = [Polyline(self.color, 0, self.width) for _ in range(n)]
        el_in_splitted = max(math.ceil(self.elements_count / n), 1)
        j = 0
        for i in range(0, self.elements_count, el_in_splitted):
            if i != 0:
                splitted[j].polyline = copy.deepcopy(self.polyline[i - 1:i + el_in_splitted])
            else:
                splitted[j].polyline = copy.deepcopy(self.polyline[i:i + el_in_splitted])
            splitted[j].elements_count = len(splitted[j].polyline)
            j += 1
        dirt_length = len(splitted)
        for i in range(dirt_length - 1, j - 1, -1):
            splitted.pop(i)
        for i in range(j - 1, 0, -1):
            if len(splitted[i].polyline) < 3:
                splitted[i - 1].polyline += splitted[i].polyline[1:]
                splitted[i - 1].elements_count = len(splitted[i - 1].polyline)
                splitted.pop(i)
        if len(splitted[0].polyline) < 3:
            splitted[0].polyline += splitted[1].polyline[1:]
            splitted[0].elements_count = len(splitted[0].polyline)
            splitted.pop(1)
        return splitted

    def fractal_dimension(self, c, k):
        delta = self.step(c)
        dimensions = []
        for i in range(1, k + 1):
            dimensions.append([math.log2(i * delta), math.log2(box_counting(self.polyline, i * delta))])
        return -least_square_method(dimensions)

    def simplify(self, h):
        dots = []
        for dot in self.polyline:
            dots.append([dot[0], dot[1], False])
        updated_dots = douglas_packer_algorithm(dots, h, 0, len(dots) - 1)
        self.polyline = []
        for dot in updated_dots:
            if dot[2]:
                self.polyline.append([dot[0], dot[1]])
        self.elements_count = len(self.polyline)
