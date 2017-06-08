from math import sqrt


class Vector3(object):

    __slots__ = ('x', 'y', 'z')

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        result = Vector3()
        if type(other) in [int, float]:
            result.x = self.x * other
            result.y = self.y * other
            result.z = self.z * other
        else:
            #TODO
            print("FIXME: MUL")
            pass
        return result

    def __div__(self, other):
        result = Vector3()
        if other == 0:
            return result
        result.x = self.x / other
        result.y = self.y / other
        result.z = self.z / other
        return result

    def __add__(self, other):
        result = Vector3()
        # Why not: (?)
        # if type(other) in [int, float]:
        #    result.x = self.x + other
        #    result.y = self.y + other
        #    result.z = self.z + other
        # else:
        #    result.x = self.x + other.x
        #    result.y = self.y + other.y
        #    result.z = self.z + other.z
        # because of speed.
        result.x = self.x + other.x
        result.y = self.y + other.y
        result.z = self.z + other.z
        return result

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __rmul__(self, other):
        result = Vector3()
        result.x = self.x * other
        result.y = self.y * other
        result.z = self.z * other
        return result

    # reverse add
    def __radd__(self, other):
        result = Vector3()
        result.x = self.x + other.x
        result.y = self.y + other.y
        result.z = self.z + other.z
        return result

    def __sub__(self, other):
        result = Vector3()
        result.x = self.x - other.x
        result.y = self.y - other.y
        result.z = self.z - other.z
        return result

    def __neg__(self):
        return Vector3() - self

    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def length_squared(self):
        return self.x**2 + self.y**2 + self.z**2

    def normalized(self):
        length = self.length()
        return self / length

    @classmethod
    def from_tuple(cls, some_tuple):
        cls.x = some_tuple[0]
        cls.y = some_tuple[1]
        cls.z = some_tuple[2]

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def __str__(self):
        return "x:\t%s, y:\t%s, z:\t%s" % (self.x, self.y, self.z)

# There we define a shortcut of most commonly used vector object
V = Vector3
