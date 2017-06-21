from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from internationalize import _, is_english_off
import gui.miscellaneous as misc


class OptionBrowser:

    _path = ["options"]

    def __init__(self, window):

        self.window = window

        # widget id -> handler
        self.actions = {
            "fullscreen": window.toggle_full_screen,
            "hide_options": window.toggle_option_browser,
            "load_from_file": self.load_from_file,
            "save_as": self.save_as,
            "save": self.save,
            "show_tips": window.toggle_tips,
            "prompt_on_exit": window.toggle_prompt,
            "do_not_use_header_bar": window.toggle_header_bar,
            "polish_version": window.toggle_polish_version,
            "plot_energies": window.simulation.plot_energies
        }

        self.let_actions = [
                "step_size", "speed", "grid", "axis",
                "direction", "gravity", "earth_gravity",
                "fog"
            ]

        self.masks = {
                "direction": {False: "forward", True: "backward"}
            }

        self.option_reference = [
                ("show_tips", "self.window.config.show_tips"),
                ("prompt_on_exit", "self.window.config.prompt_on_exit"),
                ("do_not_use_header_bar", "self.window.config.do_not_use_header_bar"),
                ("polish_version", "is_english_off()"),
            ]

        for option_name in self.let_actions:
            self.actions[option_name] = self.let_from_switch

        self.breadcrumb = self.Breadcrumb(self)
        self.browser = self.Browser(self)

        self.gui = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.gui.show()
        self.gui.add(self.breadcrumb.gui)
        self.gui.add(self.browser.gui)

        self.gui.set_size_request(200, 400)

    def back(self, to_where):
        self._path = self._path[:self._path.index(to_where) + 1]
        self.browser.update()

    def go(self, where):
        self._path.append(where)

    def get_path_string(self):
        return "gui/" + "/".join(self._path)

    def get_path(self):
        return self._path

    def load_from_file(self):
        import gui.windows as windows
        path = windows.file_chooser("open", self.window, "simulations")
        if path:
            self.window.console.controls.end()
            self.window.console.script.load_simulation(path)

    def save_as(self):
        import gui.windows as windows
        path = windows.file_chooser("save", self.window, "simulations")
        if path:
            self.window.console.script.save_simulation(path)
            self.browser.update()

    def save(self):
        import gui.windows as windows
        question = _("Do you really want to overwrite existing file?")
        title = _("Overwrite existing file?")
        overwrite = windows.ask(question, title, self.window)
        if overwrite:
            path = self.window.console.script.path
            self.window.console.script.save_simulation(path)
            self.browser.update()

    def let_from_switch(self, widget):
        option_name = misc.gtk_get_widget_name(widget)
        if self.prevent_button_action:
            self.prevent_button_action = False
            return True

        active = misc.gtk_get_value(widget)

        mask = self.get_mask(option_name)
        if mask:
            active = mask[active]

        self.window.console.script.modify('function', 'let', option_name, active, where="after_comments")

    def get_mask(self, name):
        """
        Maski sluza przkladaniu wartosci zwracanych przez switch na wartosci typu
            False: "forward", True: "backward"
        """
        if name in self.masks:
            return self.masks[name]
        else:
            return None

    def get_inverse_mask(self, name):
        mask = self.get_mask(name)
        if mask:
            return {value: key for key, value in mask.items()}
        else:
            return None

    def update_button_states(self):

        if hasattr(self.window, "console"):
            self.window.console.script.try_update_button_states()

        register = []

        for option_name, reference in self.option_reference:
            register.append( (option_name, eval(reference)) )

        self.update_button_states_from_register(register)

    def update_button_states_from_register(self, register):
        if not hasattr(self, "browser"):
            return
        for option_name, value in register:
            widget = misc.gtk_get_widget_by_name(option_name, self.browser.gui)
            if widget:
                mask = self.get_inverse_mask(option_name)
                if mask and value:
                    value = mask[value]
                self.prevent_button_action = True
                misc.gtk_set_value(widget, value)
            self.prevent_button_action = False

    def get_let_actions_list(self):
        return self.let_actions


    class Breadcrumb():

        collapsed = False
        last_visible = None
        path = None

        def __init__(self, option_browser):
            self.option_browser = option_browser

            self.bread_buttons = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
            self.bread_buttons.set_layout(Gtk.ButtonBoxStyle.START)
            self.bread_buttons.set_halign(Gtk.Align.START)
            self.bread_buttons.set_valign(Gtk.Align.START)
            self.bread_buttons.get_style_context().add_class("inline-toolbar")

            self.gui = Gtk.Box()

            self.button_prev = self.collapse_button("previous", self.move_collapsed_prev)
            self.button_next = self.collapse_button("next", self.move_collapsed_next)

            self.revealer_buttons = Gtk.Revealer()
            self.revealer_buttons.set_transition_duration(500)
            self.revealer_buttons.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)

            self.revealer_buttons.add(self.bread_buttons)

            self.gui.add(self.button_prev)
            self.gui.add(self.revealer_buttons)
            self.gui.add(self.button_next)

            self.update()

        def collapse_button(self, direction, callback):

            button = misc.IconicButton("go-" + direction + "-symbolic")
            button.connect("clicked", callback)
            return button

        def move_collapsed_next(self, widget=''):
            self.last_visible += 1
            self.redraw()

        def move_collapsed_prev(self, widget=''):
            self.last_visible -= 1
            self.redraw()

        def redraw(self):

            # Let's clear a little bit
            misc.filicide(self.bread_buttons)

            path = self.path

            if self.collapsed:

                self.button_prev.set_sensitive(self.last_visible != 1)
                self.button_next.set_sensitive(self.last_visible != len(self.path) - 1)

                path = self.path[self.last_visible - 1:self.last_visible+1]

                self.button_next.show()
                self.button_prev.show()
            else:
                self.button_next.hide()
                self.button_prev.hide()

            for crumb in path:
                button = Gtk.Button(_(crumb))
                button.connect("clicked", self.go_higher, crumb)
                self.bread_buttons.add(button)

            self.bread_buttons.show_all()

            if len(path) > 1:
                self.revealer_buttons.set_reveal_child(True)
            else:
                self.revealer_buttons.set_reveal_child(False)

            self.option_browser.update_button_states()

        def update(self):

            self.path = self.option_browser.get_path()

            # determine whether the number of elements is so high, that we will collapse it
            self.collapsed = len(self.path) > 2

            if self.collapsed:
                self.last_visible = len(self.path) - 1

            self.redraw()

        # Oh, we need some high
        def go_higher(self, x, action):
            self.option_browser.back(action)

    class Browser():

        def __init__(self, option_browser):

            self.option_browser = option_browser
            self.gui = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            self.load_options()

        # We need to go deeper...
        def go_deeper(self, level):
            self.option_browser.go(level)
            misc.filicide(self.gui)
            self.load_options()
            self.gui.show_all()
            self.option_browser.breadcrumb.update()

        def update(self):
            misc.filicide(self.gui)
            self.load_options()
            self.gui.show_all()
            self.option_browser.breadcrumb.update()

        def load_options(self):

            path = self.option_browser.get_path_string()

            # Load hierarchy
            folders = misc.get_folders(path, sort="reversed")

            for folder in folders:
                #image = misc.get_icon_image("go-next-symbolic")
                #button = Gtk.Button(label=_(folder), image=image)
                button = Gtk.Button(label=_(folder))
                button.connect("clicked", self.action, folder)
                button.set_alignment(0, 0.5)
                self.gui.add(button)

            # Load buttons from current level
            handlers = {"action": self.action}
            gui_glade_src = path + "/ui.glade"
            gui_script_src = path + "/ui.py"

            from imp import load_source

            if misc.is_file(gui_script_src, ".py"):
                options_script = load_source('', gui_script_src)
                if hasattr(options_script, 'load_gui'):
                    options_script.load_gui(self.gui, misc, self.action)

            misc.import_from_builder(self.gui, gui_glade_src, "option_box", handlers)

            for child in self.gui.get_children():
                child.set_margin_right(10)

        def action(self, widget, _action=False):
            if type(_action) is str:
                path = self.option_browser.get_path_string()
                if misc.is_dir(path + "/" + _action):
                    self.go_deeper(_action)
                elif misc.is_file("simulations/" + _action, ".py"):
                    self.option_browser.window.console.controls.end()
                    self.option_browser.window.console.script.load_simulation("simulations/" + _action)
            else:
                name = Gtk.Buildable.get_name(widget)
                actions = self.option_browser.actions
                if name in actions:
                    # callbacks of GtkButton dosen't need any widget info in my implementation
                    if widget.get_name() == "GtkButton":
                        actions[name]()
                    else:
                        actions[name](widget)
                else:
                    raise KeyError(str(name) + " is not implemented")
                pass

