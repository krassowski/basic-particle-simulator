# name: Gas simulation

# You can to turn gravity :)
let("earth_gravity", False)

# Also: you can try to >play< a simulation for a few seconds and then >pause< it,
# change speed to -10 or change "forward" to "backward" in the line below:
let('direction', 'forward')
# and then >play< it again.
# Change you have made could be interpreted as reversion of time direction!

let("speed", 0.5)

def on_load():
	box_size = 15

	for i in xrange(90):
		ball = Ball(x = rand(-box_size, box_size), y = rand(-box_size, box_size), z = rand(-box_size, box_size), mass = rand(1, 50), radius = rand(0.5, 1.5))
		ball.velocity = Vector3(x = rand(-50, 50), y = rand(-50, 50), z = rand(-50, 50))

# You can detect collisions! Uncomment lines below to hear it
# (you need some additional drivers so it is not guaranteed to work)

#def on_collision():
#	Sound()