# Welcome! Have a look at a basic simulation script:
# name=Crystal and a ball
let("step_size", 0.25)
let("speed", 350)
let('axis', True)
let('grid', False)

def build_box(size=50, spacing=1):
	all_atoms = []
	spacing *= 2
	s = size // 2
	b = - s * spacing
	for x in range(-s, s+1):
		for y in range(-s, s+1):
			for z in range(-s, s+1):
				all_atoms.append(atoms.Gold([x * spacing, y * spacing, z * spacing]))
	return all_atoms

def on_load():
	time_step = 0.005
	#integrator = integrators.EulerIntegrator(time_step)
	integrator = integrators.VerletIntegrator(time_step)
	system = System('Moj system')
	size = 5
	#atom = lambda pos, size: atoms.Gold(pos, size)
	atom = lambda pos, size: Atom(position=pos, velocity=size, mass=500, radius=5)
	my_atoms = [
		#atoms.Gold([size * 10, 0, 0], [-15, 0, 0])	# center
		#atoms.Gold([size * 5, 0, size * 5], [-5, 0, -5])	# edge
		atom([size * 5, size * 5, size * 5], [-5, -5, -5])	# vertex
	]
	crystal = build_box(size, atoms.Gold().radius())
	my_atoms.extend(crystal)
	system.atoms = my_atoms
	simulation = Simulation('Moja symulacja', system, integrator)
	fields = [
		#force_fields.SoftWall([0, 0, 1], [0, 0, 5], 2, 200),
		force_fields.VanDerWaals(system)
	]
	simulation.force_fields = fields
	if type(integrator) is integrators.VerletIntegrator:
		integrator.fill_in_initial_conditions(system, fields)
	set_simulation(simulation)
	let('all', locals())
	