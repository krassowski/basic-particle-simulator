# Welcome! Have a look at a basic simulation script:
# name=Point in wall
let('gravity', False)
let('earth_gravity', False)
let("step_size", 0.25)
let("speed", 2)
let("direction", "forward")# or backward
let('axis', True)
let('grid', False)


def on_load():
	global atom
	a = atoms.Gold([0, 0, 0], [0, 0, 1])
	integrator = integrators.EulerIntegrator(0.1)
	system = System('Moj system')
	system.atoms = [a]
	simulation = Simulation('Moja symulacja', system, integrator)
	fields = [
		force_fields.SoftWall([0, 0, 1], [0, 0, 5], 1, 200),
		force_fields.VanDerWaals(system)
	]
	simulation.force_fields = fields
	set_simulation(simulation)
	let('all', locals())
	