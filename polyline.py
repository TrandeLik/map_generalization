class Polyline:
    def __init__(self, color, elements_count):
        self.color = color
        self.elements_count = elements_count
        self.polyline = []

    def draw(self, canvas):
        for i in range(0, self.elements_count - 1):
            canvas.create_line(self.polyline[i][0], self.polyline[i][1],
                               self.polyline[i + 1][0], self.polyline[i + 1][1], fill=self.color, width=3)
