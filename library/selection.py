import abc
import functools

from library.individual import Individual
from library.fitness import FitnessFunction


class Rank:
    def __init__(self, c, fitness_function: FitnessFunction):
        if c <= 0 or c >= 1:
            raise ValueError(f"c should belong (0, 1), recieved: {c}")
        self.c = c
        self.fitness_function = fitness_function

    def match_with_probabilities(self, individuals: list[Individual]):
        individuals = self._sort(individuals)
        probabilities = self._assign_probabilities(individuals)
        return zip(individuals, probabilities)

    def _assign_probabilities(self, individuals: list[Individual]):
        size = len(individuals)
        return [self._assign_probability(size, rank) for rank in range(size)]

    def _assign_probability(self, size: int, rank: int) -> float:
        return ((self.c - 1) / (pow(self.c, size) - 1)) * pow(self.c, size - rank)

    def _sort(self, individuals: list[Individual]):
        return sorted(individuals.copy(), key=functools.cmp_to_key(self._compare))

    def _compare(self, individual1: Individual, individual2: Individual):
        if self.fitness_function.score(individual1) < self.fitness_function.score(individual2):
            return -1
        elif self.fitness_function.score(individual1) > self.fitness_function.score(individual2):
            return 1
        else:
            return 0


class Selection(abc.ABC):
    def __init__(self, c: float, fitness_function: FitnessFunction):
        self.rank = Rank(c, fitness_function)

    @abc.abstractmethod
    def next_generation(self, individuals: list[Individual]) -> list[Individual]:
        pass


@Selection.register
class RWS(Selection):
    def __init__(self, c: float, fitness_function: FitnessFunction):
        super().__init__(c, fitness_function)

    def next_generation(self, individuals: list[Individual]):
        individuals_with_probabilities = self.rank.match_with_probabilities(
            individuals)
        return []


@Selection.register
class SUS(Selection):
    def __init__(self, c: float, fitness_function: FitnessFunction):
        super().__init__(c, fitness_function)

    def next_generation(self, individuals: list[Individual]):
        individuals_with_probabilities = self.rank.match_with_probabilities(
            individuals)
        return []
