# name: Gas in box

# You can to turn gravity :)
let("earth_gravity", False)

let('speed', 1.0)

def on_load():
	box_size = 15

	for i in xrange(70):
		mass = rand(0.01, 1)
		radius = rand(0.5, 1.5)
		x = rand(-box_size, box_size)
		y = rand(-box_size, box_size)
		z = rand(-box_size, box_size)
		ball = Ball(x, y, z, mass, radius)
		ball.velocity = V(x =rand(-5, 5), y=rand(-5, 5), z=rand(-5, 5))

	# to mimimalize simulation artefacts at start (balls outside box)
	box_size += 1	

	# lower mass of wall (1000000) to see sth like pV=nRT
	Box(box_size, 1000000)


#def on_collision():
#	Sound()
