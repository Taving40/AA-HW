k = 100
s = [2, 2, 3, 4, 4, 3, 4, 6, 7, 8, 9, 10] #ex cu suma totala 62
w = [0 for _ in range(k + 1)] #vector de solutii posibile

for si in s: 
    for i in range(k, 0, -1): #parcurgem elemente posibile (in ordine inversa)
        if i+si <= k and w[i] == 1: #daca elementul merge adaugat la cel curent retinem in w
            w[i+si] = 1
            #print("w[{}+{}] = 1".format(i, si))
    w[si] = 1 #marcam elementul ca solutie valida (toate elementele sunt solutii valide din enunt)

for i in range(k, 0, -1): #parcurgem vectorul de sol posibile invers si alegem prima solutie gasita (cea mai mare)
    if w[i] == 1 :
        rez = i
        break

print(rez)
