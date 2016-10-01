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
    return [''.join(random.choice(characters) for _ in range(20)) for i in range (0,10)]

# Mutates an organism.
def mutate_member(o):
    # 1% chance to mutate every character that is not a space (to preserve the shape)
    for i, row in enumerate(o):
        for j in range(0, len(row)):
            if random.randrange(5) == 0 and row[j] != target[i][j]:
                nr = list(row)
                nr[j] = random.choice(characters)
                #nr[j] = ord(nr[j])
                #diff = -1 if random.randrange(2) == 0 else 1
                #while (random.randrange(100) < 66):
                #    nr[j] += diff
                #    nr[j] %= 256
                #nr[j] = chr(nr[j])
                row = ''.join(nr)
    return o
    
# Create a new organism, using two others.
def merge_members(a, b):
    # Initially, just mix a bunch of rows from the two.
    new = []
    for i, row in enumerate(a):
        if random.randrange(2) == 0:
            new.append(row)
        else:
            new.append(b[i])
        
    # Then, shuffle the rows with a probability 5%
    for i in reversed(range(1,len(new))):
        if random.randrange(10) == 0:
            j = random.randrange(i)
            temp = new[j]
            new[j] = new[i]
            new[i] = temp
    
    # Do the same with cols.
    for i in reversed(range(1,len(new[0]))):
        if random.randrange(10) == 0:
            for k in range(0,len(new)):
                s = list(new[k])
                j = random.randrange(i)
                temp = s[j]
                s[j] = s[i]
                s[i] = temp
                new[k] = ''.join(s)
    return new

# Evaluates the fitness of a population member. Less is better.
def evaluate_member(a):
    score = 0
    for i, row in enumerate(a):
        for j, c in enumerate(row):
            score += abs(ord(c) - ord(target[i][j]))
    return score

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