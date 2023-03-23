import functools

from library.individual import Individual
from library.population import Population
from library.fitness import FitnessFunction


class Rank:
    def __init__(self, c, fitness_function: FitnessFunction):
        if c <= 0 or c >= 1:
            raise ValueError(f"c should belong (0, 1), recieved: {c}")
        self.c = c
        self.fitness_function = fitness_function

    def match(self, population: Population):
        individuals = self._sort(population.individuals)
        probabilities = [self._probability(
            len(individuals), rank) for rank in range(len(individuals))]
        return zip(individuals, probabilities)

    def _probability(self, size: int, rank: int) -> float:
        return ((self.c - 1) / (pow(self.c, size) - 1)) * (pow(self.c, size - rank))

    def _sort(self, individuals: list[Individual]):
        return sorted(individuals.copy(), key=functools.cmp_to_key(self._compare))

    def _compare(self, individual1: Individual, individual2: Individual):
        if self.fitness_function.score(individual1) < self.fitness_function.score(individual2):
            return -1
        elif self.fitness_function.score(individual1) > self.fitness_function.score(individual2):
            return 1
        else:
            return 0


class RWS:
    def __init__(self):
        pass


class SUS:
    def __init__(self):
        pass
