import timeit


class Timer:

    time_previous = 0
    time_delta = 0
    real_time = True
    step_size = 1
    mode = 'stop'
    directions = {'forward': 1, 'backward': -1}

    def __init__(self, simulation, mode='stop', direction='forward'):
        self.modes = {
            'real_time': self._calculate_real_time_delta,
            'step_by_step': self._calculate_constant_step_delta,
            'stop': lambda: 0
        }
        self.direction = self.directions[direction]
        self.simulation = simulation
        self.restart()
        self.set_mode(mode, direction)
        self.previous_time_delta = None
        self._calculate_time_delta = None

    def restart(self):

        self.time_previous = timeit.default_timer()

    def tick(self):

        self.previous_time_delta = self.time_delta
        self.time_delta = self._calculate_time_delta()

    def set_mode(self, mode='stop', direction='forward'):
        self.mode = mode

        try:
            self.direction = self.directions[direction]
        except KeyError:
            raise ValueError('Unknown direction: ' + direction)
        try:
            self._calculate_time_delta = self.modes[mode]
        except KeyError:
            raise ValueError('Incorrect timer mode: ' + mode)

        self.restart()

    def _calculate_real_time_delta(self):

        time_delta = timeit.default_timer() - self.time_previous

        self.time_previous += time_delta

        # Now we are scaling the time span by the *speed* factor
        # And on the end we are putting into the equation also a direction of passed time

        return time_delta * self.simulation.speed * self.direction

    def _calculate_constant_step_delta(self):

        return self.step_size * self.simulation.speed * self.direction

    def _calculate_time_delta():
        raise RuntimeWarning('_calculate_time_delta() called, but not initialized with set_mode()')

