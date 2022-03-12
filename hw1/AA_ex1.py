summ = 0

#citire initiala

K = int(input("Introduceti suma maxima: "))
Xi = int(input("Introduceti urmatorul numar din sir, -1 pentru a termina de introdus: "))

#citim cate un numar pana se introduce -1

while Xi != -1:
    summ += Xi

    #adaugam numere la suma

    if summ > K: #verificare
        summ -= Xi

    #daca gasim un singur numar care ne satisface conditia ne oprim
    #astfel ne asiguram cazul in care inca nu am ajuns la o suma buna
    #insa toate numerele pe care le am adauga ne fac sa depasim suma dorita

    if Xi >= K/2:
        summ = Xi
        break

    Xi = int(input("Introduceti urmatorul numar din sir, -1 pentru a termina de introdus: "))



