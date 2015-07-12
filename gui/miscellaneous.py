from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Pango
from internationalize import _
import os


def create_function_str(name, *args):
	new_func = name + "("
	for i, arg in enumerate(args):
		if i != 0:
			new_func += ", "
		new_func += repr(arg)
	new_func += ")"
	return new_func

def gtk_is_container(widget):
	try:
		widget.get_children()
		return True
	except:
		return False


def gtk_set_value(widget, value):
	if widget.get_name() == "GtkSwitch":
		widget.set_active( bool(value) )
	else:
		widget.set_value( value )


def gtk_set_value_by_name(name, value, root):
	widget = gtk_get_widget_by_name(name, root)
	gtk_set_value(widget, value)


def gtk_get_value(widget):
	if widget.get_name() == "GtkSwitch":
		return widget.get_active()
	else:
		return widget.get_value()


def gtk_get_value_by_name(name, value, root):
	widget = gtk_get_widget_by_name(name, root)
	return gtk_gset_value(widget, value)


def gtk_get_widget_name(widget):
	return Gtk.Buildable.get_name(widget)


def gtk_get_widget_by_name(name, root):

	if name == gtk_get_widget_name(root):
		return root

	if gtk_is_container(root):

		result = None
		for child in root.get_children():
			widget = gtk_get_widget_by_name(name, child)
			if widget:
				result = widget

		return result
	else:
		return None


def reparent(what, where):
	if what.get_parent():
		what.reparent(where)
	else:
		where.add(what)


def reparent_paned(what, where, func):
	if what.get_parent():
		what.reparent(where)
	else:
		func(what, 0, 0)

def get_gtk_version():
	return Gtk.get_major_version() + 0.01 * Gtk.get_minor_version()


def filicide(parent):
	for child in parent.get_children():
		parent.remove(child)


def gtk_get_builder_object(path, name, handlers=False):
	if os.path.isfile(path):
		builder = Gtk.Builder()
		builder.add_from_file(path)
		if handlers:
			builder.connect_signals(handlers)
		return builder.get_object(name)
	else:
		return False


def gtk_translate_widget(widget):

	widget_type = widget.get_name()

	if widget_type == "GtkButton":
		widget.set_label(_(widget.get_label()))
	elif widget_type == "GtkLabel":
		widget.set_label(_(widget.get_label()))
	elif gtk_is_container(widget):
		for child in widget.get_children():
			gtk_translate_widget(child)


def import_from_builder(destination, path, name, handlers=False):
	"""
	path - path to .glade file
	name - id of container from witch we will extract widgets
	"""
	temp_object = gtk_get_builder_object(path, name, handlers)
	if temp_object:
		for child in temp_object.get_children():
			gtk_translate_widget(child)
			reparent(child, destination)


def gtk_set_margin(self, all=False, top=False, bottom=False, right=False, left=False):

	if all:
		self.set_margin_left(all)
		self.set_margin_right(all)
		self.set_margin_top(all)
		self.set_margin_bottom(all)
	if top:
		self.set_margin_top(top)
	if bottom:
		self.set_margin_bottom(bottom)
	if right:
		self.set_margin_right(right)
	if left:
		self.set_margin_left(left)

def gtk_add_css_class(widget, class_name):
	widget.get_style_context().add_class(class_name)

def gtk_remove_css_class(widget, class_name):
	widget.get_style_context().remove_class(class_name)


def gtk_add_css(css):
	from gi.repository import Gdk
	style_provider = Gtk.CssProvider()

	style_provider.load_from_data(css)

	Gtk.StyleContext.add_provider_for_screen(
		Gdk.Screen.get_default(),
		style_provider,
		Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
	)

def get_folders(path, sort=False):
	folders = os.listdir(path)
	if sort:
		folders.sort()
  		if sort == "reversed":
			folders.reverse()
	return filter(lambda x: os.path.isdir(path + "/" + x), folders)

def get_files(path, ext_filter=None, sort=False):
	folders = os.listdir(path)
	if sort:
		folders.sort()
    	if sort == "reversed":
			folders.reverse()
	return filter(lambda x: not os.path.isdir(path + "/" + x) and (not ext_filter or x.endswith(ext_filter)), folders)


def get_icon_image(name):
	icon = Gio.ThemedIcon(name=name)
	return Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)

class ToggleBox(Gtk.Box):

	def __init__(self):
		Gtk.Box.__init__(self, spacing=0)
		self.get_style_context().add_class("inline-toolbar")

		self.handlers = []
		self.tbuttons = []
		self.count = 0
		self.user_callback = None


	def add_toggler(self, tbutton):

		if tbutton.get_name() != "GtkToggleButton":
			raise Exception("ToggleBox items have to be ToggleButtons")

		self.pack_start(tbutton, True, True, 0)
		self.tbuttons.append(tbutton)

		handler = tbutton.connect("toggled", self.do_callback, self.count)

		self.handlers.append(handler)
		self.count += 1

	def set_callback(self, callback):
		self.user_callback = callback

	def do_callback(self, button, new_id):

		for id, tbutton in enumerate(self.tbuttons):

			tbutton.handler_block(self.handlers[id])

			if id == new_id:
				tbutton.set_active(True)
				self._do_user_callback(id)
			else:
				tbutton.set_active(False)

			tbutton.handler_unblock(self.handlers[id])

	def set_active(self, new_active_id):
		if new_active_id < len(self.tbuttons):
			self.do_callback(None, new_active_id)
		else:
			raise KeyError("There is no ToggleButton with id: " + new_active_id + " in this ToggleBox")


	def _do_user_callback(self, id):
 		if self.user_callback:
			self.user_callback(id)

class IconicButton(Gtk.Button):

	def __init__(self, icon_name, tooltip=None):
		Gtk.Button.__init__(self)
		# or add?

		self.set_image(get_icon_image(icon_name))

		if tooltip:
			self.set_tooltip_text(tooltip)

def is_file(path, ext_filter=None):
	import os.path
	return os.path.isfile(path) and (not ext_filter or path.endswith(ext_filter))

def is_dir(path):
	import os.path
	return os.path.isdir(path)

def file_get_contents(path):
	import os.path
	if os.path.isfile(path):
		with open(path, "r") as f:
			return f.read()
	else:
		print "no file: ", path
		return ""


def file_put_contents(path, text=""):
	import os.path
	with open(path, "w") as f:
		f.write(text)

def help_me(wast=''):
	import webbrowser, internationalize
	path = "documentation/user_guide.html"
	lang = internationalize.CURRENT_LANG
	if is_dir("documentation/" + lang):
		path = "documentation/" + lang + "/user_guide.html"
	webbrowser.open('file://' + os.path.realpath(path), new=1, autoraise=True)

def set_tabs(text_view, font_description, number_of_spaces):

	layout = Pango.Layout(text_view.get_pango_context())
	layout.set_text(" "*number_of_spaces, number_of_spaces)
	layout.set_font_description(font_description)
	real_tab_width = layout.get_pixel_size()[0]
	del layout
	tabs = Pango.TabArray.new(1, True)
	tabs.set_tab(0, Pango.TabAlign.LEFT, real_tab_width)
	text_view.set_tabs(tabs)
