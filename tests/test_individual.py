import pytest

from library.individual import BinaryGenotypeFactory, NumericalGenotypeFactory


@pytest.mark.parametrize("length,optimal_chromosome", [
    (2, "00"),
    (5, "00000")
])
def test_BinaryGenotypeFactory_optimal(length, optimal_chromosome):
    genotype_factory = BinaryGenotypeFactory(length)
    genotype_optimal = genotype_factory.optimal()
    assert len(genotype_optimal.chromosome) == length
    assert genotype_optimal.chromosome == optimal_chromosome


@pytest.mark.parametrize("length", [
    (50),
    (100),
    (1000)
])
def test_BinaryGenotypeFactory_random(length):
    genotype_factory = BinaryGenotypeFactory(length)
    genotype_random = genotype_factory.random()
    assert len(genotype_random.chromosome) == length
    assert genotype_random.chromosome.count("0") != 0
    assert genotype_random.chromosome.count("1") != 0


@pytest.mark.parametrize("length,optimal_chromosome", [
    (2, "11"),
    (5, "11111")
])
def test_NumericalGenotypeFactory_optimal(length, optimal_chromosome):
    genotype_factory = NumericalGenotypeFactory(length)
    genotype_optimal = genotype_factory.optimal()
    assert len(genotype_optimal.chromosome) == length
    assert genotype_optimal.chromosome == optimal_chromosome


@pytest.mark.parametrize("length", [
    (50),
    (100),
    (1000)
])
def test_NumericalGenotypeFactory_random(length):
    genotype_factory = NumericalGenotypeFactory(length)
    genotype_random = genotype_factory.random()
    assert len(genotype_random.chromosome) == length
    assert genotype_random.chromosome.count("0") != 0
    assert genotype_random.chromosome.count("1") != 0
