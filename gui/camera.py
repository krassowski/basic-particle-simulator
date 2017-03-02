from gi.repository import Gtk, Gio, Gdk
from internationalize import _
from OpenGL.GL import *
from OpenGL.GLU import *
from vector import *
import gtkgl
import random
import copy
import math


def sin(angle):
    return math.sin(math.radians(angle))


def cos(angle):
    return math.cos(math.radians(angle))


def atan2(x, y):
    return math.atan2(x, y) * 180.0 / math.pi


class Camera:

    output = None
    zoom = 50
    on = False

    near = 0.1
    far = 50
    is_on = False

    def __init__(self, data):

        self.pressed = False
        self.last_pos = [0, 0]

        self.eye = Vector3(z=1)
        self.look_at = Vector3()
        self.up = Vector3(y=1)
        self.angle = Vector3()
        self.position = Vector3()

        self.gl_wrapper = gtkgl.GtkGl()
        self.data = data

        if 'zoom' in self.data:
            self.zoom = self.data['zoom']

        self.reset()

        self.output = Gtk.DrawingArea()
        self.output.set_events(
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.SCROLL_MASK
            )
        self.output.connect('configure-event', self.on_configure_event)
        self.output.connect('draw', self.on_draw)
        self.output.connect('button-press-event', self.drag, True)
        self.output.connect('button-release-event', self.drag, False)
        self.output.connect('scroll-event', self.zoom_with_scroll)
        self.output.connect('motion-notify-event', self.drag)
        self.output.set_double_buffered(False)

        self.output.show()

    def drag(self, widget, event, start=None):
        if start is not None:
            self.pressed = start

        if self.pressed:
            scale = 0.01
            x_change = self.last_pos[0] - event.x
            y_change = self.last_pos[1] - event.y
            self.move(0, -x_change * self.zoom * scale)
            self.move(1, y_change * self.zoom * scale)

        self.last_pos = [event.x, event.y]

    def zoom_with_scroll(self, widget, event):
        self.zoom += event.delta_y
        self.refresh_wrapper()

    def reset(self):

        self.derotate()

        if 'up' in self.data:
            self.up = self.data['up']
        else:
            self.up = Vector3(y=1)

        self.refresh_wrapper()

    def refresh_wrapper(self):
        # affects only the 3d view
        if 'eye' in self.data:
            self.eye = self.data['eye'] * self.zoom

        if 'perspective' in self.data:
            self.gl_wrapper.perspective = self.data['perspective']

        # for non-3d view I pass a zoom parameter (it will by a factor in attributes of glOrtho call)
        self.gl_wrapper.zoom = self.zoom
        self.gl_wrapper.far = self.far * self.zoom
        self.gl_wrapper.near = self.near

    def set_zoom(self, zoom):
        self.zoom = zoom
        self.refresh_wrapper()

    def configure(self):

        self.on_configure_event(self.output)

    def on_configure(self):

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)

        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    def on_configure_event(self, widget, event=''):

        if self.is_on:

            self.gl_wrapper.configure(widget.get_window())
            self.on_configure()

    def adjust(self):

        gluLookAt(
            self.eye.x, self.eye.y, self.eye.z,
            self.look_at.x, self.look_at.y, self.look_at.z,
            self.up.x, self.up.y, self.up.z
        )

        glRotatef(self.angle.x, 0.05, 0.0, 0.0)
        glRotatef(self.angle.y, 0.0, 0.05, 0.0)
        glRotatef(self.angle.z, 0.0, 0.0, 0.05)

        glTranslatef(self.position.x, self.position.y, self.position.z)

    def get_right_vector(self):
        return self.rotate_vector(Vector3(1,0,0))

    def get_up_vector(self):
        return self.rotate_vector(self.up)

    def rotate_vector(self, vector):

        angle = - self.angle

        temp = Vector3()

        temp.x = vector.x
        temp.y = vector.y * cos(angle.x) - vector.z * sin(angle.x)
        temp.z = vector.y * sin(angle.x) + vector.z * cos(angle.x)

        vector = Vector3(temp.x, temp.y, temp.z)

        temp.x = vector.x * cos(angle.z) - vector.y * sin(angle.z)
        temp.y = vector.x * sin(angle.z) + vector.y * cos(angle.z)
        temp.z = vector.z

        vector = Vector3(temp.x, temp.y, temp.z)

        temp.x = vector.x * cos(angle.y) + vector.z * sin(angle.y)
        temp.y = vector.y
        temp.z =-vector.x * sin(angle.y) + vector.z * cos(angle.y)

        return temp

    def move(self, axis_id, direction):

        # it could be really optimized, but for readibility let it be as is:

        axis_maper = ('x', 'y', 'z')

        cam_mov = Vector3()
        setattr(cam_mov, axis_maper[axis_id], direction)

        self.position += self.get_right_vector() * cam_mov.x
        self.position += self.get_up_vector() * cam_mov.y
        # Not implemented yet and unnecessary
        # to calc this vector you need to get difference between eye and look_at
        # self.position += self.get_forward_vector() * cam_mov.z

    def rotate(self, axis_id, direction):

        axis_maper = ('x', 'y', 'z')

        new_angle = getattr(self.angle, axis_maper[axis_id]) + direction

        setattr(self.angle, axis_maper[axis_id], new_angle)

    def derotate(self, button=''):

        if 'angle' in self.data:
            self.angle = copy.deepcopy(self.data['angle'])
        else:
            self.angle = Vector3()

    def restart_position(self, button=''):

        self.position = Vector3()

    def on_draw(self, widget, context):

        if self.is_on:
            self.resize(widget)

            self.gl_wrapper.draw_start()
            self.adjust()
            self.rendering_function()
            self.gl_wrapper.draw_finish()
            self.output.queue_draw()

    def on(self):
        self.is_on = True

    def off(self):
        self.is_on = False

    def resize(self, container):

        width = container.get_allocated_width()
        height = container.get_allocated_height()

        # If camera is visible (there is a window for this camera)
        if self.output.get_window():
            self.gl_wrapper.resize(width, height, self.output.get_window())

    def rendering_function(self):
        pass
