from gi.repository import Gtk
from gi.repository import Gdk
from internationalize import _
from option_browser import OptionBrowser
from view_area import ViewArea
from console import Console
from event_handler import EventHandler
import miscellaneous as misc

class MainWindow(Gtk.Window):

	full_screen = False
	show_more_buttons = True
	show_option_browser = True
	default_view = "single"
	first_full_screen = True
	first_toggle_option_browser = True

	def on_key_press(self, win, event):
		key_sensitive = Gdk.keyval_name(event.keyval)
		key = key_sensitive.lower()
		mask = event.state & Gtk.accelerator_get_default_mod_mask()
		ctrl_key = (mask == Gdk.ModifierType.CONTROL_MASK)
		shift_key = (mask == Gdk.ModifierType.SHIFT_MASK)

		if mask == Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK:
			ctrl_key = True
			shift_key = True

		if key == 'f11':
			self.toggle_full_screen()
		elif key == 'f9':
			self.toggle_option_browser()
		elif ctrl_key and shift_key and key == "z":
			self.console.script.redo()
		elif ctrl_key and key == "z":
			self.console.script.undo()
		elif ctrl_key and key == "y":
			self.console.script.redo()
		return False

	def show_tip(self, text, force=False):
		if self.config.show_tips or force:
			self.infobar.show()
			self.infobar_label.set_text(text)

	def toggle_tips(self, switch='', gparam=''):
		old = self.config.show_tips
	 	self.config.set("show_tips", switch.get_active())
		if old != self.config.show_tips:
			self.config.save_to_file()

	def toggle_header_bar(self, switch='', gparam=''):
		old = self.config.do_not_use_header_bar
	 	self.config.set("do_not_use_header_bar", switch.get_active())
		if old != self.config.do_not_use_header_bar:
			show_info = True
			try:
				is_header_bar = (self.top_bar.get_name() == "GtkHeaderBar")
				show_info = (is_header_bar == self.config.do_not_use_header_bar)
			except:
				pass
			if show_info:
				self.show_tip(_("The changes will be applied the next time the application restarts"))
			self.config.save_to_file()

	def toggle_prompt(self, switch='', gparam=''):
		old = self.config.prompt_on_exit
	 	self.config.set("prompt_on_exit", switch.get_active())
		if old != self.config.prompt_on_exit:
			self.config.save_to_file()

	def toggle_option_browser(self, switch='', gparam=''):

		if switch:
			if switch.get_active():
				self.revealer.set_reveal_child(True)
				self.show_option_browser = True
				self.infobar.hide()
			else:
				self.revealer.set_reveal_child(False)
				self.show_option_browser = False
				if self.first_toggle_option_browser:
					self.show_tip(_("To restore option browser use a switcher on a top bar"))
					self.first_toggle_option_browser = False

		else:
			if self.show_option_browser:
				self.switch.set_active(False)
			else:
				self.switch.set_active(True)

	def toggle_full_screen(self, x='None'):

		if self.full_screen:
			self.full_screen_button.set_image(misc.get_icon_image("view-fullscreen-symbolic"))
			self.option_browser.gui.show()
			self.console.gui.show()
			self.unfullscreen()
			self.infobar.hide()
		else:
			self.full_screen_button.set_image(misc.get_icon_image("view-restore-symbolic"))
			self.option_browser.gui.hide()
			self.console.gui.hide()
			self.fullscreen()
			if self.first_full_screen:
				self.show_tip(_("Press F11 to exit full screen mode."))
				self.first_full_screen = False


		self.full_screen = not self.full_screen

	def reveal_more_buttons(self, button):
		if self.revealer_more_buttons.get_reveal_child():
			self.revealer_more_buttons.set_reveal_child(False)
			self.more_buttons.set_image(misc.get_icon_image("go-previous-symbolic"))
		else:
			self.revealer_more_buttons.set_reveal_child(True)
			self.more_buttons.set_image(misc.get_icon_image("go-next-symbolic"))

	def add_top_bar_items(self, container, modes):

		is_header_bar = (container.get_name() == "GtkHeaderBar")

		def pack_start(what):
			if is_header_bar:
				container.pack_start(what)
			else:
				container.pack_start(what, 0, 0, 0)


		def pack_end(what):
			if is_header_bar:
				container.pack_end(what)
			else:
				container.pack_end(what, 0, 0, 0)


		view_text = Gtk.Label(_("view:"))
		misc.gtk_set_margin(view_text, left=5)

		pack_start(view_text)

		store = Gtk.ListStore(str, str)

		for mode in modes:
			store.append([mode, _(mode)])

		view_chooser = Gtk.ComboBox.new_with_model(store)
		view_chooser.connect("changed", self.on_set_view_layout)

		renderer_text = Gtk.CellRendererText()
		view_chooser.pack_start(renderer_text, True)
		view_chooser.add_attribute(renderer_text, "text", 1)
		view_chooser.set_id_column(0)

		view_chooser.set_active_id(self.default_view)

		self.revealer_more_buttons = Gtk.Revealer()
		self.revealer_more_buttons.set_transition_duration(500)
		self.revealer_more_buttons.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)

		self.more_buttons = misc.IconicButton("go-previous-symbolic", _("show more buttons"))
		self.more_buttons.set_relief(Gtk.ReliefStyle.NONE)
		self.more_buttons.connect("clicked", self.reveal_more_buttons)

		self.full_screen_button = misc.IconicButton("view-fullscreen-symbolic", _("toggle fullscreen"))
		self.full_screen_button.set_relief(Gtk.ReliefStyle.NONE)
		self.full_screen_button.connect("clicked", self.toggle_full_screen)
		misc.gtk_set_margin(self.full_screen_button, left=8, right=3)

		self.switch_label = Gtk.Label(_("option browser:"))
		self.switch = Gtk.Switch()
		self.switch.connect("notify::active", self.toggle_option_browser)
		self.switch.set_active(True)

		box = Gtk.Box()

		box.add(self.switch_label)
		box.add(self.switch)
		box.add(self.full_screen_button)

		self.revealer_more_buttons.add(box)

		pack_end(self.revealer_more_buttons)
		pack_end(self.more_buttons)

		pack_start(view_chooser)

	def delete_event(self, widget, event, data=None):
		question = _("Unsaved changes will be lost.\nPress enter to discard changes and quit immediately.")
		title = _("Are you sure you want to quit?")
		if not self.config.prompt_on_exit or ask(question, title, self):
			# GTK will emit the "destroy" signal
			return False
		else:
			# The main window will not be destroyed
			return True

	def destroy(self, widget, data=None):
		self.is_open = False
		#Gtk.main_quit()

	def create_main_area(self, option_browser, view_area):
		main_area = Gtk.Box(Gtk.Orientation.HORIZONTAL)
		main_area.show()
		main_area.pack_start(option_browser, 0, 0, 0)
		main_area.pack_start(view_area, 1, 1, 0)

		return main_area

	def on_set_view_layout(self, combo):

		if not self.view_area:
			raise RuntimeWarning("on_set_view_layout was called but self.view_area wasn't initialized yet")

		it = combo.get_active_iter()

		if it is None:
			raise Warning("it in on_set_view_layout is None. It's probably some GTK+ error.")
		else:
			model = combo.get_model()
			mode = model[it][0]
			#print("Switching to mode %s" % mode)

			self.view_area.set_mode(mode)

	def infobar_response(self, infobar, respose_id):
		infobar.hide()

	def main_iteration(self):
		main_iteration()
		self.event_handler.tick()

	def __init__(self, simulation, config):

		self.config = config

		Gtk.Window.__init__(self)

		self.event_handler = EventHandler()

		self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.simulation = simulation

		self.set_resizable(True)

		self.set_reallocate_redraws(True)

		self.connect('delete_event', self.delete_event)
		self.connect('destroy', self.destroy)
		self.connect('key-press-event', self.on_key_press)

		# Elements of main area
		self.option_browser = OptionBrowser(self)

		self.revealer = Gtk.Revealer()
		self.revealer.set_transition_duration(500)
		self.revealer.set_transition_type(Gtk.RevealerTransitionType.SLIDE_RIGHT)
		self.revealer.add(self.option_browser.gui)

		self.view_area = ViewArea(self.default_view, self.event_handler)

		# Title and header bar
		title = _("Physics simulator")
		self.set_title(title)
		self.set_wmclass(title, title)

		self.top_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)

		self.infobar = Gtk.InfoBar()
		self.infobar_label = Gtk.Label()
		self.infobar.get_content_area().add(self.infobar_label)
		self.infobar_label.show()
		self.infobar.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
		self.infobar.set_default_response(Gtk.ResponseType.CLOSE)
		self.infobar.connect("response", self.infobar_response)

		self.top_layout.add(self.infobar)

		if self.config.do_not_use_header_bar:

			self.top_bar = Gtk.Box()
			#self.toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
			#self.toolbar.get_style_context().add_class("inline-toolbar")
			self.top_bar.get_style_context().add_class("primary-toolbar")
			self.top_layout.add(self.top_bar)

		else:

			self.top_bar = Gtk.HeaderBar()
			self.top_bar.set_show_close_button(True)
			self.top_bar.props.title = title
			self.set_titlebar(self.top_bar)


		self.add_top_bar_items(self.top_bar, self.view_area.allowed_modes)

		# Main panels
		self.main_panels = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
		self.main_panels.show()

		self.main_area = self.create_main_area(self.revealer, self.view_area.gui)
		self.main_panels.pack1(self.main_area, 0, 0)

		self.console = Console(self.option_browser, self.simulation)
		self.main_panels.pack2(self.console.gui, 0, 0)



		self.overlay = Gtk.Overlay()
		self.overlay.add(self.main_panels)
		self.overlay.add_overlay(self.console.controls.gui)

		self.main_panels.set_border_width(8)

		self.top_layout.pack_end(self.overlay, 1,1,1)

		self.add(self.top_layout)

		self.set_icon_from_file('gui/icon.svg')

		self.realize()

		self.infobar.set_no_show_all(True)
		self.show_all()

		self.option_browser.breadcrumb.update()

		self.is_open = True


def main_iteration():
	Gtk.main_iteration()


def message_box(text, title, window=None):

	if window:
		temp_window = window
	else:
		temp_window = Gtk.Window()
	dialog = Gtk.MessageDialog(temp_window, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, title)
	dialog.format_secondary_text(text)
	dialog.run()
	dialog.destroy()
	if not window:
		temp_window.destroy()


def ask(question, title, window=None, default_yes=True):

	if window:
		temp_window = window
	else:
		temp_window = Gtk.Window()

	dialog = Gtk.MessageDialog(temp_window, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, title)

	default_response = Gtk.ResponseType.NO

	if default_yes:
		default_response = Gtk.ResponseType.YES

	dialog.set_default_response(default_response)

	dialog.format_secondary_text(question)

	response = dialog.run()
	result = False

	if response == Gtk.ResponseType.YES:
		result = True

	dialog.destroy()

	if not window:
		temp_window.destroy()

	return result


def file_chooser(action="open", window=None, current_folder=None):
	if window:
		temp_window = window
	else:
		temp_window = Gtk.Window()

	if action == "open":
		gtk_action = Gtk.FileChooserAction.OPEN
	elif action == "save":
		gtk_action = Gtk.FileChooserAction.SAVE
	else:
		gtk_action = Gtk.FileChooserAction.OPEN

	dialog = Gtk.FileChooserDialog(_("Please choose a file"), temp_window, gtk_action, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

	if current_folder:
		dialog.set_current_folder(current_folder)

	response = dialog.run()
	result = False

	if response == Gtk.ResponseType.OK:
		result = dialog.get_filename()

	dialog.destroy()
	if not window:
		temp_window.destroy()
	return result
