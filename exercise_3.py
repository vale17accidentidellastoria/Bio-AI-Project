# -*- coding: utf-8 -*-

from pylab import *

from inspyred import benchmarks
from inspyred.ec import variators
from inspyred_utils import NumpyRandomWrapper
from sustainability_problem import DiskClutchBrake, sust_indexes_mutations

import multi_objective

import sys

from functools import reduce

""" 
-------------------------------------------------------------------------
Edit this part to do the exercises

"""

display = True

# parameters for NSGA-2
args = {}
args["pop_size"] = 100
args["max_generations"] = 10
constrained = True

"""
-------------------------------------------------------------------------
"""

problem = DiskClutchBrake(constrained)
if constrained :
    args["constraint_function"] = problem.constraint_function
args["objective_1"] = "Sustainability"
args["objective_2"] = "Price"

args["variator"] = [variators.blend_crossover,sust_indexes_mutations]

args["fig_title"] = 'NSGA-2'

if __name__ == "__main__" :
    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(123))
    else :
        rng = NumpyRandomWrapper()
    
    final_pop, final_pop_fitnesses = multi_objective.run_nsga2(rng, problem, display=display, 
                                         num_vars=4, **args)
    
    print("Final Population\n", final_pop)
    print()
    print("Final Population Fitnesses\n", final_pop_fitnesses)
    
    output = open("exercise_3.csv", "w")
    for individual, fitness in zip(final_pop, final_pop_fitnesses) :
        output.write(reduce(lambda x,y : str(x) + "," + str(y), 
                            individual))
        output.write(",")
        output.write(reduce(lambda x,y : str(x) + "," + str(y), 
                            fitness))
        output.write("\n")
    output.close()
    
    ioff()
    show()
