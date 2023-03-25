import abc
import math

from library.individual import Individual


class FitnessFunction(abc.ABC):
    @abc.abstractmethod
    def score(self, individual: Individual) -> float:
        pass


@FitnessFunction.register
class Constant100FitnessFunction(FitnessFunction):
    def score(self, _: Individual):
        return 100


@FitnessFunction.register
class FHDFitnessFunction(FitnessFunction):
    def score(self, individual: Individual):
        delta = 100
        l, k = individual.phenotype.value
        return (l - k) + k * delta


@FitnessFunction.register
class QuadraticFitnessFunction(FitnessFunction):
    def score(self, individual: Individual):
        x = individual.phenotype.value
        return math.pow(x, 2)


@FitnessFunction.register
class ConstantMinusQuadraticFitnessFunction(FitnessFunction):
    def score(self, individual: Individual):
        x = individual.phenotype.value
        return math.pow(5.12, 2) - math.pow(x, 2)


@FitnessFunction.register
class ConstantQuadraticFitnessFunction(FitnessFunction):
    def score(self, _: Individual):
        return math.pow(5.12, 2)


@FitnessFunction.register
class CExponentialFitnessFunction(FitnessFunction):
    def __init__(self, c: float):
        super().__init__()
        self.c = c

    def score(self, individual: Individual):
        x = individual.phenotype.value
        return math.exp(self.c * x)


@CExponentialFitnessFunction.register
class QuarterExponentialFitnessFunction(CExponentialFitnessFunction):
    def __init__(self):
        super().__init__(0.25)


@CExponentialFitnessFunction.register
class TwiceExponentialFitnessFunction(CExponentialFitnessFunction):
    def __init__(self):
        super().__init__(2)


@CExponentialFitnessFunction.register
class ExponentialFitnessFunction(CExponentialFitnessFunction):
    def __init__(self):
        super().__init__(1)
