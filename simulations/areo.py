# name: Areo

let('axis', True)
let('grid', False)
let('earth_gravity', False)
let('speed', 3.0)

def on_load():

	p = 20
	y = 5

	for i in xrange(10):
		mass = 1
		radius = 1
		x = rand(-p, +p)
		y = rand(0, 1) + 5
		z = rand(-p, +p)
		ball = Ball(x, y, z, mass, radius)
		ball.color = V(rand(0,1),rand(0,1),rand(0,1))
		ball.velocity = V(x =rand(-5, 5), y=rand(-0.2, 1), z=rand(-5, 5))

	# Infinity floor
	Wall(y=0, movable=False)

	step = 10
	count = 5
	mass = 100000

	for y in xrange(count):
		for i in xrange(count):
			ball = Ball(-count*step/2, y*step, -count*step/2+i*step, mass, 5)


	for y in xrange(count):
		for i in xrange(1,count+1):
			ball = Ball(count*step/2, y*step, -count*step/2+i*step, mass, 5)


	for y in xrange(count):
		for i in xrange(count):
			ball = Ball(-count*step/2+i*step, y*step, count*step/2, mass, 5)

	for y in xrange(count):
		for i in xrange(1,count+1):
			ball = Ball(-count*step/2+i*step, y*step, -count*step/2, mass, 5)


def on_collision():

	objects = filter(lambda obj: obj.type != "wall", active_objects)

	heaviest_object = max(objects, key=lambda obj: obj.mass)

	for object in objects:
		object.color = heaviest_object.color
	#Sound()
