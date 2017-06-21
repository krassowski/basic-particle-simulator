# Welcome! Have a look at a basic simulation script:
# name=Head-on collision
let("step_size", 0.25)
let('speed', 60.0)
let('axis', True)
let('grid', False)


def on_load():
	my_atoms = [
		atoms.Gold([-5, 0, 0], [1, 0, 0]),
		atoms.Gold([+10, 0, 0], [-1, 0.1, 0]),
		atoms.Gold([-5, 0, 5], [1, 0, 0]),
		atoms.Gold([+5, 0, 5], [-1, 0, 0]),
		#atoms.Gold([-5, 0, 5], [1, 0, 0]),
		#atoms.Gold([+5, 0, 5], [-1, 0, 0])
	]
	time_step = 0.01
	integrator = integrators.EulerIntegrator(time_step)
	#integrator = integrators.VerletIntegrator(time_step)
	system = System('Moj system')
	system.atoms = my_atoms
	simulation = Simulation('Moja symulacja', system, integrator)
	fields = [
		force_fields.VanDerWaals(system)
	]
	simulation.force_fields = fields
	if type(integrator) is integrators.VerletIntegrator:
		integrator.fill_in_initial_conditions(system, fields)
	set_simulation(simulation)
	let('all', locals())
	