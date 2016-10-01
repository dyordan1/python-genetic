import math
import random

class Organism:
    fitness = None
    data = None
    def __init__(self, data):
        self.data = data
    def mutate(self, mutate_func):
        self.data = mutate_func(self.data)
    def reproduce(self, reproduce_func, other):
        return Organism(reproduce_func(self.data, other.data))
    def score(self, fitness_func):
        self.fitness = fitness_func(self.data)

class GenerationStats:
    raw = []
    def __init__(self, population):
        self.raw = map(lambda o: o.fitness, population.organisms)
    
    def percentile(self, p):
        return self.raw[int((len(self.raw)-1)/100*p)]

class Population:
    generate_func = None
    mutate_func = None
    reproduce_func = None
    fitness_func = None
    organisms = []
    state = None
    generation_data = []

    def __init__(self, generate_func, mutate_func, reproduce_func, fitness_func, size):
        self.generate_func = generate_func
        self.mutate_func = mutate_func
        self.reproduce_func = reproduce_func
        self.fitness_func = fitness_func
        for i in range(0, size):
            self.organisms += [Organism(generate_func())]

    def step(self):
        # Score all organisms.
        for org in self.organisms:
            org.score(self.fitness_func)

        # Sort by fitness.
        self.organisms.sort(key=lambda o: o.fitness)
        
        # Record generation info.
        self.generation_data.append(GenerationStats(self))
        
        # Kill with gradient.
        population_size = len(self.organisms)
        for i, org in enumerate(self.organisms):
            if random.randrange(population_size) < i:
                self.organisms[i] = None
        
        # Replace missing in population with new.
        org_copy = self.organisms[:]
        for i, org in enumerate(self.organisms):
            if org is None:
                mom = None
                dad = None
                while True:
                    mom = self.organisms[random.randrange(population_size)]
                    if mom is not None:
                        break;
                while True:
                    dad = self.organisms[random.randrange(population_size)]
                    if dad is not None:
                        break;
                org_copy[i] = dad.reproduce(self.reproduce_func, mom)
                org_copy[i].mutate(self.mutate_func)
        self.organisms = org_copy[:]
    
    def has_converged(self):
        top = self.generation_data[-1].percentile(0)
        median = self.generation_data[-1].percentile(50)
        # < 1% difference between top and median in population
        return abs((top-median)/top) < 0.01
