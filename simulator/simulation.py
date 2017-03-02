import math
import sys
import traceback

from constants import Constants
from signals import Signals
import sim_objects
from timer import Timer
from vector import V, Vector3
from sound import Sound


const = Constants('simulator/constants.ini')


_active_objects = []


class Simulation:

    running = False
    paused = False
    script = ''
    mode = 'stop'

    objects = []
    walls = []
    register = {}
    signals = Signals()

    # y = -9.8, because the up vector is (x=0,y=1,z=0) and this acceleration works downwards
    gravity_of_earth = Vector3(y=-9.8)

    gravitational_constant = 6.67 * 10**(-11)

    def __init__(self):
        self.timer = Timer(self)

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

    def move_object(self, obj):
        time_delta = self.timer.time_delta

        time_delta += obj.time_unused
        obj.time_unused = 0

        # 0. if there is an earth gravity, add it:
        if self.earth_gravity:
            # F = gm
            gravity_force = self.gravity_of_earth * obj.mass

            obj.poke(gravity_force)

        # 1. Calculate resultant force

        # 2. Move it!

        # F = am
        # a = F / m
        #   a = Delta v / t
        # Delta v / t = F / m
        # Delta v = F / m * t

        delta_velocity = obj.get_resultant_force() / obj.mass * time_delta

        obj.delta_velocity = delta_velocity
        obj.velocity += delta_velocity

        obj.position += obj.velocity * time_delta

        obj.clear_momentary_forces()

    def physics(self):

        global _active_objects

        # 1. Find interactions

        # 1.1 wall - ball
        for wall in self.walls:

            for obj in self.objects:

                if wall.collision_with_ball(obj.position, obj.radius):

                    obj.position -= obj.velocity * self.timer.previous_time_delta

                    time_unused = self.timer.previous_time_delta

                    if wall.movable:
                        obj.velocity, wall.velocity = (obj.velocity * (obj.mass - wall.mass) + 2 * wall.mass * wall.velocity) / (obj.mass + wall.mass), (wall.velocity * (wall.mass - obj.mass) + 2 * obj.mass * obj.velocity) / (obj.mass + wall.mass)
                    else:
                        obj.velocity = -obj.velocity

                    for o in _active_objects:
                        _active_objects.remove(o)
                    _active_objects.extend([obj, wall])

                    self.signals.emit('on_collision')

        #map(self.move_object, self.walls)

        # 1.2 ball - ball
        for i, obj_1 in enumerate(self.objects):

            # check obj_1 against others

            for obj_2 in self.objects[len(self.objects)/2+i:]:

                displacement = obj_1.position - obj_2.position
                radius_sum = obj_1.radius + obj_2.radius

                distance = displacement.length()

                if distance <= radius_sum:
                    # So in collision checker we named two states as a collision:
                    #   - when objects are side by side (==)
                    #   - when objects are overlapping themselves (<)

                    # In reality the second state is not called only collision but rather sth like 'collapse'.
                    # To avoid situation where object which is overlapped on another only by lack of precision in our
                    # simulation (then this object might fly throughout another one - really amusing) we need to detect
                    # that state and prevent it.

                    # I think, we need to keep last movement vector to be able to 'move object back' to position where
                    # should be this collision.

                    # to nie rozwiaze w calosci problemu bo zawsze moze cos przeleciec
                    # jesli bedzie sie zbyt szybko poruszac (za maly krok symulacji)

                    time_unused = 0

                    #cofnij i sporboj wymodelowac dokladnie jesli juz po ptakach
                    if distance < radius_sum:

                        # 1.Do zderzenia doszlo teraz, nie bylo go w poprzednim kroku;
                        # moge cofnac sie stanu sprzed zderzenia znajac poprzednia predkosc i poprzedni delta t

                        obj_1.position -= obj_1.velocity * self.timer.previous_time_delta
                        obj_2.position -= obj_2.velocity * self.timer.previous_time_delta

                        displacement = obj_1.position - obj_2.position
                        distance = displacement.length()


                        # ttc - time to collision
                        # vX - velocity of X
                        # pX - position of X in the last step befor collision
                        # rX - radius of X

                        # condition of collision is:

                        # p1 + v1 * ttc + r1 = p2 + v2 * ttc + r2
                        # p1 - p2 + r1 - r2 = v2 * ttc - v1 * ttc
                        # p1 - p2 - (r1 + r2) = ttc (v2 - v1)
                        # [p1 - p2 - (r1 + r2)] / (v2 - v1) = ttc
                        # ttc = [distance - radius_sum] / (v2 - v1)
                        # ttc = [distance - radius_sum] / (velocity_diff)

                        velocity_diff = (obj_2.velocity - obj_1.velocity).length()

                        # don't divide by zero
                        if not (velocity_diff == 0):

                            time_to_collision = (distance - radius_sum) / velocity_diff

                            if time_to_collision < 0:
                                time_to_collision = 0

                            # mam: czas do kolizji, polozenia, predkosci. warunek spotkania: pos1 = pos2
                            # p1s = p2s
                            # p1 + d p1 = p2 + d p2
                            # d p1 = v1 * ttc
                            # d p2 = v2 * ttc

                            # * 0.99, to avoid next machine-precise setbacks
                            obj_1.position += obj_1.velocity * time_to_collision * 0.99
                            obj_2.position += obj_2.velocity * time_to_collision * 0.99

                            time_unused = self.timer.previous_time_delta - time_to_collision

                            obj_1.time_unused = time_unused
                            obj_2.time_unused = time_unused

                        obj_1.velocity -= obj_1.delta_velocity
                        obj_2.velocity -= obj_2.delta_velocity

                    # masy rowne
                    #obj_1.velocity, obj_2.velocity = obj_2.velocity, obj_1.velocity
                    # masy nie rowne
                    obj_1.velocity, obj_2.velocity = (obj_1.velocity * (obj_1.mass - obj_2.mass) + 2 * obj_2.mass * obj_2.velocity) / (obj_1.mass + obj_2.mass), (obj_2.velocity * (obj_2.mass - obj_1.mass) + 2 * obj_1.mass * obj_1.velocity) / (obj_1.mass + obj_2.mass)

                    for o in _active_objects:
                        _active_objects.remove(o)
                    _active_objects.extend([obj_1, obj_2])

                    self.signals.emit('on_collision')

                # if there is an active gravity (between objects), add it:
                if self.gravity:
                    # F = versor(r) * G m1 m2 / (r^2)

                    r = obj_1.position - obj_2.position

                    # gravity_force = r.normalized() * self.gravitational_constant * obj_1.mass * obj_2.mass / (r.length()**2)

                    r_squared_length = r.length_squared()

                    gravity_force = (r / math.sqrt(r_squared_length)) * self.gravitational_constant * obj_1.mass * obj_2.mass / r_squared_length

                    obj_1.poke(-gravity_force)
                    obj_2.poke(gravity_force)

        # 3. Move every object:
        map(self.move_object, self.objects)

    def simulate(self):

        if self.timer.mode == 'stop':
            return True

        self.timer.tick()
        self.physics()
        self.signals.emit('on_simulate')

    def make_a_single_step(self, direction):

        if self.step_size:
            self.timer.step_size = self.step_size

        self.timer.set_mode('step_by_step', direction)
        self.simulate()
        self.timer.set_mode(self.mode, self.get_direction())

    def step_forward(self, waste=''):
        self.make_a_single_step('forward')

    def step_backward(self, waste=''):
        self.make_a_single_step('backward')

    def expose(self):
        from random import uniform as rand

        exposed = {
            'const': const,
            'V': Vector3,
            'Vector3': Vector3,
            'Sound': Sound,
            'active_objects': _active_objects,
            'let': self.let,
            'Force': Vector3,
            'Ball': sim_objects.Ball,
            'Wall': sim_objects.Wall,
            'Box': sim_objects.Box,
            'WallBox': sim_objects.WallBox,
            'simulation': self,
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
        except SyntaxError, err:
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

        self.timer.set_mode(self.mode, self.get_direction())

        return None

    def run(self):
        self.mode = 'real_time'
        self.timer.set_mode(self.mode, self.get_direction())

        if not self.paused:
            sim_objects.Object.register = self.objects
            sim_objects.Wall.register = self.walls
            self.signals.emit('on_load')
        self.signals.emit('on_start')
        self.running = True
        self.paused = False

    def pause(self):
        self.mode = 'stop'
        self.timer.set_mode(self.mode, self.get_direction())

        self.signals.emit('on_pause')
        self.running = False
        self.paused = True

    def end(self):
        self.mode = 'stop'
        self.timer.set_mode(self.mode)

        self.signals.emit('on_end')
        self.running = False
        self.paused = False

        for obj in self.objects:
            del obj
        for obj in self.walls:
            del obj
        for entry in self.register:
            del entry

        # co bylo a nie jest nie liczy sie w rejestr
        self.register = {}
        self.objects = []
        self.walls = []
        self.signals.clear_all()

        # lets reload register to state as it was before run()
        self.set_script(self.script)

