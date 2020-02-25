import Actor as Actor
import System as System

England = Actor.Actor('England', 0, -1)
Spain = Actor.Actor('Spain', 1, -1)
France = Actor.Actor('France', 2, -1)

Start = System.System([1, 1, 1])
France.make_tree(Start)
England.make_tree(Start)

print(England.tree)

print('done')
