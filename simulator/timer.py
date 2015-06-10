import timeit

class Timer():

	time_previous = 0
	time_delta = 0
	real_time = True
	step_size = 1
	mode = "stop"

	def __init__(self, simulation, mode="stop", direction = "forward"):
		self.simulation = simulation
		self.restart()
		self.set_mode(mode, direction)

	def restart(self):

		self.time_previous = timeit.default_timer()

	def tick(self):

		self.previous_time_delta = self.time_delta
		self.time_delta = self._calculate_time_delta()


	def set_mode(self, mode="stop", direction="forward"):
	
		if not direction in ["forward", "backward"]:
			raise ValueError("Unknown direction: "+ direction)

		self.direction = {"forward": 1, "backward": -1}[direction]
		self.mode = mode
				
		if mode == "real_time":
			self._calculate_time_delta = self._calculate_real_time_delta
					
		elif mode == "step_by_step":
			self._calculate_time_delta = self._calculate_constant_step_delta
		
		elif mode == "stop":
			self._calculate_time_delta = lambda: 0
			
		else:
			raise ValueError("Incorrect timer mode: " + mode)
			
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
		raise RuntimeWarning("_calculate_time_delta() called, but not initialized with set_mode()")

