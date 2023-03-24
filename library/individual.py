import abc
import random


class Phenotype:
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"({self.value})"


class Genotype:
    def __init__(self, chromosome: str):
        self.chromosome = chromosome

    def mutate(self, locus: int):
        mutation_gene = "0" if self.chromosome[locus] == "1" else "1"
        self.chromosome = self.chromosome[:locus] + \
            mutation_gene + self.chromosome[locus + 1:]

    def __repr__(self):
        return f"({self.chromosome})"


class Individual:
    def __init__(self, genotype: Genotype, phenotype: Phenotype):
        self.genotype = genotype
        self.phenotype = phenotype

    def __repr__(self):
        return f"{self.genotype} -> {self.phenotype}"


class GenotypeFactory(abc.ABC):
    def __init__(self, length):
        self.length = length

    @abc.abstractmethod
    def random(self) -> Genotype:
        pass

    @abc.abstractmethod
    def optimal(self) -> Genotype:
        pass


@GenotypeFactory.register
class BinaryGenotypeFactory(GenotypeFactory):
    def __init__(self, length=100):
        super().__init__(length)

    def random(self):
        chromosome = "".join(
            ["1" if random.random() > 0.5 else "0" for _ in range(self.length)])
        return Genotype(chromosome)

    def optimal(self):
        chromosome = "0" * self.length
        return Genotype(chromosome)


@GenotypeFactory.register
class NumericalGenotypeFactory(GenotypeFactory):
    def __init__(self, length=10):
        super().__init__(length)

    def random(self):
        chromosome = "".join(
            ["1" if random.random() > 0.5 else "0" for _ in range(self.length)])
        return Genotype(chromosome)

    def optimal(self):
        chromosome = "1" * self.length
        return Genotype(chromosome)


class IndividualFactory:
    def __init__(self, genotype_factory: GenotypeFactory):
        self.genotype_factory = genotype_factory

    def random(self, N: int):
        return [Individual(genotype=self.genotype_factory.random(),
                           phenotype=Phenotype(i)) for i in range(N)]

    def optimal(self, N: int):
        return [Individual(genotype=self.genotype_factory.optimal(),
                           phenotype=Phenotype(i)) for i in range(N)]
