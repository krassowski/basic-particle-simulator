from gi.repository import Gtk
import os
import re

def load_gui(destination, misc, callback):
	simulation_scripts = misc.get_files("simulations", ".py")
	for script in simulation_scripts:
		script_name = script
		with open("simulations/" + script, "r") as script_file:
			regexp = re.compile("name[:=]\s*(.+)")
			for i in range(3):
				line = script_file.readline()
				match = regexp.search(line)
				if match:
					script_name = match.group(1)
					break				

		button = Gtk.Button(label=misc._(script_name))
		button.connect("clicked", callback, script)
		button.set_alignment(0, 0.5)
		destination.add(button)

