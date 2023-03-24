import abc
import random


class Genotype:
    def __init__(self, chromosome: str):
        self.chromosome = chromosome

    def mutate(self, locus: int):
        mutation_gene = "0" if self.chromosome[locus] == "1" else "1"
        self.chromosome = self.chromosome[:locus] + \
            mutation_gene + self.chromosome[locus + 1:]

    def __repr__(self):
        return f"({self.chromosome})"


class GenotypeFactory(abc.ABC):
    def __init__(self, length):
        self.length = length

    @abc.abstractmethod
    def sample(self, chromosome: str) -> Genotype:
        pass

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

    def sample(self, chromosome: str):
        return Genotype(chromosome)

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

    def sample(self, chromosome: str):
        return Genotype(chromosome)

    def random(self):
        chromosome = "".join(
            ["1" if random.random() > 0.5 else "0" for _ in range(self.length)])
        return Genotype(chromosome)

    def optimal(self):
        chromosome = "1" * self.length
        return Genotype(chromosome)


class Phenotype:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"({self.value})"


class PhenotypeFactory(abc.ABC):
    @abc.abstractmethod
    def sample(self, genotype: Genotype) -> Phenotype:
        pass


class BinaryPhenotypeFactory(PhenotypeFactory):
    def sample(self, genotype: Genotype):
        l = genotype.chromosome.__len__()
        k = genotype.chromosome.count("0")
        return Phenotype(value=(l, k))


class NumericalPhenotypeFactory(PhenotypeFactory):
    def sample(self, genotype: Genotype):
        decimal = int(genotype.chromosome, 2)
        value = decimal / 100
        return Phenotype(value)


class Individual:
    def __init__(self, genotype: Genotype, phenotype: Phenotype):
        self.genotype = genotype
        self.phenotype = phenotype

    def __repr__(self):
        return f"{self.genotype} -> {self.phenotype}"


class IndividualFactory:
    def __init__(self,
                 genotype_factory: GenotypeFactory,
                 phenotype_factory: PhenotypeFactory):
        self.genotype_factory = genotype_factory
        self.phenotype_factory = phenotype_factory

    def instance(self, chromosome: str):
        genotype = self.genotype_factory.sample(chromosome)
        phenotype = self.phenotype_factory.sample(genotype)
        return Individual(genotype, phenotype)

    def random(self, N: int):
        return [self._random_individual() for _ in range(N)]

    def _random_individual(self):
        genotype = self.genotype_factory.random()
        phenotype = self.phenotype_factory.sample(genotype)
        return Individual(genotype, phenotype)

    def optimal(self, N: int):
        return [self._optimal_individual() for _ in range(N)]

    def _optimal_individual(self):
        genotype = self.genotype_factory.optimal()
        phenotype = self.phenotype_factory.sample(genotype)
        return Individual(genotype, phenotype)
