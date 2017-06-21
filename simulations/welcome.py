# Welcome! Have a look at a basic simulation script:
# name=Welcome!
let("step_size", 0.25)
let('speed', 60.0)
let('axis', True)
let('grid', False)

def simulation_box(size=15):
	w = lambda x,y : force_fields.SoftWall(x,y,1,200)
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

def place_atoms_in_box(size=50, count=100):
	created_atoms = []
	for _ in range(count):
		well_placed = False
		s = 0.5
		speed = [rand(-s, s) for _ in range(3)]
		while not well_placed:
			position = [rand(-size, size), rand(-size, size), rand(-size, size)]
			atom = atoms.Gold(position, speed)
			well_placed = not any([(abs(other.position-atom.position)<2.0).all() for other in created_atoms])
		created_atoms.append(atom)
	return created_atoms


def on_load():
	#integrator = integrators.EulerIntegrator(1)
	integrator = integrators.VerletIntegrator(0.1)
	system = System('Moj system')
	box_size = 50
	#system_atoms = [atoms.Gold([rand(-50, 50), rand(-50, 50), rand(-50, 50)]) for _ in range(550)]
	system_atoms = place_atoms_in_box(box_size, 500)
	system.atoms = system_atoms
	simulation = Simulation('Moja symulacja', system, integrator)
	fields = []
	fields.extend(simulation_box(2 * box_size + 4))
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
