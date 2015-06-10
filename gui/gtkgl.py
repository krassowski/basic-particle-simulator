# [SNIPPET_AUTHOR: Oliver Marks ]
# [SNIPPET_LICENSE: GPL]


import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL import GLX
from OpenGL import GL
try:
	from OpenGL.GLX import struct__XDisplay
except:
	from OpenGL.raw._GLX import struct__XDisplay
from ctypes import *
from vector import *

import Xlib
from Xlib.display import Display
from gi.repository import Gtk, GdkX11, Gdk



class GtkGl():
	""" these method do not seem to exist in python x11 library lets exploit the c methods """
	xlib = cdll.LoadLibrary('libX11.so')
	xlib.XOpenDisplay.argtypes = [c_char_p]
	xlib.XOpenDisplay.restype = POINTER(struct__XDisplay)
	xdisplay = xlib.XOpenDisplay("")
	display = Xlib.display.Display()
	attrs = []

	xwindow_id = None
	width = height = 150
	perspective = True

	zoom = 1

	near = 0.1
	far = 100

	def __init__(self):
		""" lets setup are opengl settings and create the context for our window """
		self.add_attribute(GLX.GLX_RGBA, True)
		self.add_attribute(GLX.GLX_RED_SIZE, 1)
		self.add_attribute(GLX.GLX_GREEN_SIZE, 1)
		self.add_attribute(GLX.GLX_BLUE_SIZE, 1)
		self.add_attribute(GLX.GLX_ALPHA_SIZE, 1)
		self.add_attribute(GLX.GLX_DEPTH_SIZE, 1)
		self.add_attribute(GLX.GLX_DOUBLEBUFFER, 0)
		#self.add_attribute(GLX.GLX_SAMPLE_BUFFERS, 1)
		#self.add_attribute(GLX.GLX_SAMPLES, 4)


		xvinfo = GLX.glXChooseVisual(self.xdisplay, self.display.get_default_screen(), self.get_attributes())
		configs = GLX.glXChooseFBConfig(self.xdisplay, 0, None, byref(c_int()))
		self.context = GLX.glXCreateContext(self.xdisplay, xvinfo, None, True)

	def add_attribute(self, setting, value):
		"""just to nicely add opengl parameters"""
		self.attrs.append(setting)
		self.attrs.append(value)

	def get_attributes(self):
		""" return our parameters in the expected structure"""
		attrs = self.attrs + [0, 0]
		return (c_int * len(attrs))(*attrs)

	def additional_gl_configuration(self):
		pass

	def configure(self, wid=''):
		"""  """
		self.xwindow_id = GdkX11.X11Window.get_xid(wid)
		if not GLX.glXMakeCurrent(self.xdisplay, self.xwindow_id, self.context):
			print 'failed'
		glViewport(0, 0, self.width, self.height)

		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LESS)
		glClearDepth(1.0)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		ratio = float(self.width)/self.height

		if self.perspective:
			gluPerspective(45.0, ratio, self.near, self.far)
		else:
			glOrtho(-self.zoom * ratio, self.zoom * ratio, -self.zoom, self.zoom, self.near, self.far)

		glMatrixMode(GL_MODELVIEW)

		glLoadIdentity()


	def resize(self, width, height, window):
		self.width = width
		self.height = height
		self.configure(window)

	def draw_start(self):
		"""make cairo context current for drawing"""
		if not GLX.glXMakeCurrent(self.xdisplay, self.xwindow_id, self.context):
			print "failed"

	def draw_finish(self):
		"""swap buffer when we have finished drawing"""
		GLX.glXSwapBuffers(self.xdisplay, self.xwindow_id)
