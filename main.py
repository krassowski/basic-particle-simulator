#!/usr/bin/env python3
from internationalize import _
from configuration import Configuration

import sys
sys.path.insert(0, './simulation')
import simulations
import renderer

import gui.windows
import gui.miscellaneous as misc

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

    from simulation_manager import SimulationManager
    
    initial_simulation = simulations.simple_simulation()
    simulation_manager = SimulationManager(initial_simulation)

    main_renderer = renderer.Renderer(simulation_manager)
    main_window = gui.windows.MainWindow(simulation_manager, config)
    main_window.view_area.set_renderer(main_renderer)

    if gtk_version < 3.16:
        main_window.show_tip(_("You have an old GTK+ version. If you want to improve an apperance of this application, please upgrade GTK+ to 3.16 version."))

    ### FPS COUNTER CODE, part I:
    # from simulator.timer import Timer
    # fps = Timer(main_simulation, mode="real_time")
    # main_simulation.speed = 1
    # fps_list = [1] * 50
    ###


    while main_window.is_open:

        simulation_manager.simulate()

        # Rendering is called there only, to ensure that every simulation step has
        # impact on displayed image. It's only one of places where the rendering function
        # is executed (see comment below)
        main_renderer.render()

        # And there is a function giving control of our resources to the GTK library.
        # The execution of that func. will last until every waiting GUI event is handled.
        # If there was any pending window movement or cursor movement, the GTK library will call "redraw" signal.
        # That signal is connected to our rendering function (thanks to Window.view_area subclass)
        main_window.main_iteration()

        ### FPS COUNTER CODE, part II:
        #fps.tick()
        #fps_list.append(fps.time_delta)
        #fps_list.pop(0)
        #print 1.0 / (sum(fps_list) / 50.0)
        ###

    return True

if __name__ == '__main__':

    # True means success
    result = main()

    # And now I want to translate it into Unix convention, so:
    exit(not result)
