from vector import *
import math
import sys
import traceback

from constants import Constants
from timer import Timer
from signals import Signals
from sound import Sound

const = Constants("simulator/constants.ini")

class Object():

	def __init__(self,  x=0, y=0, z=0, mass=1):
		self.position = V(x, y, z)
		self.color = V(1, 1, 0.6)
		self.scale = V()
		self.mass = float(mass)
		self.radius = 1

		# forces with constant "generator"
		self.constant_forces = []

		# there will be short-living forces
		self.momentary_forces = []

		# parameter necessary to mask poor precision of simulation
		self.time_unused = 0
		self.velocity = Vector3()
		self.delta_velocity = Vector3()

	def get_resultant_force(self):
		return reduce(lambda x, y: x + y, self.constant_forces + self.momentary_forces, V())

	def poke(self, force):
		self.momentary_forces.append(force)

	def push(self, force):
		self.constant_forces.append(force)

	def clear_momentary_forces(self):

		for force in self.momentary_forces:
			del force

		self.momentary_forces = []


class Simulation():

	running = False
	paused = False
	script = ""
	mode = "stop"

	def __init__(self):
		self.timer = Timer(self)

	objects = []
	walls = []
	register = {}
	signals = Signals()

	# y = -9.8, because the up vector is (x=0,y=1,z=0) and this acceleration works downwards
	gravity_of_earth = Vector3(y=-9.8)

	gravitational_constant = 6.67 * 10**(-11)

	def __getattr__(self, attribute):
		return self.get(attribute)

	def get_direction(self):
		if not self.direction:
			return "forward"
		return self.direction

	def get(self, attribute):
		if attribute in self.register:
			return self.register[attribute]
		else:
			return False

	def let(self, variable, value):
		self.register[variable] = value

	def create_ball(self, *args, **kwargs):
		ball = self.Ball(*args, **kwargs)
		self.objects.append(ball)
		return ball

	def create_wall(self, *args, **kwargs):
 		wall = self.Wall(*args, **kwargs)
		self.walls.append(wall)
		return wall

	def create_box(self, size, mass_of_wall=1000, position=None, movable=True):

 		if not position:
			position = V(0,0,0)

		self.create_wall(x=position.x + size, mass=mass_of_wall, movable=movable)
		self.create_wall(x=position.x - size, mass=mass_of_wall, movable=movable)
		self.create_wall(y=position.y + size, mass=mass_of_wall, movable=movable)
		self.create_wall(y=position.y - size, mass=mass_of_wall, movable=movable)
		self.create_wall(z=position.z + size, mass=mass_of_wall, movable=movable)
		self.create_wall(z=position.z - size, mass=mass_of_wall, movable=movable)

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

		global active_objects

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

					active_objects = [obj, wall]

					self.signals.emit("on_collision")

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

					# In reality the second state is not called only collision but rather sth like "collapse".
					# To avoid situation where object which is overlapped on another only by lack of precision in our
					# simulation (then this object might fly throughout another one - really amusing) we need to detect
					# that state and prevent it.

					# I think, we need to keep last movement vector to be able to "move object back" to position where
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

					active_objects = [obj_1, obj_2]

					self.signals.emit("on_collision")


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

		if self.timer.mode == "stop":
			return True

		self.timer.tick()
		self.physics()
		self.signals.emit("on_simulate")


	def make_a_single_step(self, direction):

		if self.step_size:
			self.timer.step_size = self.step_size

		self.timer.set_mode("step_by_step", direction)
		self.simulate()
		self.timer.set_mode(self.mode, self.get_direction())


	def step_forward(self, waste=""):
		self.make_a_single_step("forward")


	def step_backward(self, waste=""):
		self.make_a_single_step("backward")

	def set_script(self, script):

		from random import uniform as rand

		on_load = None
		on_start = None
		on_pause = None
		on_end = None
		on_simulate = None
		on_collision = None

		global let, Force, Ball, Wall, Box, rand, simulation, active_objects

		let = self.let
		Force = Vector3
		Ball = self.create_ball
		Wall = self.create_wall
		Box = self.create_box
		simulation = self

		try:
			self.script = script
			exec self.script
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

		self.signals.update("on_load", on_load)
		self.signals.update("on_start", on_start)
		self.signals.update("on_pause", on_pause)
		self.signals.update("on_end", on_end)
		self.signals.update("on_simulate", on_simulate)
		self.signals.update("on_collision", on_collision)

		self.timer.set_mode(self.mode, self.get_direction())

		return None

	def run(self):
		self.mode = "real_time"
		self.timer.set_mode(self.mode, self.get_direction())

		if not self.paused:
			self.signals.emit("on_load")
		self.signals.emit("on_start")
		self.running = True
		self.paused = False

	def pause(self):
		self.mode = "stop"
		self.timer.set_mode(self.mode, self.get_direction())

		self.signals.emit("on_pause")
		self.running = False
		self.paused = True

	def end(self):
		self.mode = "stop"
		self.timer.set_mode(self.mode)

		self.signals.emit("on_end")
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

	class Ball(Object):

		def __init__(self,  x=0, y=0, z=0, mass=1, radius=1, color=""):
			Object.__init__(self, x, y, z, mass)
			self.type = "ball"
			self.radius = radius
			if color:
				self.color = color
			self.scale = V(radius, radius, radius)


	# Wall should always be perpendicular to axis.
	# Only because it's easier to code it ;)
	class Wall(Object):

		# if not on the same side of wall
		def _collison_x(self, center, radius):
			return self.position.x > center.x - radius and self.position.x < center.x + radius

		def _collison_y(self, center, radius):
			return self.position.y > center.y - radius and self.position.y < center.y + radius

		def _collison_z(self, center, radius):
			return self.position.z > center.z - radius and self.position.z < center.z + radius


		def __init__(self,  x=None, y=None, z=None, mass=1000, movable=True):

			self.movable = movable

			if (x is None and y is None and z is None) or (x and y) or (x and z) or (y and z):
				raise Exception("Walls needs a single plan")

			if x is not None:
				self.collision_with_ball = self._collison_x
			else:
				x = 0

			if y is not None:
				self.collision_with_ball = self._collison_y
			else:
				y = 0

			if z is not None:
				self.collision_with_ball = self._collison_z
			else:
				z = 0


			Object.__init__(self, x, y, z, mass)
   			self.type = "wall"

