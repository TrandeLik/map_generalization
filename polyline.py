from geometry import *


class Polyline:
    def __init__(self, color, elements_count, width):
        self.color = color
        self.elements_count = elements_count
        self.polyline = []
        self.width = width

    def draw(self, canvas):
        for i in range(0, self.elements_count - 1):
            canvas.create_line(int(self.polyline[i][0]), int(self.polyline[i][1]),
                               int(self.polyline[i + 1][0]), int(self.polyline[i + 1][1]),
                               fill=self.color, width=self.width)
            canvas.create_oval(self.polyline[i][0] - 3, self.polyline[i][1] - 3,
                               self.polyline[i][0] + 3, self.polyline[i][1] + 3, fill=self.color, width=1)
        canvas.create_oval(self.polyline[self.elements_count - 1][0] - 3, self.polyline[self.elements_count - 1][1] - 3,
                           self.polyline[self.elements_count - 1][0] + 3, self.polyline[self.elements_count - 1][1] + 3,
                           fill=self.color, width=1)

    def step(self, c):
        d_in = 0
        for i in range(self.elements_count - 1):
            d_in += distance(self.polyline[i], self.polyline[i - 1])
        d_in /= self.elements_count - 1
        return c * d_in
