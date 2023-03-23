from library.individual import Individual
from library.selection import Selection


class Population:
    def __init__(self,
                 individuals: list[Individual],
                 optimal: Individual,
                 selection: Selection):
        self.individuals = individuals
        self.optimal = optimal
        self.selection = selection

    def evolve(self):
        prev_individuals = self.individuals
        next_individuals = self.selection.next_generation(prev_individuals)
        return None

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
