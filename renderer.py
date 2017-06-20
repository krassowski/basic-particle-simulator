import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *
from vector import Vector3


class Color:

    def __init__(self, r, g, b, name=None):
        self.r = r
        self.g = g
        self.b = b
        self.name = name

color_map = {
    'red': (1, 0, 0),
    'green': (0, 1, 0),
    'blue': (0, 0, 1),
    'yellow': (1, 1, 0),
}

colors = {
    name: Color(r, g, b, name=name)
    for name, (r, g, b) in color_map.items()
}


class ObjectType:
    pass


class Ball(ObjectType):

    sphere_quality = 10

    @classmethod
    def draw(self):
        glutSolidSphere(1, self.sphere_quality, self.sphere_quality)


class AtomRepresentation:

    __slots__ = 'atom name color radius'.split(' ')

    default_color = Color(1, 0, 0)

    element_colors = {
        'H': colors['blue'], # TODO
        'Au': colors['yellow'],
    }

    def __init__(self, atom):
        self.atom = atom
        self.name = self.atom.name()
        self.color = self._determine_color()
        self.radius = self.atom.radius()

    type = Ball

    def _determine_color(self):
        return self.element_colors.get(self.name, self.default_color)

    @property
    def x(self):
        return self.atom.position[0]

    @property
    def y(self):
        return self.atom.position[1]

    @property
    def z(self):
        return self.atom.position[2]

    @property
    def scale(self):
        return Vector3(self.radius, self.radius, self.radius)


def perpendicular_vectors(v):
    if v.y:
        r = np.array([0.5, 0.0, 0.0])
    else:
        r = np.array([0.0, 0.5, 0.0])
    x = r
    k = np.array(v.to_list())
    x -= k * x.dot(k)
    x /= np.linalg.norm(x)
    y = np.cross(k, x)
    return Vector3.from_tuple(x), Vector3.from_tuple(y)


class Wall:
    def __init__(self, normal, distance, quality=10, size=None):
        self.lines = []
        if not size:
            size = abs(distance) * 2
        else:
            size = min(size, (abs(distance) * 2))

        quantity = quality
        if quantity % 2 == 1:
            quantity += 1
        spacing = size / quantity

        v = normal
        o1, o2 = perpendicular_vectors(v)
        o1 = o1
        o2 = o2
        d = distance
        v *= (-d)

        s = size / 2

        line_one = [v + o1 * s, v - o1 * s]
        line_two = [v + o2 * s, v - o2 * s]

        self.corners = [
            line_one[0] - o2 * s,
            line_one[0] - o2 * s,
            line_two[0] - o1 * s,
            line_two[0] + o1 * s,
        ]
        self.vertex = []
        for corner in self.corners:
            self.vertex.extend(corner.to_list())

        for i in range(-quantity // 2, quantity // 2 + 1):
            s = i * spacing

            s0 = line_one[0] + (o2 * s)
            e0 = line_one[1] + (o2 * s)
            self.lines.append((s0, e0))

            s1 = line_two[0] + (o1 * s)
            e1 = line_two[1] + (o1 * s)
            self.lines.append((s1, e1))


class Renderer:

    def __init__(self, manager):
        self.manager = manager
        self._fields = None
        self.walls = []
        glutInit()
        self.on_configure()
    
    @property
    def atoms(self):
        return self.manager.atoms

    def recompute_fields(self, fields):
        self._fields = fields
        self.walls = []
        for field in fields:
            if 'type' in field and field['type'] == 'wall':
                normal = Vector3(field['x'], field['y'], field['z'])
                wall = Wall(normal, field['distance'])
                self.walls.append(wall)

    def render(self):

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_LIGHTING)

        if self.manager.axis:
            self.draw_axis()

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

        if self.manager.grid:
            self.draw_grid()

        if self.manager.force_fields:
            if self.manager.force_fields != self._fields:
                self.recompute_fields(self.manager.force_fields)
            self.draw_fields()

        for atom in self.atoms:
            self.draw(atom)

    def draw_fields(self):
        for wall in self.walls:
            self.draw_wall(wall)

    def draw_wall(self, wall):
        glLineWidth(3)

        glColor3f(0.35, 0.85, 0.35)

        for start, end in wall.lines:
            glBegin(GL_LINES)

            glVertex3f(start.x, start.y, start.z)
            glVertex3f(end.x, end.y, end.z)

            glEnd()

    def draw_grid(self):

        #self.grid_id = glGenLists(1)

        #######
        #glNewList(self.grid_id, GL_COMPILE)

        glLineWidth(1)

        spacing = 5.0
        quantity = 26

        half_of_length = spacing * quantity // 2


        glColor3f(0.85, 0.85, 0.85)

        for i in range(-quantity // 2, quantity // 2 + 1):
            glBegin(GL_LINES)
            glVertex3f(-half_of_length, i * spacing, 0)
            glVertex3f(+half_of_length, i * spacing, 0)
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(0, i * spacing, -half_of_length)
            glVertex3f(0, i * spacing, +half_of_length)
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(i * spacing, -half_of_length, 0)
            glVertex3f(i * spacing, +half_of_length, 0)
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(i * spacing, 0, -half_of_length)
            glVertex3f(i * spacing, 0, +half_of_length)
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(-half_of_length, 0, i * spacing)
            glVertex3f(+half_of_length, 0, i * spacing)
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(0, -half_of_length, i * spacing)
            glVertex3f(0, +half_of_length, i * spacing)
            glEnd()


        #glEndList()
        #######

        #self.draw_grid = self.show_grid
        #self.draw_grid()

    def show_grid(self):
        glCallList(self.grid_id)

    def draw_axis(self):

        #self.axis_id = glGenLists(1)

        #######
        #glNewList(self.axis_id, GL_COMPILE)

        glLineWidth(2)

        axis_length = 20

        # x axis (red)
        glBegin(GL_LINES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(axis_length, 0, 0)
        glEnd()

        # y axis (green)
        glBegin(GL_LINES)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0, axis_length, 0)
        glEnd()

        # z axis (blue)
        glBegin(GL_LINES)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0, 0, axis_length)
        glEnd()

        #glEndList()
        #######

        #self.draw_axis = self.show_axis
        #self.draw_axis()

    def show_axis(self):
        glCallList(self.axis_id)

    def draw(self, obj):
        glPushMatrix()

        glColor3f(obj.color.r, obj.color.g, obj.color.b)

        glTranslatef(obj.x, obj.y, obj.z)
        # glRotatef(rotation.x, 0.1, 0.0, 0.0)
        # glRotatef(rotation.y, 0.0, 0.1, 0.0)
        # glRotatef(rotation.z, 0.0, 0.0, 0.1)
        glScalef(obj.scale.x, obj.scale.y, obj.scale.z)

        obj.type.draw()

        glPopMatrix()

    def on_configure(self):
        
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
        
        glEnable(GL_MULTISAMPLE)
        glutSetOption(GLUT_MULTISAMPLE, 16)
        #glHint(GL_MULTISAMPLE_FILTER_HINT_NV, GL_NICEST)
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        glEnable(GL_POINT_SMOOTH)
        #glHint(GL_POINT_SMOOTH_HINT, GL_LINEAR)

        glEnable(GL_LINE_SMOOTH)
        #glHint(GL_LINE_SMOOTH_HINT, GL_LINEAR)

        glEnable(GL_POLYGON_SMOOTH)
        #glHint(GL_POLYGON_SMOOTH_HINT, GL_LINEAR);

        light_ambient  = [0.0, 0.0, 0.0, 1.0]
        light_diffuse  = [1.0, 1.0, 1.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        light_position = [2.0, 5.0, 5.0, 0.0]

        mat_ambient    = [0.7, 0.7, 0.7, 1.0]
        mat_diffuse    = [0.8, 0.8, 0.8, 1.0]
        mat_specular   = [1.0, 1.0, 1.0, 1.0]
        high_shininess = [100.0]

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

        glLightfv(GL_LIGHT0, GL_AMBIENT,  light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glMaterialfv(GL_FRONT, GL_AMBIENT,   mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE,   mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR,  mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
