# name: Propagation

let('grid', True)
let('speed', 0.25)

def on_load():

	box_size = 5

	for i in xrange(10):
		mass = rand(0.01, 1)
		radius = rand(0.5, 1.5)
		x = rand(-box_size, box_size)
		y = rand(-box_size, box_size)
		z = rand(-box_size, box_size)
		ball = Ball(x, y, z, mass, radius)
		ball.color = V(rand(0,1),rand(0,1),rand(0,1))
		ball.velocity = V(x =rand(-50,50), y=rand(-50,50), z=rand(-50,50))

	Box(box_size + 4, 1000000)


def on_collision():

	objects = filter(lambda obj: obj.type != "wall", active_objects)

	heaviest_object = max(objects, key=lambda obj: obj.mass)

	for object in objects:
		object.color = heaviest_object.color
