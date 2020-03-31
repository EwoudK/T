import cProfile

from StartingValues import Start
from Loose import write_evolution


def Simulation(start):
    local_optimum_counter = 0
    counter = 0

    while local_optimum_counter < 10:

        new = start.copy()
        for actor in start.actors:
            print(actor)
            if local_optimum_counter < 1:
                actor.construct_tree(start, counter)
            else:
                actor.decide(start, new)

        if new == start:
            local_optimum_counter += 1
        else:
            local_optimum_counter = 0

        new.parent = start
        start.children = new

        start = new
        print(counter, start)

        counter += 1

        if counter == 20:
            local_optimum_counter = 11
            print('unstable system')

    print('stable configuration found')
    write_evolution(start)
    return start


New = Simulation(Start)
