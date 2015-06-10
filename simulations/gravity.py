#name: Gravity
let("gravity", True)
let("axis", True)
let("speed", 10000)

def on_load():
	for i in xrange(10):
		ball = Ball(x = rand(-15, 15), y = rand(-15, 15), z = rand(-15, 15), mass = rand(100000, 500000), radius = rand(0.5, 1.5))