from library.individual import Individual
from library.selection import Selection
from library.operator import Crossover, Mutation


class Population:
    def __init__(self,
                 individuals: list[Individual],
                 optimal: Individual):
        self.individuals = individuals
        self.optimal = optimal

    def evolve(self,
               selection: Selection,
               crossover: Crossover or None,
               mutation: Mutation or None):
        individuals = self.individuals.copy()
        individuals = selection.next_generation(individuals)
        if crossover is not None:
            individuals = crossover.next_generation(individuals)
        if mutation is not None:
            individuals = mutation.next_generation(individuals)
        self.individuals = individuals

    def is_optimal(self, percentage: float = 90.):
        total = len(self.individuals)
        optimal = len(list(filter(lambda individual: individual.genotype.chromosome ==
                                  self.optimal.genotype.chromosome, self.individuals)))
        return (optimal / total) * 100 >= percentage

    def is_identical(self, count: int = 1):
        unique = len(
            set(map(lambda individual: individual.genotype.chromosome, self.individuals)))
        return unique == count

    def is_homogeneous(self, percentage: float = 1.):
        total = len(self.individuals)
        unique = len(
            set(map(lambda individual: individual.genotype.chromosome, self.individuals)))
        return (unique / total) * 100 <= percentage
