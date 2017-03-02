# name: Demo of boxes

let('speed', 15.5)
let('axis', False)
let('grid', True)

def on_load():

	# set view to front and restart simulation several
	# times to understand where the boxes are placed

	box_size = 15
	mass_of_the_wall = 1000000

	# === You can simply create a box ===

	WallBox(box_size, mass_of_the_wall)

	# above is equivalent to:	

	# Wall(x= box_size, mass=mass_of_the_wall)
	# Wall(x=-box_size, mass=mass_of_the_wall)
	# Wall(y= box_size, mass=mass_of_the_wall)
	# Wall(y=-box_size, mass=mass_of_the_wall)
	# Wall(z= box_size, mass=mass_of_the_wall)
	# Wall(z=-box_size, mass=mass_of_the_wall)

	# Let's put some ball into it (walls are invisible, so we need a "test particle")

	ball = Ball(x = 0, y = 0, z = 0, mass = 1, radius = 1)
	ball.velocity = Vector3(x=rand(-5, 5), y=rand(-5, 5), z=rand(-5, 5))


	# === You can also set position ===

	WallBox(3, mass_of_the_wall, position = V(20, 20, 20) )

	ball = Ball(x=20, y=20, z=20, mass=1, radius =1)
	ball.velocity = Vector3(x=rand(-5, 5), y=rand(-5, 5), z=rand(-5, 5))

	# === WallBox can be movable or not (like walls) ===

	# if box is not movable, mass has no meaning
	WallBox(3, 1, position = V(-20, -20, -20), movable = False)

	ball = Ball(x=-20, y=-20, z=-20, mass=1000000, radius = 1)
	ball.velocity = Vector3(x=rand(-5, 5), y=rand(-5, 5), z=rand(-5, 5))
