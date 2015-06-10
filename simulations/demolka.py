# name: Demolka

let('axis', True)
let('grid', False)
let('earth_gravity', False)
let('speed', 5.0)

def on_load():

	p = 20
	y = 5

	for i in xrange(20):
		mass = 1
		radius = 1
		x = rand(-p, +p)
		y = rand(0, 1) + 5
		z = rand(-p, +p)
		ball = Ball(x, y, z, mass, radius)
		ball.color = V(rand(0,1),rand(0,1),rand(0,1))
		ball.velocity = V(x =rand(-5, 5), y=rand(-5, 5), z=rand(-5, 5))

	# Infinity floor
	Wall(y=0, movable=False)

	step = 10
	count = 5
	mass = 0.5

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

