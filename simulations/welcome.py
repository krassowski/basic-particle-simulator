# Welcome! Have a look at a basic simulation script:
# name=Welcome!
let("step_size", 0.25)
let("speed", 2)
let('axis', True)
let('grid', False)

def simulation_box(size=15):
	w = lambda x,y : force_fields.SoftWall(x,y,1,1)
	size //= 2
	walls = [
		w([-1, 0, 0], size),
		w([+1, 0, 0], size),
		w([0, -1, 0], size),
		w([0, +1, 0], size),
		w([0, 0, -1], size),
		w([0, 0, +1], size)
	]
	return walls


def on_load():
	#integrator = integrators.EulerIntegrator(1)
	integrator = integrators.VerletIntegrator(0.1)
	system = System('Moj system')
	system_atoms = [atoms.Gold([rand(-50, 50), rand(-50, 50), rand(-50, 50)]) for _ in range(350)]
	system.atoms = system_atoms
	simulation = Simulation('Moja symulacja', system, integrator)
	fields = []
	fields.extend(simulation_box(102))
	fields.append(force_fields.VanDerWaals(system))
	simulation.force_fields = fields
	if type(integrator) is integrators.VerletIntegrator:
		integrator.fill_in_initial_conditions(system, fields)
	set_simulation(simulation)
	let('all', locals())

def on_simulate():
	#print(atom.position)
	pass

def on_collision():
	Sound()
