import abc
import random

from library.individual import Genotype, Individual, Phenotype


class Crossover(abc.ABC):
    @abc.abstractmethod
    def next_generation(self, individuals: list[Individual]) -> list[Individual]:
        pass


@Crossover.register
class OnePointCrossover(Crossover):
    def next_generation(self, individuals: list[Individual]):
        next_individuals = []

        individuals = individuals.copy()

        def pop_individual():
            index = random.randrange(0, len(individuals))
            return individuals.pop(index)

        while len(individuals) > 0:
            parent1 = pop_individual()
            parent2 = pop_individual()

            child1, child2 = self._birth(parent1, parent2)

            next_individuals.append(child1)
            next_individuals.append(child2)

        return next_individuals

    def _birth(self, parent1: Individual, parent2: Individual):
        chromosome1 = parent1.genotype.chromosome
        chromosome2 = parent2.genotype.chromosome

        crossover_point = int(random.random() * len(chromosome1))

        child1 = Individual(genotype=Genotype(chromosome1[:crossover_point] + chromosome2[crossover_point:]),
                            phenotype=Phenotype(0))
        child2 = Individual(genotype=Genotype(chromosome2[:crossover_point] + chromosome1[crossover_point:]),
                            phenotype=Phenotype(0))

        return [child1, child2]


class MutationTable:
    def __init__(self):
        f = [0.0005, 0.00001]

        self.l = [10, 100]
        self.n = [10, 100, 200, 300, 400, 500, 1000]

        self.table = [[0.] * len(self.n) for _ in range(len(self.l))]
        for l_index, _ in enumerate(self.l):
            for n_index, n_value in enumerate(self.n):
                self.table[l_index][n_index] = f[l_index] / (n_value / 100)

    def rate(self, l: int, n: int):
        l_index = self.l.index(l)
        n_index = self.n.index(n)
        return self.table[l_index][n_index]

    def __repr__(self):
        return '\n'.join([''.join(str(col) for col in row) for row in self.table])


class Mutation(abc.ABC):
    def __init__(self):
        self.mutation_table = MutationTable()

    @abc.abstractmethod
    def next_generation(self, individuals: list[Individual]) -> list[Individual]:
        pass


@Mutation.register
class DenseMutation(Mutation):
    def next_generation(self, individuals: list[Individual]):
        individuals = individuals.copy()

        n = len(individuals)
        l = len(individuals[0].genotype.chromosome)

        mutation_rate = self.mutation_table.rate(l, n)

        for individual in individuals:
            for locus, _ in enumerate(individual.genotype.chromosome):
                active_mutation = (random.random() <= mutation_rate)
                if active_mutation:
                    individual.genotype.mutate(locus)

        return individuals
