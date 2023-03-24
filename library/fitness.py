import abc
import math

from library.individual import Individual


class FitnessFunction(abc.ABC):
    @abc.abstractmethod
    def score(self, individual: Individual) -> float:
        pass


@FitnessFunction.register
class ConstFitnessFunction(FitnessFunction):
    def score(self, _: Individual):
        return 100


@FitnessFunction.register
class FHDFitnessFunction(FitnessFunction):
    def score(self, individual: Individual):
        delta = 100
        l = individual.genotype.chromosome.__len__()
        k = individual.genotype.chromosome.count("0")
        return (l - k) + k * delta


@FitnessFunction.register
class QuadraticFitnessFunction(FitnessFunction):
    def score(self, individual: Individual):
        x = individual.phenotype.value
        return math.pow(x, 2)


@FitnessFunction.register
class ExponentialFitnessFunction(FitnessFunction):
    def __init__(self, c: float):
        super().__init__()
        self.c = c

    def score(self, individual: Individual):
        x = individual.phenotype.value
        return math.exp(self.c * x)
