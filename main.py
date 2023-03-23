from operator import itemgetter

from library.individual import IndividualFactory, BinaryGenotypeFactory
from library.fitness import QuadraticFitnessFunction
from library.population import Population
from library.selection import SUS


class GeneticAlgorithm:
    def __init__(self,
                 population: Population,
                 crossover_probability: float = 1,
                 mutation_probability: float = 0):
        self.population = population
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

    def has_solution(self, verbose=True):
        iteration = 0
        while not self._converge(iteration):
            self.population.evolve()
            if verbose:
                if iteration % 1000 == 0:
                    print(f"Iteration {iteration} has finished!")
            iteration += 1
        return self._check_for_solution()

    def _check_for_solution(self):
        if self.mutation_probability:
            return self.population.is_optimal(percentage=90)
        else:
            return self.population.is_optimal(percentage=100)

    def _converge(self, iteration):
        if self.mutation_probability:
            if iteration == 10000000 or self.population.is_homogeneous():
                return True
        else:
            if iteration == 10000000 or self.population.is_identical():
                return True
        return False


def report(config, runs=100):
    population_size, genotype_factory, selection, *rest_config = itemgetter(
        "population_size",
        "genotype_factory",
        "selection",
        "crossover_probability",
        "mutation_probability"
    )(config)

    individual_factory = IndividualFactory(genotype_factory)

    random_individuals = individual_factory.random(population_size - 1)
    optimal_individuals = individual_factory.optimal(1)

    individuals = random_individuals + optimal_individuals
    optimal = optimal_individuals[0]

    success = 0
    for _ in range(runs):
        population = Population(individuals, optimal, selection)
        if GeneticAlgorithm(population, *rest_config).has_solution():
            success += 1

    print(f"Success runs: {success} / {runs}")


def main():
    report({
        "population_size": 100,
        "genotype_factory": BinaryGenotypeFactory(),
        "selection": SUS(0.9801, QuadraticFitnessFunction()),
        "crossover_probability": 1,
        "mutation_probability": 0
    })


if __name__ == "__main__":
    main()
