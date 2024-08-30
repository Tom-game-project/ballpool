import math

class vector2D:

    def __init__(self, x: float, y: float):
        self._x: float = x
        self._y: float = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def abspow2(self):
        return pow(self._x, 2)+pow(self._y, 2)

    def __abs__(self):
        return math.sqrt(pow(self._x, 2)+pow(self._y, 2))

    def __add__(self, other) -> "vector2D":
        if type(other) is vector2D:
            return vector2D(self.x+other.x, self.y+other.y)
        else:
            raise BaseException("vector2D同士で計算してください")

    def __sub__(self, other) -> "vector2D":
        if type(other) is vector2D:
            return vector2D(self.x-other.x, self.y-other.y)
        else:
            raise BaseException("vector2D同士で計算してください")

    def __mul__(self, other):
        if type(other) is vector2D:
            return self.x*other.x+self.y*other.y
        elif (type(other) is int) or (type(other) is float):
            return vector2D(self.x*other, self.y*other)

    def __rmul__(self, other):
        if type(other) is vector2D:
            return self.x*other.x+self.y*other.y
        elif (type(other) is int) or (type(other) is float):
            return vector2D(self.x*other, self.y*other)

    def __truediv__(self, other) -> "vector2D":
        if (type(other) is int) or (type(other) is float):
            return vector2D(self.x/other, self.y/other)
        else:
            raise BaseException("型が正しくありません")

    def __repr__(self) -> str:
        return f"vector2D({self.x},{self.y})"
