import itertools

from library.individual import BinaryGenotypeFactory, BinaryPhenotypeFactory, IndividualFactory, NumericalGenotypeFactory, NumericalPhenotypeFactory
from library.fitness import FitnessFunction, Constant100FitnessFunction, ConstantQuadraticFitnessFunction, FHDFitnessFunction, ExponentialFitnessFunction, QuadraticFitnessFunction, ConstantMinusQuadraticFitnessFunction
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
        iteration = 1
        while not self._stop_criteria(iteration):
            self.population.evolve(selection=self.selection,
                                   crossover=self.crossover,
                                   mutation=self.mutation)
            if verbose:
                if iteration % 10 == 0:
                    print(f"Iteration {iteration} has finished!")
            iteration += 1
        return self._check_for_solution()

    def _check_for_solution(self):
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


class GeneticAlgorithmSandbox:
    def __init__(self,
                 individual_factory: IndividualFactory,
                 fitness_functions: list[FitnessFunction]):
        crossovers: list[Crossover | None] = [
            OnePointCrossover(individual_factory), None]
        mutations: list[Mutation | None] = [DenseMutation(), None]
        selections: list[type[Selection]] = [RWS, SUS]

        self.settings: list[dict] = [
            {
                "selection": selection(fitness_function),
                "crossover": crossover,
                "mutation": mutation
            }
            for (selection, fitness_function, crossover, mutation)
            in itertools.product(*[selections, fitness_functions, crossovers, mutations])
        ]
        self.individual_factory = individual_factory

    def initial_population(self, size: int = 100):
        random_individuals = self.individual_factory.random(size - 1)
        optimal_individuals = self.individual_factory.optimal(1)

        individuals = random_individuals + optimal_individuals
        optimal = optimal_individuals[0]

        return Population(individuals, optimal)

    def report(self, size: int = 100, runs: int = 1, verbose=False):
        for _ in range(runs):
            initial_population = self.initial_population(size)

            for setting in self.settings:
                algorithm = f"<{', '.join(f'{name}:{subalgorithm.__class__.__name__}' for name, subalgorithm in setting.items())}>"

                if verbose:
                    print(f"{algorithm} is running...")

                population = initial_population.copy()

                if GeneticAlgorithm(population, *setting.values()).has_solution(verbose):
                    if verbose:
                        print(f"{algorithm} succeeded!")


class BinaryGeneticAlgorithmSandbox(GeneticAlgorithmSandbox):
    def __init__(self):
        super().__init__(individual_factory=IndividualFactory(genotype_factory=BinaryGenotypeFactory(length=100, codec=BinaryCodec()),
                                                              phenotype_factory=BinaryPhenotypeFactory(codec=BinaryCodec())),
                         fitness_functions=[
            Constant100FitnessFunction(),
            FHDFitnessFunction()
        ])


class NumericalGeneticAlgorithmSandbox(GeneticAlgorithmSandbox):
    def __init__(self):
        super().__init__(individual_factory=IndividualFactory(genotype_factory=NumericalGenotypeFactory(length=10, codec=BinaryCodec()),
                                                              phenotype_factory=NumericalPhenotypeFactory(codec=BinaryCodec())),
                         fitness_functions=[
            QuadraticFitnessFunction(),
            ConstantMinusQuadraticFitnessFunction(),
            ConstantQuadraticFitnessFunction(),
            ExponentialFitnessFunction(c=0.5),
            ExponentialFitnessFunction(c=1),
            ExponentialFitnessFunction(c=2)
        ])


def main(target="both", **kwargs):
    binary_sandbox = BinaryGeneticAlgorithmSandbox()
    numarical_sandbox = NumericalGeneticAlgorithmSandbox()
    if target == "binary":
        binary_sandbox.report(**kwargs)
    elif target == "numerical":
        numarical_sandbox.report(**kwargs)
    else:
        binary_sandbox.report(**kwargs)
        numarical_sandbox.report(**kwargs)


if __name__ == "__main__":
    main(target="numerical",
         size=100,
         runs=1,
         verbose=True)
