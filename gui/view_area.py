from gi.repository import Gtk, Gio, Gdk
from internationalize import _
import camera
from vector import *
import miscellaneous as misc
from event_handler import EventHandler

class ViewArea():

	allowed_modes = ["single", "vertical", "horizontal", "quad"]
	mode = None
	renderer = None

	def set_renderer(self, renderer):
		self.renderer = renderer
		for view in self.views:
			view.renderer = self.renderer
			view.connect_renderer()
		self.configure()

	# event_handler=EventHandler()
	def __init__(self, mode_on_start="single", event_handler=''):

		self.event_handler = event_handler

		# TODO: move it to file (json or repr)
		camera_data = [
			{
				"name": "3d view",
				"eye": Vector3(0, 0, 2),
				"perspective": True,
				"angle": Vector3(30, -45, 0)
			},
			{
				"name": "top projection",
				"eye": Vector3(0, 1, 0),
				"up": Vector3(0, 0, -1),
				"perspective": False
			},
			{
				"name": "bottom projection",
				"eye": Vector3(0, -1, 0),
				"up": Vector3(0, 0, 1),
				"perspective": False
			},
			{
				"name": "front projection",
				"eye": Vector3(0, 0, 1),
				"perspective": False
			},
			{
				"name": "back projection",
				"eye": Vector3(0, 0, -1),
				"perspective": False
			},
			{
				"name": "left projection",
				"eye": Vector3(-1, 0, 0),
				"perspective": False
			},
			{
				"name": "right projection",
				"eye": Vector3(1, 0, 0),
				"perspective": False
			}
		]

		self.cameras = {}

		for data in camera_data:
			camera_id = data["name"]
			# User is a view witch is connected to a camera
			self.cameras[camera_id] = {"camera": camera.Camera(data), "default_data": data}

		self.views = []

		self.views.append(self.View(self, "3d view"))
		self.views.append(self.View(self, "front projection"))
		self.views.append(self.View(self, "left projection"))
		self.views.append(self.View(self, "top projection"))

		self.gui = Gtk.Table()

		# Let's define .gui and .mode
		self.set_mode(mode_on_start)

	def set_mode(self, mode="single"):

		if mode not in self.allowed_modes:
			raise ValueError("The mode " + mode + "is not allowed")

		if self.mode:

			for widget in self.gui.get_children():
				widget.hide()

		for view in self.views:
			view.hide()

		if mode == "single":

			single = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
			single.show()

			misc.reparent_paned(self.views[0].gui, single, single.pack1)

			self.gui.add(single)
			self.views[0].show()

		elif mode == "vertical":

			paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
			paned.show()

			misc.reparent_paned(self.views[0].gui, paned, paned.pack1)
			misc.reparent_paned(self.views[1].gui, paned, paned.pack2)

			self.gui.add(paned)
			self.views[0].show()
			self.views[1].show()

			paned.show_all()

		elif mode == "horizontal":

			paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
			paned.show()

			misc.reparent_paned(self.views[0].gui, paned, paned.pack1)
			misc.reparent_paned(self.views[1].gui, paned, paned.pack2)

			self.gui.add(paned)
			self.views[0].show()
			self.views[1].show()

			paned.show_all()

		elif mode == "quad":

			paned1 = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
			paned1.show()

			misc.reparent_paned(self.views[0].gui, paned1, paned1.pack1)
			misc.reparent_paned(self.views[1].gui, paned1, paned1.pack2)

			paned2 = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
			paned2.show()

			misc.reparent_paned(self.views[2].gui, paned2, paned2.pack1)
			misc.reparent_paned(self.views[3].gui, paned2, paned2.pack2)

			quad = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
			quad.show()

			misc.reparent(paned1, quad)
			misc.reparent(paned2, quad)

			self.gui.add(quad)

			for view in self.views:
				view.show()

			quad.show_all()

		self.mode = mode

	def configure(self):

			for view in self.views:
				view.configure()

	class View():

		camera = None
		camera_id = None

		max_zoom = 500
		zoom_step = 20

		def show(self):
			self.gui.show()
			self.camera.on()

		def hide(self):
			self.gui.hide()
			self.camera.off()

		def adjust_camera(self, camera_id):

			data = self.cameras[camera_id]["default_data"]

			self.camera_id = camera_id
			self.camera.data = data
			self.camera.reset()

		def set_scale(self, button, value):

			if self.scale.get_value() != value:
				self.scale.set_value(value)

			self.camera.set_zoom(self.max_zoom - value)

		def choose_camera(self, combo):
			it = combo.get_active_iter()

			if it is None:
				raise Warning("it in choose_camera is None. It's probably some GTK+ error.")
			else:
				model = combo.get_model()
				camera_id = model[it][0]

				self.adjust_camera(camera_id)

		def configure(self):
			self.camera.configure()

		def connect_renderer(self):
			if self.renderer:
				self.camera.rendering_function = self.renderer.render
				if self.renderer.on_configure:
					self.camera.on_configure = self.renderer.on_configure

		def update_camera_chooser(self):
			self.camera_chooser.set_active_id(self.camera_id)

		def set_rotate_axis(self, new_axis_id):
			self.rotate_around = new_axis_id

		def rotate(self, button, direction):

			self.camera.rotate(self.rotate_around, direction)


		def move(self, button, axis_id, direction):

			self.camera.move(axis_id, direction)

		def __init__(self, parent, camera_id):

			self.camera_id = camera_id
			self.cameras = parent.cameras
			self.renderer = parent.renderer
			self.parent = parent

			self.gui = Gtk.Table()

			self.camera = self.cameras[camera_id]["camera"]
			self.connect_renderer()

			self.gui.attach(self.camera.output, 0, 1, 1, 2)

			self.stopgap = Gtk.Label()
			self.stopgap.set_alignment(0, 0.5)

			store = Gtk.ListStore(str, str)

			for camera_id, camera_data in self.cameras.items():
				store.append([camera_id, _(camera_id)])

			self.camera_chooser = Gtk.ComboBox.new_with_model(store)
			self.camera_chooser.connect("changed", self.choose_camera)
			renderer_text = Gtk.CellRendererText()
			self.camera_chooser.pack_start(renderer_text, True)
			self.camera_chooser.add_attribute(renderer_text, "text", 1)
			self.camera_chooser.set_id_column(0)


			self.update_camera_chooser()

			scale_adjustment = Gtk.Adjustment(value=self.max_zoom-self.camera.zoom, lower=0, upper=self.max_zoom - 1, step_incr=1, page_incr=5)

			self.scale = Gtk.ScaleButton()
			self.scale.set_adjustment(scale_adjustment)
			self.scale.set_icons(["edit-find-symbolic"])
			self.scale.connect("value-changed", self.set_scale)
			self.scale.set_tooltip_text(_("Adjust zoom of camera"))
			self.scale.get_plus_button().set_tooltip_text(_("zoom in"))
			self.scale.get_minus_button().set_tooltip_text(_("zoom out"))

			manipulating_toggler = Gtk.MenuButton()
			manipulating_toggler.set_relief(Gtk.ReliefStyle.NONE)
			manipulating_toggler.set_image(misc.get_icon_image("view-more-symbolic"))
			manipulating_toggler.set_tooltip_text(_("Show manipulating options"))
			manipulating_toggler.set_halign(Gtk.Align.CENTER)

			try:
				manipulators = Gtk.PopoverMenu()
			except:
				manipulators = Gtk.Popover()

			manipulators_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

			manipulators_box.set_border_width(9)

			move_text = Gtk.Label()
			move_text.set_markup('<span foreground="gray">' + _("Move precisely") + '</span>')
			move_text.set_alignment(0, 0.5)
			manipulators_box.add(move_text)

			move_table = Gtk.Table()

			b = misc.IconicButton("go-up-symbolic")
			self.parent.event_handler.connect_with_press_up(b, self.move, 1, -1)
			move_table.attach(b, 1, 2, 0, 1)

			b = misc.IconicButton("go-previous-symbolic")
			self.parent.event_handler.connect_with_press_up(b, self.move, 0, -1)
			move_table.attach(b, 0, 1, 1, 2)

			b = misc.IconicButton("window-close-symbolic", _("Restart position"))
			b.connect("clicked", self.camera.restart_position)
			move_table.attach(b, 1, 2, 1, 2)

			b = misc.IconicButton("go-next-symbolic")
			self.parent.event_handler.connect_with_press_up(b, self.move, 0, 1)
			move_table.attach(b, 2, 3, 1, 2)

			b = misc.IconicButton("go-down-symbolic")
			self.parent.event_handler.connect_with_press_up(b, self.move, 1, 1)
			move_table.attach(b, 1, 2, 2, 3)

			manipulators_box.add(move_table)

			manipulators_box.add(Gtk.Separator())

			axis_text = Gtk.Label()
			axis_text.set_markup('<span foreground="gray">' + _("Rotate around axis") + '</span>')
			axis_text.set_alignment(0, 0.5)
			manipulators_box.add(axis_text)

			axis_toggle_box = misc.ToggleBox()
			axis_toggle_box.add_toggler( Gtk.ToggleButton("x") )
			axis_toggle_box.add_toggler( Gtk.ToggleButton("y") )
			axis_toggle_box.add_toggler( Gtk.ToggleButton("z") )

			axis_toggle_box.set_callback(self.set_rotate_axis)
			axis_toggle_box.set_active(0)

			manipulators_box.add(axis_toggle_box)

			rotator_box = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
			rotator_box.set_layout(Gtk.ButtonBoxStyle.START)
			rotator_box.set_halign(Gtk.Align.START)
			rotator_box.set_valign(Gtk.Align.START)

			rotator_box.get_style_context().add_class("inline-toolbar")
			rotator_left = misc.IconicButton("edit-undo-symbolic", _("Rotate left"))
			rotator_right = misc.IconicButton("edit-redo-symbolic", _("Rotate right"))
			self.parent.event_handler.connect_with_press_up(rotator_left, self.rotate, -1)
			self.parent.event_handler.connect_with_press_up(rotator_right, self.rotate, +1)
			rotator_box.add(rotator_left)
			rotator_box.add(rotator_right)
			manipulators_box.add(rotator_box)

			try:
				rotator_restart = Gtk.ModelButton("")
			except:
				rotator_restart = Gtk.Button("")
			rotator_restart.set_label(_("Restart rotation"))
			rotator_restart.connect("clicked", self.camera.derotate)

			manipulators_box.add(rotator_restart)


			manipulating_toggler.set_popover(manipulators)

			manipulators.add(manipulators_box)
			manipulators.show_all()
			manipulators.hide()


			top = Gtk.Box()
			top.pack_start(self.camera_chooser, False, False, 0)
			top.pack_start(self.stopgap, True, True, 0)
			top.pack_start(self.scale, False, False, 0)
			top.pack_start(manipulating_toggler, False, False, 0)
			misc.gtk_set_margin(top, bottom=2)

			self.gui.attach(top, 0, 1, 0, 1, yoptions=Gtk.AttachOptions.SHRINK)
			self.gui.set_size_request(300, 200)

			misc.gtk_set_margin(self.gui, 10)
