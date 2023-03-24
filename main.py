from operator import itemgetter

from library.individual import BinaryGenotypeFactory, BinaryPhenotypeFactory, IndividualFactory, NumericalGenotypeFactory, NumericalPhenotypeFactory
from library.fitness import Constant100FitnessFunction, FHDFitnessFunction, ExponentialFitnessFunction
from library.population import Population
from library.selection import Selection, RWS, SUS
from library.operator import Crossover, DenseMutation, Mutation, OnePointCrossover


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
            print(f"Head individuals: {self.population.head()}")
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


def report(config, runs=1):
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


def main():
    individual_factory = IndividualFactory(genotype_factory=BinaryGenotypeFactory(length=10),
                                           phenotype_factory=BinaryPhenotypeFactory())
    report({
        "population_size": 100,
        "individual_factory": individual_factory,
        "selection": RWS(0.9801, FHDFitnessFunction()),
        "crossover": OnePointCrossover(individual_factory),
        "mutation": DenseMutation()
    })


if __name__ == "__main__":
    main()
