class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

class Triangle:
    def __init__(self, id, a: Point, b: Point, c: Point):
        self.id = id
        self.vertices = [a, b, c]
        if self.area() == 0: raise ValueError(f"Треугольник '{id}' является вырожденным (все точки на одной прямой).")

    def area(self):
        a = self.distance(self.vertices[0], self.vertices[1])
        b = self.distance(self.vertices[1], self.vertices[2])
        c = self.distance(self.vertices[2], self.vertices[0])
        s = (a + b + c) / 2
        areal = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        return areal

    def distance(self, p1: Point, p2: Point):
        return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5

    def move(self, dx, dy):
        for i in self.vertices:
            i.x += dx
            i.y += dy

    def __str__(self):
        return f"Триугольник '{self.id}': {self.vertices[0]}, {self.vertices[1]}, {self.vertices[2]}"

class Rectangle:
    def __init__(self, id, topLeft: Point, width, height):
        if width <= 0 or height <= 0: raise ValueError(f"Прямоугольник '{id}' не может иметь неположительные ширину или высоту ({width}, {height}).")
        self.id = id
        self.topLeft = topLeft
        self.width = width
        self.height = height

    def area(self):
        areal = self.width * self.height
        return areal

    def move(self, dx, dy):
        self.topLeft.x += dx
        self.topLeft.y += dy

    def __str__(self):
        return f"Прямоугольник '{self.id}': top_left{self.topLeft}, width={self.width}, height={self.height}"

def compare(s1, s2):
    area1 = s1.area()
    area2 = s2.area()

    if area1 > area2:
        print(f"Площадь триугольника:({area1}) больше площади прямоугольника:({area2}) на {area1 - area2}")
    elif area1 < area2:
        print(f"Площадь прямоугольника:({area2}) больше площади триугольника:({area1}) на {area2 - area1}")
    else:
        print(f"Площадь триугольника:({area1}) равна площади прямоугольника:({area2})")

def main():
    p1 = Point(0, 0)
    p2 = Point(3, 0)
    p3 = Point(0, 4)
    rect_point = Point(5, 5)
    triangle = Triangle("Tri1", p1, p2, p3)
    rectangle = Rectangle("Rect1", rect_point, -4, 6)

    print("До перемещения:")
    print(triangle)
    print(rectangle)

    triangle.move(2, 3)
    rectangle.move(-1, -1)

    print("\nПосле перемещения:")
    print(triangle)
    print(rectangle)

    print("\nРезультат сравнения:")
    result = compare(triangle, rectangle)
    print(result)

if __name__ == "__main__":
    main()