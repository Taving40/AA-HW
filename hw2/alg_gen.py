import math
import copy
import random
from utils import *
from bisect import bisect_left

# -----------------CITIRE-----------------------

f = open("input.txt", "r")
g = open("output.txt", "w")

bool_use_elitism = bool(int(f.readline().strip()))
print(bool_use_elitism)


dim_pop = int(f.readline().strip())
# print("dim_pop = {}".format(dim_pop))

domeniu = f.readline().strip().split(" ")
lwr_bound, uppr_bound = int(domeniu[0]), int(domeniu[1])
# print(lwr_bound, uppr_bound)

nr_termeni = int(f.readline().strip())
polinom = [] #tupluri de forma (grad, coef)
for _ in range(nr_termeni):
    termen = f.readline().split()
    polinom.append((int(termen[0]), int(termen[1])))
# print(polinom)

precision = int(f.readline().strip()) #nr de zecimale
# print(precision)

crossover = float(f.readline().strip())
# print(crossover)

mutation = float(f.readline().strip())
# print(mutation)

nr_etape = int(f.readline().strip())
# print(nr_etape)

f.close()

# -----------------CITIRE-----------------------

# -----------------GENERARE POPULATIE INITIALA-----------------------

#calculeaza lungime cromozom 
l = math.floor(math.log((uppr_bound - lwr_bound)*(10**precision), 2))
# print(l)

#genereaza l random bits (functie)
def get_crom(l=l):
    temp_list = []
    for _ in range(l):
        temp_list.append(random.choice(["0","1"]))
    return "".join(temp_list)
# print(get_crom(l))

#decodifica cromozom cu formula (functie)
def decode_crom(crom):
    return int(crom, 2)*((uppr_bound - lwr_bound)/((2**l)-1)) + lwr_bound
# print(decode_crom(get_crom()))

def fitness(x):
    rez = 0
    for termen in polinom:
        rez += (x**termen[0])*termen[1]
    return rez
# print(fitness(3))

populatie = []
print("Populatia initiala:\n")
g.write("Populatia initiala:\n")

for i in range(dim_pop):
    x = get_crom()
    y = decode_crom(x)
    print("{}: {}\t x = {} f = {}".format(i+1, x, y, fitness(y)))
    g.write("{}: {}\t x = {} f = {}\n".format(i+1, x, y, fitness(y)))
    populatie.append([x, y, fitness(y)])

# -----------------GENERARE POPULATIE INITIALA-----------------------

# -----------------PROCESUL DE SELECTIE----------------------- 

#determinare probabilitati de selectie

performanta_totala = 0
for crom in populatie:
    performanta_totala += crom[2]

print("\nProbabilitati selectie\n")
g.write("\nProbabilitati selectie\n")
for i in range(len(populatie)):
    populatie[i].append(populatie[i][2]/performanta_totala)
    print("cromozom\t {} probabilitate {}".format(i+1, populatie[i][3]))
    g.write("cromozom\t {} probabilitate {}\n".format(i+1, populatie[i][3]))

#determinare intervale

if bool_use_elitism:
    elita, index_elita, _ = get_max_perf(populatie)
    elita = copy.deepcopy(populatie[index_elita])

print("\nIntervale probabilitati selectie\n")
g.write("\nIntervale probabilitati selectie\n")

q = [0]
print(q[0], end=" ")
g.write(str(q[0]) + " ")
for i in range(len(populatie)):
    q.append(q[i] + populatie[i][3])
    print(q[i+1], end=" ")
    g.write(str(q[i+1])+ " ")
print()  
g.write("\n") 

#generare u
populatie_prim = []
for _ in range(len(populatie)):
    u = random.random()
    poz = binary_search(q, u)
    print("u = {}\t selectam cromozomul {}".format(u, poz+1))
    g.write("u = {}\t selectam cromozomul {}\n".format(u, poz+1))
    populatie_prim.append(copy.deepcopy(populatie[poz]))

print("Dupa selectie:")
g.write("Dupa selectie: \n")
for i in range(len(populatie_prim)):
    print("\t {}: {}\t x = {} f = {}".format(i+1, populatie_prim[i][0], populatie_prim[i][1], populatie_prim[i][2]))
    g.write("\t {}: {}\t x = {} f = {}\n".format(i+1, populatie_prim[i][0], populatie_prim[i][1], populatie_prim[i][2]))

# -----------------PROCESUL DE SELECTIE-----------------------

# -----------------PROCESUL DE CROSSOVER-----------------------

print("\nProbabilitatea de incrucisare {}\n".format(crossover))
g.write("\nProbabilitatea de incrucisare {}\n".format(crossover))

populatie_crossover = []

for i in range(len(populatie_prim)):
    u = random.random()
    print("{}: {} u = {}".format(i+1, populatie_prim[i][0], u), end = " ")
    g.write("{}: {} u = {}".format(i+1, populatie_prim[i][0], u) + " ")
    if u < crossover:
        print("<{} participa".format(crossover))
        g.write("<{} participa\n".format(crossover))
        populatie_crossover.append([copy.deepcopy(populatie_prim[i]), i])
    else:
        print()
        g.write("\n")

if len(populatie_crossover)%2 == 0:
    for i in range(0, len(populatie_crossover)-1, 2):
        print("Recombinare dintre cromozomul {} cu cromozomul {}:".format(populatie_crossover[i][1]+1, populatie_crossover[i+1][1]+1))
        g.write("Recombinare dintre cromozomul {} cu cromozomul {}:\n".format(populatie_crossover[i][1]+1, populatie_crossover[i+1][1]+1))
        print("{} {} puncte ".format(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0]), end="")
        g.write("{} {} puncte ".format(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0]))
        temp_list = cross_xy2(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0])
        populatie_crossover[i][0][0] = temp_list[0]
        populatie_crossover[i+1][0][0] = temp_list[1]
        taietura1 = temp_list[2]
        taietura2 = temp_list[3]
        print(str(taietura1) + " " + str(taietura2))
        g.write(str(taietura1) + "\n")
        print("Rezultat \t {} {}".format(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0]))
        g.write("Rezultat \t {} {}\n".format(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0]))

elif len(populatie_crossover)%2 == 1 and len(populatie_crossover) > 2:
    tratat_separat = populatie_crossover[-3:]
    populatie_crossover = populatie_crossover[:-3]
    #print("\nlungime separat = {}, lungime pop_cross = {}\n".format(len(tratat_separat), len(populatie_crossover)))

    for i in range(0, len(populatie_crossover)-1, 2):
        print("Recombinare dintre cromozomul {} cu cromozomul {}:".format(populatie_crossover[i][1]+1, populatie_crossover[i+1][1]+1))
        g.write("Recombinare dintre cromozomul {} cu cromozomul {}:\n".format(populatie_crossover[i][1]+1, populatie_crossover[i+1][1]+1))
        print("{} {} punct ".format(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0]), end="")
        g.write("{} {} punct ".format(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0]))
        temp_list = cross_xy2(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0])
        
        populatie_crossover[i][0][0] = temp_list[0]
        populatie_crossover[i][0][1] = decode_crom(populatie_crossover[i][0][0]) #update rest of fields
        populatie_crossover[i][0][2] = fitness(populatie_crossover[i][0][1])

        populatie_crossover[i+1][0][0] = temp_list[1]
        populatie_crossover[i+1][0][1] = decode_crom(populatie_crossover[i+1][0][0])
        populatie_crossover[i+1][0][2] = fitness(populatie_crossover[i+1][0][1])

        taietura1 = temp_list[2]
        taietura2 = temp_list[3]
        print(str(taietura1) + " " + str(taietura2))
        g.write(str(taietura1) + "\n")
        print("Rezultat \t {} {}".format(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0]))
        g.write("Rezultat \t {} {}\n".format(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0]))
    
    print("Recombinare dintre ultimii trei cromozomi {}, {} si {}:".format(tratat_separat[0][1]+1, tratat_separat[1][1]+1, tratat_separat[2][1]+1))
    g.write("Recombinare dintre ultimii trei cromozomi {}, {} si {}:\n".format(tratat_separat[0][1]+1, tratat_separat[1][1]+1, tratat_separat[2][1]+1))
    print("{} {} {} punct ".format(tratat_separat[0][0][0], tratat_separat[1][0][0], tratat_separat[2][0][0]), end="")
    g.write("{} {} {} punct ".format(tratat_separat[0][0][0], tratat_separat[1][0][0], tratat_separat[2][0][0]))
    temp_list = cross_xyz2(tratat_separat[0][0][0], tratat_separat[1][0][0], tratat_separat[2][0][0])
    for i in range(3):
        tratat_separat[i][0][0] = temp_list[i]
        tratat_separat[i][0][1] = decode_crom(tratat_separat[i][0][0])
        tratat_separat[i][0][2] = fitness(tratat_separat[i][0][1])
    taietura = temp_list[3]
    print(taietura)
    g.write(str(taietura) + "\n")
    print("Rezultat \t {} {} {}".format(tratat_separat[0][0][0], tratat_separat[1][0][0], tratat_separat[2][0][0]))
    g.write("Rezultat \t {} {} {}".format(tratat_separat[0][0][0], tratat_separat[1][0][0], tratat_separat[2][0][0]) + "\n")
    populatie_crossover.extend(tratat_separat)

#replace crossovered individuals in populatie_prim
for i in range(len(populatie_crossover)):
    index_to_replace = populatie_crossover[i][1]
    populatie_prim[index_to_replace] = populatie_crossover[i][0]

print("Dupa recombinare: ")
g.write("Dupa recombinare: \n")
for i in range(len(populatie_prim)):
    print("\t {}: {}\t x = {} f = {}".format(i+1, populatie_prim[i][0], populatie_prim[i][1], populatie_prim[i][2]))
    g.write("\t {}: {}\t x = {} f = {}\n".format(i+1, populatie_prim[i][0], populatie_prim[i][1], populatie_prim[i][2]))

# -----------------PROCESUL DE CROSSOVER-----------------------

# -----------------PROCESUL DE MUTATIE-----------------------

print("Probabilitate de mutatie pentru fiecare gena {}".format(mutation))
g.write("Probabilitate de mutatie pentru fiecare gena {}\n".format(mutation))
populatie_mutation = []

for i in range(len(populatie_prim)):
    u = random.random()
    if u < mutation:
        populatie_mutation.append([copy.deepcopy(populatie_prim[i]), i])

print("Au fost modificati cromozomii: ")
g.write("Au fost modificati cromozomii: \n")
for x in populatie_mutation:
    print(x[1]+1)
    g.write(str(x[1]+1) + "\n")

for i in range(len(populatie_mutation)):
    #print("{} mutated {} into ".format(populatie_mutation[i][1]+1, populatie_mutation[i][0][0]), end="")
    #g.write("{} mutated {} into ".format(populatie_mutation[i][1]+1, populatie_mutation[i][0][0]))

    populatie_mutation[i][0][0] = mutate(populatie_mutation[i][0][0])

    print(populatie_mutation[i][0][0])
    g.write(populatie_mutation[i][0][0] + "\n")

    populatie_mutation[i][0][1] = decode_crom(populatie_mutation[i][0][0])
    populatie_mutation[i][0][2] = fitness(populatie_mutation[i][0][1])

#replace mutated individuals in populatie_prim
for i in range(len(populatie_mutation)):
    index_to_replace = populatie_mutation[i][1]
    # print("trying to replace cromozomul de pe pozitia {}".format(index_to_replace))
    populatie_prim[index_to_replace] = populatie_mutation[i][0]

#adaugam elita inapoi dupa ce am terminat mutatia
if bool_use_elitism:
    populatie_prim[index_elita] = elita

print("Dupa mutatie: ")
g.write("Dupa mutatie: \n")
for i in range(len(populatie_prim)):
    print("\t {}: {}\t x = {} f = {}".format(i+1, populatie_prim[i][0], populatie_prim[i][1], populatie_prim[i][2]))
    g.write("\t {}: {}\t x = {} f = {}\n".format(i+1, populatie_prim[i][0], populatie_prim[i][1], populatie_prim[i][2]))


# -----------------PROCESUL DE MUTATIE-----------------------

# -----------------AFISARE RESTUL PASILOR-----------------------

populatie = copy.deepcopy(populatie_prim)


print("Evolutia maximului")
g.write("Evolutia maximului\n")
for _ in range(nr_etape-1):

    print(get_max_perf(populatie)[0], get_max_perf(populatie)[2]  , sep= " ")
    g.write(str(get_max_perf(populatie)[0]) + "\n")
    #SELECTIE

    performanta_totala = 0
    for crom in populatie:
        performanta_totala += crom[2]

    for i in range(len(populatie)):
        populatie[i].append(populatie[i][2]/performanta_totala)

    #calcul elita
    if bool_use_elitism:
        elita, index_elita, _ = get_max_perf(populatie)
        elita = copy.deepcopy(populatie[index_elita])


    #determinare intervale
    q = [0]
    for i in range(len(populatie)):
        q.append(q[i] + populatie[i][3])

    #generare u
    populatie_prim = []
    for _ in range(len(populatie)):
        u = random.random()
        poz = binary_search(q, u)
        populatie_prim.append(copy.deepcopy(populatie[poz]))

    #CROSSOVER

    #ABC XYZ ------> AYC XBZ 

    populatie_crossover = []

    for i in range(len(populatie_prim)):
        u = random.random()
        if u < crossover:
            populatie_crossover.append([copy.deepcopy(populatie_prim[i]), i])

    if len(populatie_crossover)%2 == 0:
        for i in range(0, len(populatie_crossover)-1, 2):
            temp_list = cross_xy(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0])
            populatie_crossover[i][0][0] = temp_list[0]
            populatie_crossover[i+1][0][0] = temp_list[1]

    elif len(populatie_crossover)%2 == 1 and len(populatie_crossover) > 2:
        tratat_separat = populatie_crossover[-3:]
        populatie_crossover = populatie_crossover[:-3]

        for i in range(0, len(populatie_crossover)-1, 2):
        
            temp_list = cross_xy(populatie_crossover[i][0][0], populatie_crossover[i+1][0][0])
            
            populatie_crossover[i][0][0] = temp_list[0]
            populatie_crossover[i][0][1] = decode_crom(populatie_crossover[i][0][0]) #update rest of fields
            populatie_crossover[i][0][2] = fitness(populatie_crossover[i][0][1])

            populatie_crossover[i+1][0][0] = temp_list[1]
            populatie_crossover[i+1][0][1] = decode_crom(populatie_crossover[i+1][0][0])
            populatie_crossover[i+1][0][2] = fitness(populatie_crossover[i+1][0][1])
        
        temp_list = cross_xyz(tratat_separat[0][0][0], tratat_separat[1][0][0], tratat_separat[2][0][0])
        for i in range(3):
            tratat_separat[i][0][0] = temp_list[i]
            tratat_separat[i][0][1] = decode_crom(tratat_separat[i][0][0])
            tratat_separat[i][0][2] = fitness(tratat_separat[i][0][1])

        populatie_crossover.extend(tratat_separat)

    #replace crossovered individuals in populatie_prim
    for i in range(len(populatie_crossover)):
        index_to_replace = populatie_crossover[i][1]
        populatie_prim[index_to_replace] = populatie_crossover[i][0]

    #MUTATIE

    populatie_mutation = []

    for i in range(len(populatie_prim)):
        u = random.random()
        if u < mutation:
            populatie_mutation.append([copy.deepcopy(populatie_prim[i]), i])

    for i in range(len(populatie_mutation)):
        populatie_mutation[i][0][0] = mutate(populatie_mutation[i][0][0])
        populatie_mutation[i][0][1] = decode_crom(populatie_mutation[i][0][0])
        populatie_mutation[i][0][2] = fitness(populatie_mutation[i][0][1])

    #replace mutated individuals in populatie_prim
    for i in range(len(populatie_mutation)):
        index_to_replace = populatie_mutation[i][1]
        populatie_prim[index_to_replace] = populatie_mutation[i][0]

    populatie = copy.deepcopy(populatie_prim)
    if bool_use_elitism:
        populatie[index_elita] = elita



g.close()

# -----------------AFISARE RESTUL PASILOR-----------------------