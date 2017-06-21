# Welcome! Have a look at a basic simulation script:
# name=Bouncing
let("step_size", 0.25)
let("speed", 2)
let('axis', True)
let('grid', False)


def on_load():
	a = atoms.Gold([0, 0, 0], [0, 2, 0])
	time_step = 0.01
	#integrator = integrators.EulerIntegrator(time_step)
	integrator = integrators.VerletIntegrator(time_step)
	system = System('Moj system')
	system.atoms = [a]
	simulation = Simulation('Moja symulacja', system, integrator)
	fields = [
		force_fields.SoftWall([0, 1, 0], -6, 3, 200),
		force_fields.SoftWall([0, 1, 0], 6, 3, 200),
		force_fields.VanDerWaals(system)
	]
	simulation.force_fields = fields
	if type(integrator) is integrators.VerletIntegrator:
		integrator.fill_in_initial_conditions(system, fields)
	set_simulation(simulation)
	let('all', locals())
	