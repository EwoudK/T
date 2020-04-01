import cProfile
from StartingValues import Start
from Loose import write_evolution


def Simulation(start):
    local_optimum_counter = 0
    counter = 0
    unstable = False

    while local_optimum_counter < 10:

        new = start.copy()
        for actor in start.actors:
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

        counter += 1

        if counter == 50:
            local_optimum_counter = 11
            print('unstable system')
            unstable = True

    if not unstable:
        print('stable configuration found')
    write_evolution(start)
    return start


New = Simulation(Start)

