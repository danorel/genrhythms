from operator import itemgetter

from library.individual import BinaryGenotypeFactory, BinaryPhenotypeFactory, IndividualFactory, NumericalGenotypeFactory, NumericalPhenotypeFactory
from library.fitness import Constant100FitnessFunction, FHDFitnessFunction, ExponentialFitnessFunction, QuadraticFitnessFunction
from library.population import Population
from library.selection import Selection, RWS, SUS
from library.operator import Crossover, DenseMutation, Mutation, OnePointCrossover
from library.codec import BinaryCodec, GrayCodec


class GeneticAlgorithm:
    def __init__(self,
                 population: Population,
                 selection: Selection,
                 crossover: Crossover or None,
                 mutation: Mutation or None):
        self.population = population
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation

    def has_solution(self, verbose=False):
        iteration = 0
        while not self._stop_criteria(iteration):
            self.population.evolve(selection=self.selection,
                                   crossover=self.crossover,
                                   mutation=self.mutation)
            if verbose:
                if iteration % 10 == 0:
                    print(f"Iteration {iteration} has finished!")
            iteration += 1
        return self._check_for_solution(verbose)

    def _check_for_solution(self, verbose=False):
        if verbose:
            print(f"Head individuals: {self.population.head(N=1)}")
        if self.mutation is not None:
            return self.population.is_optimal(percentage=90)
        else:
            return self.population.is_optimal(percentage=100)

    def _stop_criteria(self, iteration):
        if self.mutation is not None:
            if iteration == 10000001 or self.population.is_homogeneous():
                return True
        else:
            if iteration == 10000001 or self.population.is_identical():
                return True
        return False


def report(config, runs=100):
    population_size, individual_factory, *rest_config = itemgetter(
        "population_size",
        "individual_factory",
        "selection",
        "crossover",
        "mutation"
    )(config)

    random_individuals = individual_factory.random(population_size - 1)
    optimal_individuals = individual_factory.optimal(1)

    individuals = random_individuals + optimal_individuals
    optimal = optimal_individuals[0]

    success = 0
    for _ in range(runs):
        population = Population(individuals, optimal)
        if GeneticAlgorithm(population, *rest_config).has_solution(verbose=True):
            success += 1

    print(f"Success runs: {success} / {runs}")


def report_binary(only_target=False):
    individual_factory = IndividualFactory(genotype_factory=BinaryGenotypeFactory(length=100, codec=BinaryCodec()),
                                           phenotype_factory=BinaryPhenotypeFactory(codec=BinaryCodec()))

    if only_target:
        report({
            "population_size": 100,
            "individual_factory": individual_factory,
            "selection": RWS(0.9801, FHDFitnessFunction()),
            "crossover": None,
            "mutation": None
        })
    else:
        report({
            "population_size": 100,
            "individual_factory": individual_factory,
            "selection": RWS(0.9801, FHDFitnessFunction()),
            "crossover": None,
            "mutation": None
        })
        report({
            "population_size": 100,
            "individual_factory": individual_factory,
            "selection": RWS(0.9801, FHDFitnessFunction()),
            "crossover": OnePointCrossover(individual_factory),
            "mutation": None
        })
        report({
            "population_size": 100,
            "individual_factory": individual_factory,
            "selection": RWS(0.9801, FHDFitnessFunction()),
            "crossover": None,
            "mutation": DenseMutation()
        })
        report({
            "population_size": 100,
            "individual_factory": individual_factory,
            "selection": RWS(0.9801, FHDFitnessFunction()),
            "crossover": OnePointCrossover(individual_factory),
            "mutation": DenseMutation()
        })


def report_numerical(only_target=False):
    individual_factory = IndividualFactory(genotype_factory=NumericalGenotypeFactory(length=10, codec=GrayCodec()),
                                           phenotype_factory=NumericalPhenotypeFactory(codec=GrayCodec()))

    if only_target:
        report({
            "population_size": 100,
            "individual_factory": individual_factory,
            "selection": RWS(0.9801, ExponentialFitnessFunction(c=1)),
            "crossover": OnePointCrossover(individual_factory),
            "mutation": DenseMutation()
        })
    else:
        report({
            "population_size": 100,
            "individual_factory": individual_factory,
            "selection": RWS(0.9801, ExponentialFitnessFunction(c=1)),
            "crossover": None,
            "mutation": None
        })
        report({
            "population_size": 100,
            "individual_factory": individual_factory,
            "selection": RWS(0.9801, ExponentialFitnessFunction(c=1)),
            "crossover": OnePointCrossover(individual_factory),
            "mutation": DenseMutation()
        })


def main(target="both", only_target=False):
    if target == "binary":
        report_binary(only_target)
    elif target == "numerical":
        report_numerical(only_target)
    else:
        report_binary(only_target)
        report_numerical(only_target)


if __name__ == "__main__":
    main(target="numerical", only_target=True)
