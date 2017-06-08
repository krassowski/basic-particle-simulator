from internationalize import _
import gi
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import Pango
from gui.highlighter import Highlighter
import gui.miscellaneous as misc
import re


class Console:

    def __init__(self, option_browser, simulation):

        self.option_browser = option_browser
        self.simulation = simulation
        #simulation_keywords = simulation.expose().keys()
        simulation_keywords = []
        self.script = self.Script(self, simulation_keywords)
        self.controls = self.Controls(self.script, self.simulation)

        self.gui = self.script.gui

        self.gui.set_size_request(250, 115)
        self.gui.show()

    class Script:

        def __init__(self, console, simulation_keywords):
            self.simulation_keywords = simulation_keywords
            self.gui = Gtk.Table()
            self.window = Gtk.ScrolledWindow()
            self.console = console

            self.prevent_button_update = False
            self._textview = Gtk.TextView()

            self._textbuffer = GtkSource.Buffer()
            self._textview.set_buffer(self._textbuffer)

            self._textbuffer.set_max_undo_levels(-1)
            self._textbuffer.set_undo_manager(None)

            self._textbuffer.connect("changed", self.on_text_changed)
            self._textbuffer.connect("paste-done", self.on_text_changed)

            self.error_tag = self._textbuffer.create_tag("error", background="orange")

            font_description = Pango.FontDescription("monospace 9")
            self._textview.modify_font(font_description)

            misc.set_tabs(self._textview, font_description, 4)

            self.window.set_shadow_type(Gtk.ShadowType.IN)
            misc.gtk_set_margin(self.gui, 5, top=10)

            # Init highlight:
            self.highlight = Highlighter(self._textbuffer)
            self.load_highlight()

            self.error_bar = Gtk.InfoBar()
            self.error_bar_label = Gtk.Label()
            self.error_bar.get_content_area().add(self.error_bar_label)
            self.error_bar_label.show()

            self.error_bar.set_message_type(Gtk.MessageType.ERROR)

            self.window.add(self._textview)
            #self.error_bar.set_size_request(80, 100)

            self.gui.attach(self.window, 0, 8, 0, 1)
            self.gui.attach(self.error_bar, 8, 10, 0, 1)

            self.error_bar.set_no_show_all(True)

            # Init script
            self.load_simulation("./simulations/welcome.py")


        def on_text_changed(self, x='', y=''):
            self.highlight.perform()
            error = None
            if hasattr(self.console, "controls"):
                error = self.console.controls.refresh()

            if not error:
                if self.prevent_button_update:
                    self.prevent_button_update = False
                else:
                    self.try_update_button_states()
                if hasattr(self.console, "controls"):
                    self.error_bar.hide()
            else:
                error_name = error[0]
                exception = error[1]
                line = error[2]
                self.highlight_error_line(line)
                if hasattr(self.console, "controls"):

                    messsage = _(error_name)
                    messsage = '<span weight="bold">' + _(error_name) + ':</span>\n'

                    args = exception.args

                    if error_name in ["IndentationError", "SyntaxError"]:
                        pos = args[1][2]
                        wrong_line = args[1][3]
                        messsage += "\n" + _(args[0])
                        messsage += "\n" + '<span style="italic">' + wrong_line + '</span>'
                    elif error_name in ["NameError"]:
                        print(exception)
                        print(exception.args)
                        name = args[0][6:][:-16]
                        messsage += "\n" + _("name '%s' is not defined") % name
                    elif error_name in ["AttributeError"]:
                        print(exception.args)
                        match = re.search("no attribute '(.*?)'", args[0])
                        name = match.group(1)
                        match = re.search("'(.*?)' object", args[0])
                        obj = match.group(1)
                        messsage += "\n" + _("'%s' object has no attribute '%s'") % (obj, name)
                    else:
                        print(exception.args)
                        messsage += "\n" + str(exception)

                    self.error_bar_label.set_markup('<span foreground="black">' + messsage + '</span>')

                    self.error_bar.show()

        def get_functions_data(self, name, max_args=0):

            script = self.get_script()
            functions = []

            reg_str = name + "\("
            for i in range(max_args):
                reg_str += "("

                if i > 0:
                    reg_str += ",\s*"
                reg_str += "(.*?)"
                reg_str += ")?"
            reg_str += "\)"

            regexp_object = re.compile(reg_str)

            for match in regexp_object.finditer(script):

                entry = []

                d = {
                    'element': match.group(0),
                    'start': match.start(0),
                    'end': match.end(0)
                }

                entry.append( d )

                for i in range(max_args):
                    try:
                        arg = eval(match.group(2 + 2*i))
                    except:
                        arg = False
                    entry.append(arg)

                functions.append(entry)

            return functions

        def try_update_button_states(self):

            # 1. Let
            # regexp wyszukujacy let(option_name, value_from_script),
            # Z zapisem do listy register w postaci rekordow:
            # register[option_name] = value_from_script
            register_change = {}

            lets_data = self.get_functions_data('let', 2)

            for data in lets_data:
                if data[1] and data[2]:

                    value = False

                    try:
                        option_name = data[1]
                        value = data[2]
                        register_change[option_name] = value
                    except:
                        pass

            # pobieram z option_browsera informacje o dostepnych let-ach
            # i ustawiam wszystkie na False. Potem aktualizuje liste dostepnych
            # let-ow lista register (aby wyeliminowac usuniete w skrypcie let-y)
            available = self.console.option_browser.get_let_actions_list()

            register = {}

            for let in available:
                register[let] = False

            register.update(register_change)

            register = register.items()

            self.console.option_browser.update_button_states_from_register(register)
            # 2. ...

        def undo(self):
            if self._textbuffer.can_undo():
                self._textbuffer.undo()

        def redo(self):
            if self._textbuffer.can_redo():
                self._textbuffer.redo()

        def insert(self, *args, **kwargs):
            self.insert_or_modify(True, *args, **kwargs)

        def modify(self, *args, **kwargs):
            """
            try to find object specified by identity of x first arguments
            and modify them (where x is given by 'identities' keyword argument)
            otherwise add new object with specified variables
            """
            self.insert_or_modify(False, *args, **kwargs)

        def insert_or_modify(self, force_new_instance, *args, **kwargs):
            """

            where - on_top, on_bottom, after_comments
            into - script_body, <function_name>

            """
            # whether to insert new instances on top or bottom of script
            where = kwargs.pop('where', "on_bottom")
            into = kwargs.pop('into', "script_body")

            # if the force_new_instance is true,
            # we will not modify exiting objects, but always add new
            # otherwise it will modify all existing object of specified
            # (by first 'non-self' positional argument) name.
            # It's possible to specify number of arguments that have to be identical,
            # to modify existing a function

            identities = kwargs.pop('identities', 1)

            args = list(args)
            object_type = args.pop(0)
            name = args.pop(0)

            if object_type in ["function", "object"]:
                new_func = misc.create_function_str(name, *args)

                if force_new_instance:
                    return self.insert_into_buffer(new_func, where, into)

                replaced = False

                if identities > len(args):
                    raise Exception("Wrong arguments: identities higher than number of non-special arguments (all arguments excep self, object_type and name)")

                data_list = self.get_functions_data(name, len(args))

                for data in data_list:
                    good_match = True
                    for i in range(identities):
                        if args[i] != data[1 + i]:
                            good_match = False
                    if good_match:
                        self.replace_on_pos(data[0]["start"], data[0]["end"], new_func)
                        replaced = True

                if not replaced:
                    return self.insert_into_buffer(new_func, where, into)

            #if obj_type == class_function: (ball.push(...))
            #if obj_type == class_property: (ball.velocity = ...)
            #if obj_type == comment: (# name = Nazwa symulacji)

            else:
                raise ValueError("object_type: " + str(object_type) + " is not defined")

        def replace_on_pos(self, start, end, new_text):
            start = self._textbuffer.get_iter_at_offset(start)
            end = self._textbuffer.get_iter_at_offset(end)
            self.prevent_button_update = True
            self._textbuffer.delete(start, end)
            self.prevent_button_update = True
            self._textbuffer.insert(start, new_text)

        def insert_into_buffer(self, new_text, where, into):
            if where in ["on_top", "after_comments"]:

                offset = 0

                if where == "after_comments":

                    script = self.get_script()

                    inside_doc_string = False

                    for line in script.split("\n"):

                        raw_line = line.strip()

                        if not raw_line:
                            offset += len(line) + 1
                            break

                        if inside_doc_string:
                            if raw_line[-3:] == '"""':
                                inside_doc_string = False
                            offset += len(line) + 1
                            continue
                        else:
                            # TODO: could docstring by with '''?
                            if raw_line[:3] == '"""':
                                if raw_line[-3:] != '"""':
                                    inside_doc_string = True
                                offset += len(line) + 1
                                continue

                        # if line is comment
                        if raw_line[0] == "#":
                            offset += len(line) + 1
                        else:
                            if not inside_doc_string:
                                break

                new_text += "\n"
                iterator = self._textbuffer.get_iter_at_offset(offset)
            else:
                iterator = self._textbuffer.get_end_iter()
                new_text = "\n" + new_text

            self._textbuffer.insert(iterator, new_text)

        def highlight_error_line(self, line_number):

            start = self._textbuffer.get_iter_at_line(line_number - 1)
            end = self._textbuffer.get_iter_at_line(line_number)

            self._textbuffer.apply_tag(self.error_tag, start, end)

        def load_simulation(self, path):

            script = misc.file_get_contents(path)

            self.set_script(script)
            self.path = path

        def save_simulation(self, path):
            self.path = path
            script = self.get_script()
            misc.file_put_contents(path, script)

        def load_highlight(self):
            python_tfn = ["None", "True", "False", "-?\d+\.\d+", "-?\d+"]
            python_statements = [
                "nonlocal", "and", "as", "assert", "break", "class", "continue", "def", "del", "elif",
                "else", "except", "exec", "finally", "for", "from", "global", "if", "import", "in",
                "is", "lambda", "raise", "return", "not", "or", "pass", "print", "try", "while", "with", "yield"
            ]
            self.highlight.add_words(python_statements, "statements", foreground="brown", weight=Pango.Weight.BOLD)
            self.highlight.add_words(python_tfn, "tfn", foreground="purple")
            self.highlight.add_words(self.simulation_keywords, "sim_func", foreground="green")
            self.highlight.add([re.compile("(?P<highlight>const)([.]+)")], "const", foreground="green", weight=Pango.Weight.NORMAL)
            self.highlight.add([re.compile("[\"](.*?)[\"]|['](.*?)[']")], "string", foreground="purple", weight=Pango.Weight.NORMAL)
            self.highlight.add([re.compile("def([\s])(?P<highlight>(.*?))\((.*?)\):")], "after_def", foreground="purple", weight=Pango.Weight.NORMAL)
            # comment must be last (color overriding)
            self.highlight.add([re.compile("#(.)*")], "comment", foreground="blue", weight=Pango.Weight.NORMAL)

        def set_script(self, text):

            self._textbuffer.begin_not_undoable_action()
            self._textbuffer.set_text(text)
            self._textbuffer.end_not_undoable_action()

        def get_script(self):

            start_iter = self._textbuffer.get_start_iter()
            end_iter = self._textbuffer.get_end_iter()

            return self._textbuffer.get_text(start_iter, end_iter, True)

    class Controls():

        def __init__(self, script, simulation):

            self.simulation = simulation
            self.script = script

            self.gui = Gtk.Table()


            self.run_pause_button = misc.IconicButton("media-playback-start-symbolic", _("Run simulation"))
            end = misc.IconicButton("media-playback-stop-symbolic", _("End simulation"))

            step_forward = misc.IconicButton("media-seek-forward-symbolic", _("Step forward"))
            step_backward = misc.IconicButton("media-seek-backward-symbolic", _("Step backward"))
            help_me = misc.IconicButton("system-help-symbolic", _("Help"))

            self.run_pause_button.connect("clicked", self.run_pause)
            end.connect("clicked", self.end)

            step_forward.connect("clicked", self.simulation.step_forward)
            step_backward.connect("clicked", self.simulation.step_backward)
            help_me.connect("clicked", misc.help_me)

            self.gui.attach(self.run_pause_button, 0, 2, 0, 1)
            self.gui.attach(end, 2, 3, 0, 1)
            self.gui.attach(step_backward, 0, 1, 1, 2)
            self.gui.attach(step_forward, 1, 2, 1, 2)
            self.gui.attach(help_me, 2, 3, 1, 2)

            self.gui.set_valign(Gtk.Align.END)
            self.gui.set_halign(Gtk.Align.END)
            misc.gtk_set_margin(self.gui, right=25, bottom=25)

            self.refresh()

        def run_pause(self, button):

            if self.simulation.mode == 'stop':
                self.refresh()

            if self.simulation.mode != 'run':
                button.set_image(misc.get_icon_image("media-playback-pause-symbolic"))
                button.set_tooltip_text(_("Pause simulation"))
                self.simulation.run()
            else:
                button.set_image(misc.get_icon_image("media-playback-start-symbolic"))
                button.set_tooltip_text(_("Run simulation"))
                self.simulation.pause()
                
        # The optional argument's ("waste") are there to allow passing additional data from GUI calls
        # (GTK always want to give us a reference to calling object in callback - take look above) but we really
        # don't need them. If they were removed, the Python Interpreter will be mad and all off our efforts will go off

        def refresh(self, waste=''):
            return self.simulation.set_script(self.script.get_script())

        def end(self, waste=''):
            self.run_pause_button.set_image(misc.get_icon_image("media-playback-start-symbolic"))
            self.run_pause_button.set_tooltip_text(_("Run simulation"))
            self.simulation.end()
