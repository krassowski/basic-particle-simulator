# Welcome! Have a look at a basic simulation script:
# name=Gold Gold Gold
let("gravity", False)
let("earth_gravity", False)
let("step_size", 0.25)
let("speed", 2)
let("direction", "forward")# or backward
let('axis', True)
let('grid', False)

def simulation_box(size=15):
	w = force_fields.SoftWall
	size //= 2
	walls = [
		w([-size, 0, 0], size),
		w([+size, 0, 0], size),
		w([0, -size, 0], size),
		w([0, +size, 0], size),
		w([0, 0, -size], size),
		w([0, 0, +size], size)
	]
	return walls

atom = None
all = []

def on_load():
	global atom
	a = atoms.Gold([0, 0, 10], [0, 0, -0.01])
	all.append(a)
	b = atoms.Gold()
	all.append(b)
	integrator = integrators.EulerIntegrator(10)
	all.append(integrator)
	system = System('Moj system')
	all.append(system)
	system.atoms = [a, b]
	simulation = Simulation('Moja symulacja', system, integrator)
	fields = []
	#fields.extend(simulation_box(10))
	f = force_fields.VanDerWaals(system)
	fields.append(f)
	simulation.force_fields = fields
	let('all', locals())	
	set_simulation(simulation)
	
def on_simulate():
	#print(atom.position)
	pass

def on_collision():
	Sound()
