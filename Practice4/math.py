import math

def deg_to_rad(deg):
    return deg * math.pi / 180


def area_trapezoid(h, a, b):
    return (a + b) * h / 2


def area_regular_polygon(n, s):
    return (n * s * s) / (4 * math.tan(math.pi / n))


def area_parallelogram(base, height):
    return base * height


if __name__ == "__main__":
    print("Radian:", deg_to_rad(15))
    print("Trapezoid:", area_trapezoid(5, 5, 6))
    print("Polygon:", area_regular_polygon(4, 25))
    print("Parallelogram:", area_parallelogram(5, 6))