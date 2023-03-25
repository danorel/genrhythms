import os
import itertools
import matplotlib.pyplot as plt

from collections import Counter
from statistics import stdev

from library.individual import BinaryGenotypeFactory, BinaryPhenotypeFactory, IndividualFactory, NumericalGenotypeFactory, NumericalPhenotypeFactory
from library.fitness import FitnessFunction, Constant100FitnessFunction, ConstantQuadraticFitnessFunction, FHDFitnessFunction, ExponentialFitnessFunction, QuadraticFitnessFunction, ConstantMinusQuadraticFitnessFunction, QuarterExponentialFitnessFunction, TwiceExponentialFitnessFunction
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

    def solve(self, verbose: bool = False):
        snapshots: list[Population] = []
        generation = 1
        while not self._stop_criteria(generation):
            snapshots.append(self.population.copy())
            self.population.evolve(selection=self.selection,
                                   crossover=self.crossover,
                                   mutation=self.mutation)
            if verbose:
                if generation % 25 == 0:
                    print(f"Generation {generation} has grown!")
            generation += 1
        return self._check_for_solution(), snapshots + [self.population.copy()]

    def _check_for_solution(self):
        if self.mutation is not None:
            return self.population.is_optimal(percentage=90)
        else:
            return self.population.is_optimal(percentage=100)

    def _stop_criteria(self, generation: int):
        if self.mutation is not None:
            if generation == 10000001 or self.population.is_homogeneous(percentage=99):
                return True
        else:
            if generation == 10000001 or self.population.is_identical():
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
                "fitness_function": fitness_function,
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

    def report(self,
               size: int = 100,
               runs: int = 1,
               snapshot_first: int = 5,
               verbose=False):
        statistics = Counter()

        for run in range(1, runs + 1):
            initial_population = self.initial_population(size)

            for setting in self.settings:
                fitness_function, *rest_setting = setting.values()

                name = f"<{', '.join(f'{function.__class__.__name__}' for function in setting.values())}>"

                if verbose:
                    print(f"{name} is running...")

                algorithm = GeneticAlgorithm(
                    initial_population.copy(), *rest_setting)
                has_solution, populations = algorithm.solve(verbose)

                statistics[name] += 1 if has_solution else 0

                if run <= snapshot_first:
                    self.plot_snapshot(run,
                                       populations,
                                       fitness_function,
                                       name)

    def plot_snapshot(self,
                      run: int,
                      populations: list[Population],
                      fitness_function: FitnessFunction,
                      algorithm_name: str):
        plot_data = []

        N = len(populations[0].individuals)
        generations = [number for number in range(1, len(populations) + 1)]

        for population in populations:
            individuals_health = [fitness_function.score(
                individual) for individual in population.individuals]
            plot_data.append({
                "Mean health": sum(individuals_health) / len(individuals_health),
                "Max health": max(individuals_health),
                "Min health": min(individuals_health),
                "Stdev health": stdev(individuals_health)
            })

        dirfig = f"function/{N}/{algorithm_name}/{run}"
        if not os.path.exists(dirfig):
            os.makedirs(dirfig)

        def plot_metric(metric_name: str):
            metric_data = list(
                map(lambda plot_item: plot_item[metric_name], plot_data))
            plt.title(metric_name)
            plt.plot(generations, metric_data)
            plt.ylabel(metric_name)
            plt.xlabel("Generation")
            plt.savefig(f'{dirfig}/{metric_name}')
            plt.clf()

        metrics = ["Mean health", "Max health", "Min health", "Stdev health"]

        for metric in metrics:
            plot_metric(metric)


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
            QuarterExponentialFitnessFunction(),
            ExponentialFitnessFunction(),
            TwiceExponentialFitnessFunction(),
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
         snapshot_first=5,
         verbose=True)
