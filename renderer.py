from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.freeglut import *


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

from vector import Vector3

class AtomRepresentation:

    __slots__ = 'atom name color radius'.split(' ')

    default_color = Color(1, 0, 0)

    element_colors = {
        'H': colors['red'], # TODO
        'Au': colors['yellow'],
    }

    def __init__(self, atom):
        self.atom = atom
        self.name = self.atom.name()
        self.color = self._determine_color()
        self.radius = self.atom.radius()

    @property
    def type(self):
        return 'ball'

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


class Renderer:

    sphere_quality = 16

    def __init__(self, manager):
        self.manager = manager
        glutInit()
        self.on_configure()
    
    @property
    def atoms(self):
        return self.manager.atoms

    def render(self):

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.manager.grid:
            self.draw_grid()

        if self.manager.axis:
            self.draw_axis()

        for atom in self.atoms:
            self.draw(atom)

    def draw_grid(self):

        #self.grid_id = glGenLists(1)

        #######
        #glNewList(self.grid_id, GL_COMPILE)

        glLineWidth(1)

        spacing = 5.0
        quantity = 26

        half_of_length = spacing * quantity // 2

        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_LIGHTING)

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

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

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

        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_LIGHTING)

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

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

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

        #obj.shape.draw()

        if obj.type == "ball":
            self.draw_sphere()

        elif obj.type == "box":
            self.draw_box()

        glPopMatrix()

    def on_configure(self):
        
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
        
        glEnable(GL_MULTISAMPLE)
        glutSetOption(GLUT_MULTISAMPLE, 8)
        #glHint(GL_MULTISAMPLE_FILTER_HINT_NV, GL_NICEST)
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glEnable(GL_BLEND);

        glEnable(GL_POINT_SMOOTH);
        #glHint(GL_POINT_SMOOTH_HINT, GL_LINEAR);

        glEnable(GL_LINE_SMOOTH);
        #glHint(GL_LINE_SMOOTH_HINT, GL_LINEAR);

        glEnable(GL_POLYGON_SMOOTH);
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
        


    def draw_sphere(self):
        #glutWireSphere(1, 16, 16)
        #print(self.sphere_quality, self.sphere_quality)
        #self.draw_box()
        #glutSolidSphere(1, self.sphere_quality, self.sphere_quality)
        glutWireSphere(1, self.sphere_quality, self.sphere_quality)
        #glutSolidCylinder(1, 1, 4, 4)
        #
        
  
        """
        #define X .525731112119133606 
        #define Z .850650808352039932

        static GLfloat vdata[12][3] = {    
        {-X, 0.0, Z}, {X, 0.0, Z}, {-X, 0.0, -Z}, {X, 0.0, -Z},    
        {0.0, Z, X}, {0.0, Z, -X}, {0.0, -Z, X}, {0.0, -Z, -X},    
        {Z, X, 0.0}, {-Z, X, 0.0}, {Z, -X, 0.0}, {-Z, -X, 0.0} 
        };
        
        tindices[20][3] = { 
            {0,4,1}, {0,9,4}, {9,5,4}, {4,5,8}, {4,8,1},    
            {8,10,1}, {8,3,10}, {5,3,8}, {5,2,3}, {2,7,3},    
            {7,10,3}, {7,6,10}, {7,11,6}, {11,0,6}, {0,1,6}, 
            {6,1,10}, {9,0,11}, {9,11,2}, {9,2,5}, {7,2,11}
            }


        for i in range(20):
            subdivide(
                &vdata[tindices[i][0]][0],       
                &vdata[tindices[i][1]][0],       
                &vdata[tindices[i][2]][0]
            )
        """
        
    def drawtriangle(v1, v2, v3):
        glBegin(GL_TRIANGLES)
        glNormal3fv(v1)
        vlVertex3fv(v1)
        
        glNormal3fv(v2)
        vlVertex3fv(v2)    
        
        glNormal3fv(v3)
        vlVertex3fv(v3)    
        glEnd()

    def subdivide(v1, v2, v3):
        v12 = []
        v23 = []
        v31 = []

        for i in range(3):
            v12.append(v1[i] + v2[i]) 
            v23.append(v2[i] + v3[i])
            v31.append(v3[i] + v1[i])  
            
        normalize(v12)
        normalize(v23) 
        normalize(v31) 
        drawtriangle(v1, v12, v31)
        drawtriangle(v2, v23, v12)    
        drawtriangle(v3, v31, v23)    
        drawtriangle(v12, v23, v31) 

   
    @staticmethod
    def draw_box():
        glBegin(GL_QUADS)            # Start Drawing The Cube

        glColor3f(0.0,1.0,0.0)            # Set The Color To Blue
        glVertex3f( 1.0, 1.0,-1.0)        # Top Right Of The Quad (Top)
        glVertex3f(-1.0, 1.0,-1.0)        # Top Left Of The Quad (Top)
        glVertex3f(-1.0, 1.0, 1.0)        # Bottom Left Of The Quad (Top)
        glVertex3f( 1.0, 1.0, 1.0)        # Bottom Right Of The Quad (Top)

        glColor3f(1.0,0.5,0.0)            # Set The Color To Orange
        glVertex3f( 1.0,-1.0, 1.0)        # Top Right Of The Quad (Bottom)
        glVertex3f(-1.0,-1.0, 1.0)        # Top Left Of The Quad (Bottom)
        glVertex3f(-1.0,-1.0,-1.0)        # Bottom Left Of The Quad (Bottom)
        glVertex3f( 1.0,-1.0,-1.0)        # Bottom Right Of The Quad (Bottom)

        glColor3f(1.0,0.0,0.0)            # Set The Color To Red
        glVertex3f( 1.0, 1.0, 1.0)        # Top Right Of The Quad (Front)
        glVertex3f(-1.0, 1.0, 1.0)        # Top Left Of The Quad (Front)
        glVertex3f(-1.0,-1.0, 1.0)        # Bottom Left Of The Quad (Front)
        glVertex3f( 1.0,-1.0, 1.0)        # Bottom Right Of The Quad (Front)

        glColor3f(1.0,1.0,0.0)            # Set The Color To Yellow
        glVertex3f( 1.0,-1.0,-1.0)        # Bottom Left Of The Quad (Back)
        glVertex3f(-1.0,-1.0,-1.0)        # Bottom Right Of The Quad (Back)
        glVertex3f(-1.0, 1.0,-1.0)        # Top Right Of The Quad (Back)
        glVertex3f( 1.0, 1.0,-1.0)        # Top Left Of The Quad (Back)

        glColor3f(0.0,0.0,1.0)            # Set The Color To Blue
        glVertex3f(-1.0, 1.0, 1.0)        # Top Right Of The Quad (Left)
        glVertex3f(-1.0, 1.0,-1.0)        # Top Left Of The Quad (Left)
        glVertex3f(-1.0,-1.0,-1.0)        # Bottom Left Of The Quad (Left)
        glVertex3f(-1.0,-1.0, 1.0)        # Bottom Right Of The Quad (Left)

        glColor3f(1.0,0.0,1.0)            # Set The Color To Violet
        glVertex3f( 1.0, 1.0,-1.0)        # Top Right Of The Quad (Right)
        glVertex3f( 1.0, 1.0, 1.0)        # Top Left Of The Quad (Right)
        glVertex3f( 1.0,-1.0, 1.0)        # Bottom Left Of The Quad (Right)
        glVertex3f( 1.0,-1.0,-1.0)        # Bottom Right Of The Quad (Right)
        glEnd()                # Done Drawing The Quad
