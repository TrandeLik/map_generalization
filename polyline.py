from geometry import *


class Polyline:
    def __init__(self, color, elements_count):
        self.color = color
        self.elements_count = elements_count
        self.polyline = []
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0

    def draw(self, canvas):
        for i in range(0, self.elements_count - 1):
            canvas.create_line(int(self.polyline[i][0]), int(self.polyline[i][1]),
                               int(self.polyline[i + 1][0]), int(self.polyline[i + 1][1]), fill=self.color, width=3)

    def update_limits(self):
        self.min_x = self.polyline[0][0]
        self.min_y = self.polyline[0][1]
        self.max_x = self.polyline[self.elements_count - 1][0]
        self.max_y = self.polyline[self.elements_count - 1][1]

    def step(self, c):
        d_in = 0
        for i in range(self.elements_count - 1):
            d_in += distance(self.polyline[i], self.polyline[i - 1])
        d_in /= self.elements_count - 1
        return c * d_in
