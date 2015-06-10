# name: Demo of signals
let("speed", 5)
let("axis", True)

def on_load():

	global big_ball, small_force, small_ball

	small_force = Force(x = 15, y = 0, z = 0)

	small_ball = Ball(x = 0, y = 0, z = 0, mass = 1)
	big_ball = Ball(x = 20, y = 0, z = 0, mass = 20, radius = 2)

	small_ball.push(small_force)
	big_ball.push(small_force)


def on_start():
	print "Some text on begining"
	print "Let's speed up big_ball!"
	big_ball.push(small_force)

def on_pause():
	print "If you see it, someone has clicked a pause button"

def on_end():
	print "This is the end"
	print "Final position of big ball:   " + str(big_ball.position)
	print "Final position of small ball: " + str(small_ball.position)
	print "Thank you"

def on_simulate():
	#print "Big ball is on position: " + str(big_ball.position)
	pass

def on_collision():
	Sound()
