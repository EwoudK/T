# Thesis: Coalition theory

There are three visualisations for now. Evolution.html, PathIntegral.html, Tree.html.
    Evolution shows the evolution of the system from one configuration into a new one because of actors seeking to maximize their gain.
    Tree shows the rationality tree that is built for every actor in a certain step. The tree is built as follows:
        - actor for whom the tree is built can choose to stay in current configuration or flip its spin.
        - all the other actors flip their spin.
        - the configuration where the all other actors do not flip their spin is added as well.
    This gives 2*[(N-1) + 1] new configurations per rationality tree node.
    Red is for -1, Blue is for +1.
    The gain is calculated with the hamiltonian and propensities that can be found inside the file System.py
    For the propensities a symmetric matrix is built with the diagonal elements zero (no self interactions).
    
   Tree is able to show the rationality tree for every country for every step in the simulation by use of the selection menu.
    
   PathIntegral shows the decision process every actor makes to decide which path to take.
   Every actor wants to end in a configuration that maximizes its personal gain but also maximize its path to this configuration.
   
One caveat, the current code does not detect unstable systems and will loop forever.
This is not a hard fix but still needs to be implemented either way.