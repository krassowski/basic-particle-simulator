# name: Some funny stuff

let('axis', True)
let('grid', False)
let('earth_gravity', True)
let('speed', 3.0)

def on_load():

	y = 5

	# Infinity floor
	Wall(y=0, movable=False)

	step = 5
	count = 5

	for y in xrange(1,count+1):
		for i in xrange(count):
			ball = Ball(0, y*step, i*step, 1000000, 5)
