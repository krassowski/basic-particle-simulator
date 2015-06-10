# name: Absortion

let('axis', True)
let('grid', False)
let('earth_gravity', True)
let('speed', 3.0)

def on_load():

	box_size = 3
	y = 5

	for i in xrange(20):
		mass = 1
		radius = 1
		x = rand(box_size, 2*box_size)
		y = rand(box_size, 2*box_size) + y
		z = rand(box_size, 2*box_size)
		ball = Ball(x, y, z, mass, radius)
		ball.color = V(rand(0,1),rand(0,1),rand(0,1))
		ball.velocity = V(x =rand(-50,50), y=rand(-50,50), z=rand(-50,50))

	# heavy, heavy floor but movable - so there bals losses their energy
	Wall(y=0)
	# or alternatively
	# Wall(y=0, movable=False)

def on_collision():

	objects = filter(lambda obj: obj.type != "wall", active_objects)

	heaviest_object = max(objects, key=lambda obj: obj.mass)

	for object in objects:
		object.color = heaviest_object.color
	#Sound()
