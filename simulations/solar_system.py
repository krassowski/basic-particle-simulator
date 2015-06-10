# name: Solar system
let("gravity", True)
let("axis", True)
let("speed", 130000)

def on_load():

	# Jak przeskalowac odleglosc?
	# F1 = G (Mm)/r1^2
	# F2 = G (M)/r2^2*m
	# F1 = F2
	# r2^2 = r1^2/m^2

	sun = Ball(x = 0, y = 0, z = 0, mass = const.sun_mass/const.earth_mass, radius = const.sun_radius/const.earth_radius, color=const.blue)
	earth = Ball(x = 200, y = 0, z = 0, mass = 1, radius = 1, color=const.white)

	# Average orbital speed of earth: 29.78
	earth.velocity = Vector3(z = 0.0003)
	print "Should_be_distance:" + str(const.sun_earth_distance)#149.6
