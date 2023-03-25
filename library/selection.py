import abc
import functools
import random

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
        return [self._assign_probability(size, rank) for rank in range(1, size + 1)]

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
    def __init__(self, fitness_function: FitnessFunction):
        self.rank = Rank(0.9801, fitness_function)

    @abc.abstractmethod
    def next_generation(self, individuals: list[Individual]) -> list[Individual]:
        pass


@Selection.register
class RWS(Selection):
    def __init__(self, fitness_function: FitnessFunction):
        super().__init__(fitness_function)

    def next_generation(self, individuals: list[Individual]):
        next_individuals = []

        wheel = dict()
        spins = len(individuals)
        segment = 0

        for individual, probability in self.rank.match_with_probabilities(individuals):
            segment_from, segment_to = segment, segment + probability
            wheel[(segment_from, segment_to)] = individual
            segment += probability

        for _ in range(spins):
            segment_point = random.random()
            for (segment_from, segment_to), individual in wheel.items():
                if segment_point >= segment_from and segment_point <= segment_to:
                    next_individuals.append(individual)
                    break

        assert len(next_individuals) == spins

        return next_individuals


@Selection.register
class SUS(Selection):
    def __init__(self, fitness_function: FitnessFunction):
        super().__init__(fitness_function)

    def next_generation(self, individuals: list[Individual]):
        next_individuals = []

        wheel = dict()
        segment = 0

        for individual, probability in self.rank.match_with_probabilities(individuals):
            segment_from, segment_to = segment, segment + probability
            wheel[(segment_from, segment_to)] = individual
            segment += probability

        arrows = len(individuals)
        arrow_step = 1 / arrows
        arrow_countdown = random.random()

        for arrow_index in range(arrows):
            segment_point = arrow_countdown + arrow_index * arrow_step
            if segment_point > 1:
                segment_point -= 1
            for (segment_from, segment_to), individual in wheel.items():
                if segment_point >= segment_from and segment_point <= segment_to:
                    next_individuals.append(individual)
                    break

        assert len(next_individuals) == arrows

        return next_individuals
