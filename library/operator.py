import abc

from library.individual import Individual


class Crossover(abc.ABC):
    @abc.abstractmethod
    def next_generation(self, individuals: list[Individual]) -> list[Individual]:
        pass


@Crossover.register
class SinglePointCrossover(Crossover):
    def next_generation(self, individuals: list[Individual]):
        return individuals


class Mutation(abc.ABC):
    @abc.abstractmethod
    def next_generation(self, individuals: list[Individual]) -> list[Individual]:
        pass


@Mutation.register
class DenseMutation(Mutation):
    def next_generation(self, individuals: list[Individual]):
        return individuals
