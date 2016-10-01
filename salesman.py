from genetic import *
import json

# Generates a random organism for the 0th generation.
def generate_member():
    r = range(0, 42)
    random.shuffle(r)
    return r

# Mutates an organism.
def mutate_member(o):
    # OK, doesn't mutate an organism.
    return o
    
# Create a new organism, using two others.
def merge_members(a, b):
    # Keep all the nodes chosen from a in a set.
    seen = set()

    # Initialize to empty genome.
    new = [None] * len(a)
    
    # Probabilistically pick alleles from a.
    for i, n in enumerate(a):
      if (random.randrange(2) < 1):
        new[i] = n
        seen.add(n)

    # Fill in the gaps with alleles from b in sequence.
    bIndex = 0
    for i, n in enumerate(a):
        if new[i] != None:
            continue
        while bIndex < len(b) and b[bIndex] in seen:
            bIndex += 1
        new[i] = b[bIndex]
        bIndex += 1
    return new

# Generate 10 random points on the grid
points = [[random.randrange(11), random.randrange(11)] for i in range(0,42)]

# Evaluates the fitness of a population member. Less is better.
def evaluate_member(a):
    previous = a[0]
    total = 0
    for i in range(1,42):
        dx = points[a[i]][0] - points[previous][0]
        dy = points[a[i]][1] - points[previous][1]
        total += math.sqrt(dx*dx + dy*dy)
        previous = a[i]
    return total

# Initialize
pop = Population(
    generate_member,
    mutate_member,
    merge_members,
    evaluate_member,
    1000
)

# Step one generation to get the best randomly generated organism.
pop.step()
old = pop.organisms[0]

# Step a set amount of times or until converged.
for i in range(1, 1000):
    # Output simple stats about the population.
    if (i-1)%10==0:
        print "Gen #" + str(i-1), ":", [pop.generation_data[i-1].percentile(p) for p in [0, 25, 50, 75, 100]]
    
    # Step through one generation.
    pop.step()
    
    # Check for convergence.
    if (pop.has_converged()):
        print "Converged after", i, "generations."
        break;

# Get the best organism after convergence or set amount of steps.
new = pop.organisms[0]

# Salesman specific - export fake save for web UI to visualize.
save = {}
save["n"] = 10
save["m"] = 10
save["count"] = 42
save["cities"] = map(lambda p: {"_x": p[0], "_y": p[1]}, points)
save["popCount"] = 1
save["population"] = {"_members": map(lambda o: {"_seq": o.data, "_length": o.fitness}, [old, new]), "_state": "NEW"}
print json.dumps(save)
# Web UI: http://output.jsbin.com/roxebux