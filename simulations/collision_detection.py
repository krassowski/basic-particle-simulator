# name: Collisions

let('speed', 0.25)

def on_load():

	box_size = 20

	for i in xrange(45):
		mass = rand(0.01, 1)
		radius = rand(0.5, 1.5)
		x = rand(-box_size, box_size)
		y = rand(-box_size, box_size)
		z = rand(-box_size, box_size)
		ball = Ball(x, y, z, mass, radius)
		ball.velocity = V(x =rand(-5, 5), y=rand(-5, 5), z=rand(-5, 5))

	WallBox(box_size + 1, 1000000)


def on_collision():
	for object in active_objects:
		object.color = const.red
	# Sound()
