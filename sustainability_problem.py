from inspyred import benchmarks 
from inspyred.ec.emo import Pareto
from inspyred.ec.variators import mutator
from pylab import *
import copy

# parameters, see Deb 2006
Delta_R = 20  # mm
L_max = 30  # mm
delta = 0.5  # mm
p_max = 1  # MPa
V_sr_max = 10  # m/s
n = 250  # rpm
mu = 0.5
s = 1.5
M_s = 40  # Nm
omega = pi * n / 30.  # rad/s
rho = 0.0000078  # kg/mm^3
T_max = 15  # s
M_f = 3  # Nm
I_z = 55  # kg*m^2

# possible values
values = [arange(0, 10, 0.1), arange(0, 5, 0.5)]


class DiskClutchBounder(object):
    def __call__(self, candidate, args):
        closest = lambda target, index: min(values[index],
                                            key=lambda x: abs(x - target))

        for i, c in enumerate(candidate):
            candidate[i] = closest(c, i)
        return candidate


class ConstrainedPareto(Pareto):
    def __init__(self, values=None, violations=None, ec_maximize=False):
        Pareto.__init__(self, values, maximize=[True, False])
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
        benchmarks.Benchmark.__init__(self, 2, 2)
        self.bounder = DiskClutchBounder()
        self.maximize = True
        self.constrained = constrained

    def generator(self, random, args):
        print("GENERATOR")
        return [random.sample(values[i], 1)[0] for i in range(self.dimensions)]

    def evaluator(self, candidates, args):
        print("EVALUATOR")
        fitness = []
        for c in candidates:
            f1 = c[1]

            f2 = c[0]
            #ipotesi: come dicevamo con Asia, si potrebbe fare f2 = 0.15*c[1] + 0.35*c[2].... dove c[1], c[2], c[3] saranno i nostri 3 sotto indici (che naturalmente andranno definiti aumentando il numero di variables e aggiungengo i loro tre range in values

            fitness.append(ConstrainedPareto([f2, f1],
                                             self.constraint_function(c),
                                             self.maximize))

        return fitness

    def constraint_function(self, candidate):
        if not self.constrained:
            return 0
        """Return the magnitude of constraint violations."""
        A = pi * (candidate[1] ** 2 - candidate[0] ** 2)  # mm^2
        p_rz = candidate[3] / A  # N/mm^2
        R_sr = ((2. / 3.) * (candidate[1] ** 3 - candidate[0] ** 3) /
                (candidate[1] ** 2 - candidate[0] ** 2))  # mm
        V_sr = pi * R_sr * n / 30000.  # m/s

        M_h = ((2. / 3.) * mu * candidate[3] * candidate[4] *
               (candidate[1] ** 3 - candidate[0] ** 3) /
               (candidate[1] ** 2 - candidate[0] ** 2)) / 1000.  # N*m

        T = (I_z * omega) / (M_h + M_f)

        violations = 0
        # g_1
        if (candidate[1] - candidate[0] - Delta_R) < 0:
            violations -= (candidate[1] - candidate[0] - Delta_R)
            # g_2
        if (L_max - (candidate[4] + 1) * (candidate[2] + delta)) < 0:
            violations -= (L_max - (candidate[4] + 1) * (candidate[2] + delta))
        # g_3
        if (p_max - p_rz) < 0:
            violations -= (p_max - p_rz)
            # g_4
        if (p_max * V_sr_max - p_rz * V_sr) < 0:
            violations -= (p_max * V_sr_max - p_rz * V_sr)
        # g_5
        if (V_sr_max - V_sr) < 0:
            violations -= (V_sr_max - V_sr)
        # g_6
        if (M_h - s * M_s) < 0:
            violations -= (M_h - s * M_s)
            # g_7
        if (T < 0):
            violations -= T
        # g_8
        if (T_max - T) < 0:
            violations -= (T_max - T)

        return violations


@mutator
def disk_clutch_brake_mutation(random, candidate, args):
    mut_rate = args.setdefault('mutation_rate', 0.1)
    bounder = args['_ec'].bounder
    mutant = copy.copy(candidate)
    for i, m in enumerate(mutant):
        if random.random() < mut_rate:
            mutant[i] += random.gauss(0, (values[i][-1] - values[i][0]) / 10.0)
    mutant = bounder(mutant, args)
    return mutant
