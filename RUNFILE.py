from System import System
from StartingValues import Actors, SpinValues
from Loose import config_to_Json, print_energy_degeneracy, Simulation

Test = System(Actors, SpinValues, Hamiltonian_to_use='B')

print_energy_degeneracy(Test)

Simulation(Test, update='chronological')

config_to_Json(Test)
