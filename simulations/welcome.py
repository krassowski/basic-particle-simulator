# Welcome! Have a look at a basic simulation script:
# name=Welcome!
let("gravity", False)
let("earth_gravity", False)
let("step_size", 0.25)
let("speed", 2)
let("direction", "forward")# or backward
let("axis", True)
let("grid", False)

def on_load():

	V_1 = V(x = 2, y = 0, z = 0)
	V_2 = V(x = -5, y = 0, z = 0)

	big_ball = Ball(x = 0, y = 0, z = 0, mass = 20, radius = 2)
	small_ball = Ball(x = 40, y = 0, z = 0, mass = 1, color = const.red)

	big_ball.velocity = V_1
	small_ball.velocity = V_2

def on_collision():
	Sound()
