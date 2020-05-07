from System import System
from StartingValues import Actors, SpinValues
from Loose import config_to_Json, print_energy_degeneracy, Simulation
from numpy import heaviside

Test = System(Actors, SpinValues, Hamiltonian_to_use='V')

print_energy_degeneracy(Test)

Simulation(Test, update='chronological', prefactor_function=heaviside)

config_to_Json(Test)
