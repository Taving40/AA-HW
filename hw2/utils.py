import random
import copy
from bisect import bisect_left

#get max performanta
def get_max_perf(populatie):
    maxx = -1
    index = -1
    individ = -1
    for i in range(len(populatie)):
        if populatie[i][2] > maxx:
            maxx = populatie[i][2]
            index = i
            individ = populatie[i][1]
    return maxx, index, individ 

def binary_search(a, x): #returneaza cea mai mare valoare strict mai mica decat x pe care o gaseste
    i = bisect_left(a, x)
    if i:
        if x >= a[i]:
            return i
        return (i-1)

    else:
        return -1

def cross_xy(crom_x, crom_y):
    taietura = random.choice(range(len(crom_x)))
    new_crom_x = crom_y[:taietura] + crom_x[taietura:]
    new_crom_y = crom_x[:taietura] + crom_y[taietura:]
    return [new_crom_x, new_crom_y, taietura]

def cross_xyz(crom_x, crom_y, crom_z):
    taietura = random.choice(range(len(crom_x)))
    crom_x_left = crom_x[:taietura]
    crom_x_right = crom_x[taietura:]
    crom_y_left = crom_y[:taietura]
    crom_y_right = crom_y[taietura:]
    crom_z_left = crom_z[:taietura]
    crom_z_right = crom_z[taietura:]

    new_crom_x = crom_x_left + crom_y_right
    new_crom_y = crom_y_left + crom_z_right
    new_crom_z = crom_z_left + crom_x_right

    return [new_crom_x, new_crom_y, new_crom_z, taietura]

def cross_xy2(crom_x, crom_y): #ABC XYZ ------> AYC XBZ 
    taietura1 = random.choice(range(len(crom_x)))
    taietura2 = random.choice(range(len(crom_x)))
    if taietura1 > taietura2:
        temp = taietura1
        taietura1 = taietura2
        taietura2 = temp
    new_crom_x = crom_x[:taietura1] + crom_y[taietura1:taietura2] + crom_x[taietura2:]
    new_crom_y = crom_y[:taietura1] + crom_x[taietura1:taietura2] + crom_y[taietura2:]
    return [new_crom_x, new_crom_y, taietura1, taietura2]

def cross_xyz2(crom_x, crom_y, crom_z): #ABC XYZ DEF ------> AYC XEZ DBF
    taietura1 = random.choice(range(len(crom_x)))
    taietura2 = random.choice(range(len(crom_x)))
    if taietura1 > taietura2:
        temp = taietura1
        taietura1 = taietura2
        taietura2 = temp
    new_crom_x = crom_x[:taietura1] + crom_y[taietura1:taietura2] + crom_x[taietura2:]
    new_crom_y = crom_y[:taietura1] + crom_z[taietura1:taietura2] + crom_y[taietura2:]
    new_crom_z = crom_z[:taietura1] + crom_x[taietura1:taietura2] + crom_z[taietura2:]
    return [new_crom_x, new_crom_y, new_crom_z, taietura1, taietura2]

    

def mutate(crom):
    xi = random.choice(range(len(crom)))
    l = copy.deepcopy(crom)
    l = list(l)
    if crom[xi] == '0':
        l[xi] = "1"
    else:
        l[xi] = "0"
    return "".join(l)