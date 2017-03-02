from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Renderer:

    sphere_quality = 16

    def __init__(self, simulation):
        self.simulation = simulation
        glutInit()

    def render(self):

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.simulation.grid:
            self.draw_grid()

        if self.simulation.axis:
            self.draw_axis()

        for obj in self.simulation.objects:
            self.draw(obj)

    def draw_grid(self):

        #self.grid_id = glGenLists(1)

        #######
        #glNewList(self.grid_id, GL_COMPILE)

        glLineWidth(1)

        spacing = 5.0
        quantity = 26

        half_of_length = spacing * quantity / 2

        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_LIGHTING)

        glColor3f(0.85, 0.85, 0.85)

        for i in xrange(-quantity/2, quantity/2+1):
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

        glColor3f(obj.color.x, obj.color.y, obj.color.z)

        glTranslatef(obj.position.x, obj.position.y, obj.position.z)
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
