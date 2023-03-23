from library.fitness import FitnessFunction
from library.individual import Individual
from library.selection import Rank


class Population:
    def __init__(self,
                 individuals: list[Individual],
                 fitness_function: FitnessFunction):
        self.individuals = individuals
        self.rank = Rank(0.9801, fitness_function)

    def evolve(self):
        individuals_probabilities = self.rank.match(self)
        return None

    def is_identical(self):
        unique = self.__unique__()
        return unique == 1

    def is_homogeneous(self, diversity: float = .01):
        total = self.individuals.__len__()
        unique = self.__unique__()
        return unique / total <= diversity

    def __unique__(self):
        chromosomes = set(
            map(lambda individual: individual.genotype.chromosome, self.individuals))
        return len(chromosomes)
