from genetic import *
import json
import string

# We'll teach an organism to look like an ascii cat (below).
#
# _
#( \
# ) )  -""-
#( (  `    `  A.-.A
# \ \/      \/ , , \
#  \   \    =;  t  /=
#   \   |""\  ',--'
#    / //  | ||
#   /_,))  |_,))

target = ["                    ",
          " _                  ",
          "( \                 ",
          " ) )  -\"\"-          ",
          "( (  `    `  A.-.A  ",
          " \ \/      \/ , , \ ",
          "  \   \    =;  t  /=",
          "   \   |\"\"\  ',--'  ",
          "    / //  | ||      ",
          "   /_,))  |_,))     "]
          
characters = ["(",")","\\","\"","'","t","A","/","-",".","-",",","|","`","_"," "]

# Generates a random organism for the 0th generation.
def generate_member():
    pass

# Mutates an organism.
def mutate_member(o):
    pass
    
# Create a new organism, using two others.
def merge_members(a, b):
    pass

# Evaluates the fitness of a population member. Less is better.
def evaluate_member(a):
    pass

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
for i in range(1, 10000):
    # Output simple stats about the population.
    if (i-1)%10==0:
        print "Gen #" + str(i-1), ":", [pop.generation_data[i-1].percentile(p) for p in [0, 25, 50, 75, 100]]
    if (i-1)%100==0:
        print "Gen #" + str(i-1), " best contender:"
        for row in pop.organisms[0].data:
            print row
    
    # Step through one generation.
    pop.step()

# Get the best organism after convergence or set amount of steps.
new = pop.organisms[0]

print "Gen 0:"
for row in old.data:
    print row
print "Final Gen:"
for row in new.data:
    print row