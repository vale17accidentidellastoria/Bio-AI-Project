from pylab import *

from inspyred.ec.emo import NSGA2
from inspyred.ec import terminators, variators, replacers, selectors
from inspyred.ec import EvolutionaryComputation

import inspyred_utils
import plot_utils

def run_nsga2(random, problem, display=False, num_vars=0, use_bounder=True,
        variator=None, **kwargs) :
    """ run NSGA2 on the given problem """
    
    #create dictionaries to store data about initial population, and lines
    initial_pop_storage = {}
 
    algorithm = NSGA2(random)
    algorithm.terminator = terminators.generation_termination 
    if variator is None :     
        algorithm.variator = [variators.blend_crossover,
                              variators.gaussian_mutation]
    else :
        algorithm.variator = variator
    
    kwargs["num_selected"]=kwargs["pop_size"]  
    if use_bounder :
        kwargs["bounder"]=problem.bounder
    
    if display and problem.objectives == 2:
        algorithm.observer = [inspyred_utils.initial_pop_observer]
    else :
        algorithm.observer = inspyred_utils.initial_pop_observer
        
    final_pop = algorithm.evolve(evaluator=problem.evaluator,  
                          maximize=problem.maximize,
                          initial_pop_storage=initial_pop_storage,
                          num_vars=num_vars, 
                          generator=problem.generator,
                          **kwargs)         
    
    best_guy = final_pop[0].candidate[0:num_vars]
    best_fitness = final_pop[0].fitness
    #final_pop_fitnesses = asarray([guy.fitness for guy in algorithm.archive])
    #final_pop_candidates = asarray([guy.candidate[0:num_vars] for guy in algorithm.archive])
    final_pop_fitnesses = asarray([guy.fitness for guy in final_pop])
    final_pop_candidates = asarray([guy.candidate[0:num_vars] for guy in final_pop])

    if display :
        # Plot the parent and the offspring on the fitness landscape 
        # (only for 1D or 2D functions)
        if num_vars == 1 :
            plot_utils.plot_results_multi_objective_1D(problem, 
                                  initial_pop_storage["individuals"], 
                                  initial_pop_storage["fitnesses"], 
                                  final_pop_candidates, final_pop_fitnesses,
                                  'Initial Population', 'Final Population',
                                  len(final_pop_fitnesses[0]), kwargs)
    
        elif num_vars == 2 :
            plot_utils.plot_results_multi_objective_2D(problem, 
                                  initial_pop_storage["individuals"], 
                                  final_pop_candidates, 'Initial Population',
                                  'Final Population',
                                  len(final_pop_fitnesses[0]), kwargs)

        plot_utils.plot_results_multi_objective_PF(final_pop, kwargs['fig_title'] + ' (Pareto front)')

    return final_pop_candidates, final_pop_fitnesses

def run_ga(random,problem, display=False, num_vars=0, 
           maximize=False, use_bounder=True, **kwargs) :
    """ run a GA on the given problem """
    
    #create dictionaries to store data about initial population, and lines
    initial_pop_storage = {}
    
    algorithm = EvolutionaryComputation(random)
    algorithm.terminator = terminators.generation_termination
    algorithm.replacer = replacers.generational_replacement    
    algorithm.variator = [variators.uniform_crossover, 
                          variators.gaussian_mutation]
    algorithm.selector = selectors.tournament_selection
    if display and problem.objectives == 2:
        algorithm.observer = [plot_utils.plot_observer, inspyred_utils.initial_pop_observer]
    else :
        algorithm.observer = inspyred_utils.initial_pop_observer
    
    kwargs["num_selected"]=kwargs["pop_size"]  
    if use_bounder :
        kwargs["bounder"]=problem.bounder
    if "pop_init_range" in kwargs :
        kwargs["generator"]=inspyred_utils.generator
    else :
        kwargs["generator"]=problem.generator
    
    kwargs["problem"] = problem
    final_pop = algorithm.evolve(evaluator=inspyred_utils.single_objective_evaluator,
                                 maximize=problem.maximize,
                                 initial_pop_storage=initial_pop_storage,
                                 num_vars=num_vars, 
                                 **kwargs)                          

    best_guy = final_pop[0].candidate
    best_fitness = final_pop[0].fitness.fitness
    final_pop_fitnesses = asarray([guy.fitness for guy in final_pop])
    final_pop_candidates = asarray([guy.candidate for guy in final_pop])
    
    if display :
        # Plot the parent and the offspring on the fitness landscape 
        # (only for 1D or 2D functions)
        if num_vars == 1 :
            plot_utils.plot_results_multi_objective_1D(problem, 
                                  initial_pop_storage["individuals"], 
                                  initial_pop_storage["fitnesses"], 
                                  final_pop_candidates, final_pop_fitnesses,
                                  'Initial Population', 'Final Population',
                                  len(final_pop_fitnesses[0]), kwargs)
    
        elif num_vars == 2 :
            plot_utils.plot_results_multi_objective_2D(problem, 
                                  initial_pop_storage["individuals"], 
                                  final_pop_candidates, 'Initial Population',
                                  'Final Population',
                                  len(final_pop_fitnesses[0]), kwargs)
   
    return best_guy, best_fitness
