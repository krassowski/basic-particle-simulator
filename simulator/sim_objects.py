from vector import V
from vector import Vector3


class Object(object):

    """
    __slots__ = (
        'position', 'color', 'scale', 'mass', 'radius',
        'constant_forces', 'momentary_forces', 'time_unused',
        'velocity', 'delta_velocity', 'register'
    )
    """
    register = []

    def __init__(self,  x=0, y=0, z=0, mass=1):
        self.position = V(x, y, z)
        self.color = V(1, 1, 0.6)
        self.scale = V()
        self.mass = float(mass)
        self.radius = 1

        # forces with constant "generator"
        self.constant_forces = []

        # there will be short-living forces
        self.momentary_forces = []

        # parameter necessary to mask poor precision of simulation
        self.time_unused = 0
        self.velocity = Vector3()
        self.delta_velocity = Vector3()
        self.register.append(self)

    def get_resultant_force(self):
        return reduce(Vector3.__add__, self.constant_forces + self.momentary_forces, V())

    def poke(self, force):
        self.momentary_forces.append(force)

    def push(self, force):
        self.constant_forces.append(force)

    def clear_momentary_forces(self):

        for force in self.momentary_forces:
            del force

        self.momentary_forces = []


class Box(Object):
    def __init__(self, x=0, y=0, z=0, mass=1, size=1, color=''):
        Object.__init__(self, x, y, z, mass)
        self.type = 'box'
        self.radius = size
        if color:
            self.color = color
        self.scale = V(size, size, size)


class Ball(Object):

    def __init__(self, x=0, y=0, z=0, mass=1, radius=1, color=''):
        Object.__init__(self, x, y, z, mass)
        self.type = 'ball'
        self.radius = radius
        if color:
            self.color = color
        self.scale = V(radius, radius, radius)


class WallBox:

    def __init__(self, size, mass_of_wall=1000, position=None, movable=True):

        if not position:
            position = V(0, 0, 0)

        Wall(x=position.x + size, mass=mass_of_wall, movable=movable)
        Wall(x=position.x - size, mass=mass_of_wall, movable=movable)
        Wall(y=position.y + size, mass=mass_of_wall, movable=movable)
        Wall(y=position.y - size, mass=mass_of_wall, movable=movable)
        Wall(z=position.z + size, mass=mass_of_wall, movable=movable)
        Wall(z=position.z - size, mass=mass_of_wall, movable=movable)


class Wall(Object):
    """Wall always is perpendicular to an axis."""

    # if not on the same side of wall
    def _collison_x(self, center, radius):
        return self.position.x > center.x - radius and self.position.x < center.x + radius

    def _collison_y(self, center, radius):
        return self.position.y > center.y - radius and self.position.y < center.y + radius

    def _collison_z(self, center, radius):
        return self.position.z > center.z - radius and self.position.z < center.z + radius

    def __init__(self,  x=None, y=None, z=None, mass=1000, movable=True):

        self.movable = movable

        if (x is None and y is None and z is None) or (x and y) or (x and z) or (y and z):
            raise Exception("Walls needs a single plane")

        if x is not None:
            self.collision_with_ball = self._collison_x
        else:
            x = 0

        if y is not None:
            self.collision_with_ball = self._collison_y
        else:
            y = 0

        if z is not None:
            self.collision_with_ball = self._collison_z
        else:
            z = 0

        Object.__init__(self, x, y, z, mass)
        self.type = 'wall'

