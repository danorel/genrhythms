from operator import itemgetter

from library.individual import IndividualFactory, BinaryGenotypeFactory
from library.fitness import FHDFitnessFunction
from library.population import Population
from library.selection import Selection, RWS, SUS
from library.operator import Crossover, Mutation


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

    def has_solution(self, verbose=True):
        iteration = 0
        while not self._converge(iteration):
            self.population.evolve(selection=self.selection,
                                   crossover=self.crossover,
                                   mutation=self.mutation)
            if verbose:
                if iteration % 5 == 0:
                    print(f"Iteration {iteration} has finished!")
            iteration += 1
        return self._check_for_solution()

    def _check_for_solution(self):
        if self.mutation is not None:
            return self.population.is_optimal(percentage=90)
        else:
            return self.population.is_optimal(percentage=100)

    def _converge(self, iteration):
        if self.mutation is not None:
            if iteration == 11 or self.population.is_homogeneous():
                return True
        else:
            if iteration == 11 or self.population.is_identical():
                return True
        return False


def report(config, runs=1):
    population_size, genotype_factory, *rest_config = itemgetter(
        "population_size",
        "genotype_factory",
        "selection",
        "crossover",
        "mutation"
    )(config)

    individual_factory = IndividualFactory(genotype_factory)

    random_individuals = individual_factory.random(population_size - 1)
    optimal_individuals = individual_factory.optimal(1)

    individuals = random_individuals + optimal_individuals
    optimal = optimal_individuals[0]

    success = 0
    for _ in range(runs):
        population = Population(individuals, optimal)
        if GeneticAlgorithm(population, *rest_config).has_solution():
            success += 1

    print(f"Success runs: {success} / {runs}")


def main():
    report({
        "population_size": 10,
        "genotype_factory": BinaryGenotypeFactory(length=10),
        "selection": SUS(0.9801, FHDFitnessFunction()),
        "crossover": None,
        "mutation": None
    })


if __name__ == "__main__":
    main()
