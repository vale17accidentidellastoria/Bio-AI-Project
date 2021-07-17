from inspyred import benchmarks 
from inspyred.ec.emo import Pareto
from inspyred.ec.variators import mutator
from pylab import *
import copy



# possible values

        # c[0] prezzo          c[1] production          c[2] workers         c[3] transportation
values = [arange(0.5, 5, .3), arange(0.5, 9, 0.1), arange(0.5, 9, 0.1), arange(0.5, 9, 0.1)]


class DiskClutchBounder(object):
    def __call__(self, candidate, args):
        closest = lambda target, index: min(values[index],
                                            key=lambda x: abs(x - target))

        for i, c in enumerate(candidate):
            print("before:", candidate[i])
            candidate[i] = closest(c, i)
            print("after:", candidate[i])
        return candidate


class ConstrainedPareto(Pareto):
    def __init__(self, values=None, violations=None, ec_maximize=False):
        Pareto.__init__(self, values, maximize=[False, True, True, True])
        self.violations = violations
        self.ec_maximize = ec_maximize

    def __lt__(self, other):
        if self.violations is None:
            return Pareto.__lt__(self, other)
        elif len(self.values) != len(other.values):
            raise NotImplementedError
        else:
            if self.violations > other.violations:
                # if self has more violations than other
                # return true if EC is maximizing otherwise false
                return (self.ec_maximize)
            elif other.violations > self.violations:
                # if other has more violations than self
                # return true if EC is minimizing otherwise false
                return (not self.ec_maximize)
            elif self.violations > 0:
                # if both equally infeasible (> 0) than cannot compare
                return False
            else:
                # only consider regular dominance if both are feasible
                not_worse = True
                strictly_better = False
                for x, y, m in zip(self.values, other.values, self.maximize):
                    if m:
                        if x > y:
                            not_worse = False
                        elif y > x:
                            strictly_better = True
                    else:
                        if x < y:
                            not_worse = False
                        elif y < x:
                            strictly_better = True
            return not_worse and strictly_better


class DiskClutchBrake(benchmarks.Benchmark):

    def __init__(self, constrained=False):
        benchmarks.Benchmark.__init__(self, 4, 2)
        self.bounder = DiskClutchBounder()
        self.maximize = True
        self.constrained = constrained

    def generator(self, random, args):
        return [random.sample(values[i], 1)[0] for i in range(self.dimensions)]

    def evaluator(self, candidates, args):
        fitness = []
        for c in candidates:

            f2 = 0.5 * c[1]+ 0.35 * c[2] + 0.15 * c[3] 

            f1 = c[0]

            fitness.append(ConstrainedPareto([f1, f2],
                                             self.constraint_function(c),
                                             self.maximize))

        return fitness

        


    def constraint_function(self,candidate):
        if not self.constrained :
            return 0
        """Return the magnitude of constraint violations."""

        violations = 0
        f = 0.5*candidate[1] + 0.35*candidate[2] + 0.15*candidate[3]

        if f > 0 and f <=1:
            if candidate[0] <= 1: 
                violations = violations
            
            if candidate[0] > 1.1:
                violations = candidate[0] - 1.1 
        
        if f > 1 and f <=2 : 
            if candidate[0] >= 2: 
                violations = candidate[0] - 2
        
        if f > 2 and f <= 3: 

            if candidate[0] >= 3 :
                violations = candidate[0] - 3
            
            if candidate[0] <= 2: 
                violations =  2 - candidate[0]
        
        if f > 3 and f <=4:
            if candidate[0] <= 2.5: 
                violations = 2.5 - candidate[0]

    
            if candidate[0] >= 3.5: 
                violations = candidate[0] - 2.5


        if f > 4 and f <= 5: 
            if candidate[0] <= 3 : 
                violations = 3 - candidate[0]  

        if f > 5 and f <=6: 
            if candidate[0] <= 3.5: 
                violations = 3.5 - candidate[0]            
            
        if f > 6 and f <= 7: 
            if candidate[0] <= 4: 
                violations = 4 - candidate[0]

        if f > 7 and f <= 8: 
            if candidate[0] <= 4.5: 
                violations = 4.4 - candidate[0]

        if f > 8: 

            if candidate[0] <= 5 : 
                violations = 5 - candidate[0]


        return violations





@mutator
def sust_indexes_mutations(random, candidate, args):
    mut_rate = args.setdefault('mutation_rate', 0.1)
    bounder = args['_ec'].bounder
    mutant = copy.copy(candidate)
    for i, m in enumerate(mutant):
        if random.random() < mut_rate:
            mutant[i] += random.gauss(0, (values[i][-1] - values[i][0]) / 10.0)
    mutant = bounder(mutant, args)
    return mutant
