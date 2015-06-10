# name: Grav box

let('axis', False)
let('grid', False)
let('gravity', True)
let('speed', 25.0)

def on_load():

	# Infinity floor
	Wall(y=0, movable=False)

	step = 10
	count = 5
	mass = 100000000

	for y in xrange(1,count):
		for i in xrange(count):
			ball = Ball(-count*step/2, y*step, -count*step/2+i*step, mass, 5)


	for y in xrange(1,count):
		for i in xrange(1,count+1):
			ball = Ball(count*step/2, y*step, -count*step/2+i*step, mass, 5)


	for y in xrange(1,count):
		for i in xrange(count):
			ball = Ball(-count*step/2+i*step, y*step, count*step/2, mass, 5)

	for y in xrange(1,count):
		for i in xrange(1,count+1):
			ball = Ball(-count*step/2+i*step, y*step, -count*step/2, mass, 5)

