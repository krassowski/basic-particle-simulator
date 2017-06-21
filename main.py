#!/usr/bin/env python3
import threading

from internationalize import _
from configuration import Configuration

import sys


sys.path.insert(0, './simulation')
import simulations
import renderer

import gui.windows
import gui.miscellaneous as misc
from gui.windows import message_box

PATH_TO_CONFIG_FILE = "config.ini"


def main():

    config = Configuration(PATH_TO_CONFIG_FILE)

    gtk_version = misc.get_gtk_version()

    if gtk_version < 3.12:
        title = _("You have too old version of GTK+")
        content = _("You shall upgrade your GTK+ to version 3.12 at least. Your GTK+ version is ") + str(gtk_version)
        content += "\n\n" + _("Some functions may not work properly with current GTK+ version.")
        content += "\n" + _("Do you want to continue?")

        response = gui.windows.ask(content, title)

        if response:
            pass
        else:
            return False

    from simulation_manager import SimulationManager, SimulationException
    
    initial_simulation = simulations.simple_simulation()
    simulation_manager = SimulationManager(initial_simulation)

    main_renderer = renderer.Renderer(simulation_manager)

    class WindowThread(threading.Thread):
        def __init__(self, event, simulation_manager, main_renderer, sync):
            threading.Thread.__init__(self)
            self.stopped = event
            self.simulation_manager = simulation_manager
            self.main_renderer = main_renderer
            self.main_window = gui.windows.MainWindow(simulation_manager, config)
            self.main_window.view_area.set_renderer(main_renderer)
            self.interface = sync
            if gtk_version < 3.16:
                self.main_window.show_tip(_("You have an old GTK+ version. If you want to improve an apperance of this application, please upgrade GTK+ to 3.16 version."))

        def run(self):
            exceptions = self.interface.slave_exceptions
            while self.main_window.is_open:
                if exceptions:
                    e = exceptions.pop()
                    message_box(str(e), 'Exception')
                self.main_window.main_iteration()
            self.interface.done.set()
            return

    class SimulatorThread(threading.Thread):
        def __init__(self, event, simulation_manager, sync):
            threading.Thread.__init__(self)
            self.stopped = event
            self.simulation_manager = simulation_manager
            self.fps = 30
            self.interface = sync

        def run(self):
            done = self.interface.done.wait
            timer = self.stopped.wait
            speed = 1 / self.fps
            while not timer(speed) and not done(0):
                try:
                    self.simulation_manager.simulate()
                except SimulationException as e:
                    self.interface.slave_exceptions.append(e)

    class ThreadingInterface:

        def __init__(self):
            self.done = threading.Event()
            self.slave_exceptions = []

    interface = ThreadingInterface()

    stop = threading.Event()
    main_thread = WindowThread(stop, simulation_manager, main_renderer, interface)
    main_thread.start()

    stop = threading.Event()
    slave = SimulatorThread(stop, simulation_manager, interface)
    slave.start()

    main_thread.join()
    slave.join()

    return True

if __name__ == '__main__':

    # True means success
    result = main()

    # And now I want to translate it into Unix convention, so:
    exit(not result)
