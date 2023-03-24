import abc
import random

from library.individual import Individual, IndividualFactory


class Crossover(abc.ABC):
    def __init__(self, individual_factory: IndividualFactory) -> None:
        self.individual_factory = individual_factory

    @abc.abstractmethod
    def next_generation(self, individuals: list[Individual]) -> list[Individual]:
        pass


@Crossover.register
class OnePointCrossover(Crossover):
    def next_generation(self, prev_individuals: list[Individual]):
        next_individuals = []

        individuals = prev_individuals.copy()

        def pop_individual():
            index = random.randrange(0, len(individuals))
            return individuals.pop(index)

        while len(individuals) > 0:
            parent1 = pop_individual()
            parent2 = pop_individual()

            chromosome1 = parent1.genotype.chromosome
            chromosome2 = parent2.genotype.chromosome

            crossover_point = int(random.random() * len(chromosome1))

            child1 = self.individual_factory.instance(
                chromosome1[:crossover_point] + chromosome2[crossover_point:])
            child2 = self.individual_factory.instance(
                chromosome2[:crossover_point] + chromosome1[crossover_point:])

            next_individuals.append(child1)
            next_individuals.append(child2)

        assert(len(prev_individuals) == len(next_individuals))

        return next_individuals


class MutationTable:
    def __init__(self):
        f = [0.0005, 0.00001]

        self.l = [10, 100]
        self.n = [100, 200, 300, 400, 500, 1000]

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
    def next_generation(self, prev_individuals: list[Individual]):
        next_individuals = prev_individuals.copy()

        n = len(next_individuals)
        l = len(next_individuals[0].genotype.chromosome)

        mutation_rate = self.mutation_table.rate(l, n)

        for individual in next_individuals:
            for locus, _ in enumerate(individual.genotype.chromosome):
                active_mutation = (random.random() <= mutation_rate)
                if active_mutation:
                    individual.genotype.mutate(locus)

        assert(len(prev_individuals) == len(next_individuals))

        return next_individuals
