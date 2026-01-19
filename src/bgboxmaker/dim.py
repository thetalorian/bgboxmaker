from typing import TypeVar, cast
"""Collection of various helper classes."""
T = TypeVar('T', int, float)

class Vec2:
    def __init__(self, value : list[int] = [0,0]):
        self.x = int(value[0])
        self.y = int(value[1])
    def __mul__(self, a : int):
        return Vec2([self.x * a, self.y * a])
    def __eq__(self,a):
        return self.x == a.x and self.y == a.y
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)
    def __iter__(self):
        yield self.x
        yield self.y


class Dim(list[T]):
    def __init__(self, *args):
        inputs : list[T] = list(args)
        if len(inputs) > 0 and isinstance(inputs[0], list):
            inputs = inputs[0]
        while len(inputs) < 3:
            inputs.append(cast(T, 0))
        super().__init__(inputs)

    @property
    def x(self) -> T:
        return self[0]
    @x.setter
    def x(self, value: T) -> None:
        self[0] = value
    @property
    def w(self) -> T:
        return self[0]
    @w.setter
    def w(self, value : T) -> None:
        self[0] = value
    @property
    def y(self) -> T:
        return self[1]
    @y.setter
    def y(self, value: T) -> None:
        self[1] = value
    @property
    def h(self) -> T:
        return self[1]
    @h.setter
    def h(self, value : T) -> None:
        self[1] = value
    @property
    def z(self) -> T:
        return self[2]
    @z.setter
    def z(self, value: T) -> None:
        self[2] = value
    @property
    def d(self) -> T:
        return self[2]
    @d.setter
    def d(self, value : T) -> None:
        self[2] = value

    @property
    def wh(self) -> tuple[T, T]:
        return (self[0], self[1])

    @property
    def xy(self) -> tuple[T, T]:
        return (self[0], self[1])



    def __mul__(self, value : T):
        newDim = Dim()
        for i in range(0, len(self)):
            newDim[i] = cast(T, self[i] * value)
        return newDim

    def as_ints(self):
        newDim = Dim()
        for i in range(0, len(self)):
            newDim[i] = int(self[i])
        return newDim

class Vec3:
    def __init__(self, value : list[int] = [0, 0, 0]):
        self.x = int(value[0])
        self.y = int(value[1])
        self.z = int(value[2])
    def __mul__(self, a):
        return Vec3([self.x * a, self.y * a, self.z * a])
    def __eq__(self, a):
        return self.x == a.x and self.y == a.y and self.z == a.z
    def __str__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


