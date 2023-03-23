from operator import attrgetter

from library.individual import IndividualFactory, NumericalGenotypeFactory, BinaryGenotypeFactory
from library.fitness import QuadraticFitnessFunction
from library.population import Population


class GeneticAlgorithm:
    def __init__(self,
                 population: Population,
                 crossover_probability: float = 1,
                 mutation_probability: float = 0):
        self.population = population
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

    def run(self):
        iteration = 0
        while not self._converge_(iteration):
            self.population.evolve()
        return self._is_solution_()

    def _is_solution_(self):
        if self.mutation_probability:
            return self.population.is_homogeneous(diversity=.1) and self.population.is_optimal()
        else:
            return self.population.is_identical() and self.population.is_optimal()

    def _converge_(self, iteration):
        if self.mutation_probability:
            if iteration == 10000000 or self.population.is_homogeneous():
                return True
        else:
            if iteration == 10000000 or self.population.is_identical():
                return True
        return False


def report(config, runs=100):
    population_size, genotype_factory, fitness_function, *rest_config = attrgetter(
        "population_size",
        "genotype_factory",
        "fitness_function",
        "crossover_probability",
        "mutation_probability"
    )(config)

    individuals = IndividualFactory(genotype_factory).generate(population_size)
    population = Population(individuals, fitness_function)

    success = 0
    for _ in range(runs):
        if GeneticAlgorithm(population, *rest_config).run():
            success += 1

    print(f"Success runs: {success} / {runs}")


def main():
    report({
        "population_size": 100,
        "genotype_factory": BinaryGenotypeFactory(),
        "fitness_function": QuadraticFitnessFunction(),
        "crossover_probability": 1,
        "mutation_probability": 0
    })


if __name__ == "__main__":
    main()
