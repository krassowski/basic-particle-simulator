import math
import sys
import traceback

from vector import V, Vector3
from simulation_manager.constants import Constants
from simulation_manager.signals import Signals
from simulation_manager.timer import Timer
from simulation_manager.sound import Sound


const = Constants('simulator/constants.ini')


class Dot(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def module_members(module):
    return Dot({
        name: getattr(module, name)
        for name in dir(module)
        if not name.startswith('_')
    })



class SimulationManager:

    script = ''
    mode = 'stop'

    register = {}
    signals = Signals()

    # y = -9.8, because the up vector is (x=0,y=1,z=0) and this acceleration works downwards
    gravity_of_earth = Vector3(y=-9.8)

    gravitational_constant = 6.67 * 10**(-11)

    def __init__(self, initial_simulation):
        self.set_simulation(initial_simulation)
 
    def set_simulation(self, simulation):
        self.simulation = simulation
        from renderer import AtomRepresentation
        self.atoms = [
            AtomRepresentation(atom)
            for atom in self.simulation.system.atoms
        ]

    def __getattr__(self, attribute):
        try:
            return self.get(attribute)
        except KeyError:
            return
            # raise AttributeError

    def get_direction(self):
        if not self.direction:
            return 'forward'
        return self.direction

    def get(self, attribute):
        return self.register[attribute]

    def let(self, variable, value):
        self.register[variable] = value

    def simulate(self):

        if self.mode != 'run':
            return True

        self.simulation.tick()
        #self.signals.emit('on_simulate')

    def make_a_single_step(self, direction):

        # self.timer.set_mode('step_by_step', direction)
        self.simulate()
        # self.timer.set_mode(self.mode, self.get_direction())

    def step_forward(self, waste=''):
        self.make_a_single_step('forward')

    def step_backward(self, waste=''):
        self.make_a_single_step('backward')

    def expose(self):
        from random import uniform as rand
        import atom
        import integrator
        import system
        import simulation
        import forcefield
        
        exposed = {
            'const': const,
            'V': Vector3,
            'Vector3': Vector3,
            'Sound': Sound,
            'let': self.let,
            #'Force': Vector3,
            'Atom': atom.Atom,
            'integrators': module_members(integrator),
            'atoms': module_members(atom),
            'force_fields': module_members(forcefield),
            'System': system.System,
            'Simulation': simulation.Simulation,
            'set_simulation': self.set_simulation,
            'rand': rand
        }

        for signal in self.signals.names:
            exposed[signal] = None

        return exposed

    def set_script(self, script):
        exposed = self.expose()

        try:
            self.script = script
            exec (self.script, exposed, exposed)
            error = None
        except SyntaxError as err:
            error_class = err.__class__.__name__
            line_number = err.lineno
            error = (error_class, err, line_number, None)
        except Exception as err:
            error_class = err.__class__.__name__
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            error = (error_class, err, line_number)

        if error:
            return error

        for signal in self.signals.names:
            self.signals.update(signal, exposed[signal])

        #self.timer.set_mode(self.mode, self.get_direction())

        return None

    def run(self):
        if self.mode != 'pause':
            self.signals.emit('on_load')
            
        self.mode = 'run'

        self.simulation.running = True
        self.signals.emit('on_start')

    def plot_energies(self):
        energies = self.simulation.history.energies
        
        import matplotlib.pyplot as plt
        
        for energy_name, values in energies.items():
            print(len(self.simulation.history.timesteps), self.simulation.history.timesteps)
            print(len(values), values)
            plt.plot(
                self.simulation.history.timesteps,
                values,
                label=energy_name
            )
            
        plt.xlabel('Timestep')
        plt.ylabel('Energy')

        plt.legend()
            
        plt.show()

    def pause(self):
        self.mode = 'pause'
        self.signals.emit('on_pause')

    def end(self):
        self.mode = 'stop'
        self.signals.emit('on_end')
        
        for entry in self.register:
            del entry

        # co bylo a nie jest nie liczy sie w rejestr
        self.register = {}
        self.signals.clear_all()

        # lets reload register to state as it was before run()
        self.set_script(self.script)

