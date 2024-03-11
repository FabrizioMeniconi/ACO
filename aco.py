import numpy as np
import numpy.random as rnd
import tsplib95



# ACO prende in input il numero di formiche, di ere e il probleme e restituisce il miglior percorso trovato
def ACO(problem, ant, age):
    
    ncity = len(list(problem.get_nodes()))      # Numero delle città
    M = np.zeros ((ncity, ncity))               # Matrice dei feromoni
    a = np.zeros ((ant, ncity))                 # Miglior percorso di ogni formica
    rest = np.arange(ncity)                     # Vettore delle città rimaste da visitare
   
    for i in range(age):
        for n in range(ant):        
            patt = np.zeros(ncity)              #vettore dove viene memorizzato il percorso trascorso da una singola formica
            
            for c in range(ncity):               

                if c == 0:                      # La prima città visitata è sempre la 0
                    now = c                    
                else:                           # La prossima città da visitare viene scelta medianta la funzione probability
                    city = rest[now]
                    rest = np.delete(rest, now)
                    now = probability(rest, city, M, ncity, problem)
              
                patt[c] = rest[now]             # La nuova città visitata viene aggiunta a patt

            # Se il nuovo percorso della formica n è migliore di tutti quelli che ha intrapeso in passato a[n] diventa patt
            if(z(a[n], problem) == 0 or z(patt, problem) < z(a[n], problem)):
                a[n] = patt
          
            rest = np.arange(ncity)             # Viene resettato rest

        updateM(M, a, problem)                  # La matrice dei feromoni M viene aggiornata
        
        
    mini = 0                                    # In mini verrà memorizzata la minor distanza percorsa in a
    
    for x in range(len(a)):
        distance = z(a[x], problem)
        if mini == 0:
            mini = distance
            travel = a[x]                       # In travel viene memorizzato il miglio percorso
        if mini != 0 and mini > distance:
            mini = distance
            travel = a[x]

    # Vengono stampati i risultati
    print("")   
    print("Il percroso più corto trovato con", ant, "formiche e", age, "iterazioni è:")
    print(travel)
    print("E' lungo ", mini)



# Probability calcola le probabilità del nodo city di passare ad un suo vicino e sceglie il successore
def probability (rest, city, M, ncity, problem):

    prob = np.zeros (ncity)                     # Vettore delle probabilità
    tot = 0

    for x in range(len(rest)):                  # Si calcola il prodotto atterattività per traccia di ogni nodo
        index = rest[x]
        edge = int(city), int(rest[x])          # Nodo
        weight = problem.get_weight(*edge)      # Peso del nodo
        tot = tot + ((1/weight) * (M[city][index] + 0.001)) 

    for x in range(len(rest)):                  # Si divide il prodotto di atrrattività e traccia di un singolo nodo per tot
        index = rest[x]
        edge = int(city), int(rest[x])
        weight = problem.get_weight(*edge)
        # Inserisce il risultato in prob
        prob[index] = ((1/weight) * (M[city][index] + 0.001 )) / tot
    
    # Numero randomico tra 0 e 1
    random = rnd.uniform(low=0.0, high=1.0, size=None)
    
    prov = 0 

    for i in range(len(prob)):                  # Viene deciso in quale nodo andare in base alla sua probabilità
        prov = prov + prob[i]
        if random <= prov:
            for n in range(len(rest)):
                if rest[n] == i:
                    return n



# Funzione che utilizza a per aggiornare M
def updateM(M, a, problem):

    # Ogni elemento di M viene moltiplicato pe ril coefficiente di evaporazione
    for x in range(len(M)):
        for y in range(len(M[x])):
            M[x][y] = M[x][y] * 0.1

    # Ogni elemento di M viene incrementato in base a quante volte ha preso parte ad un percorso di a
    for x in range(len(a)):
        distance = z(a[x], problem)             # Distanza percorsa da un elemento di a
        for y in range(len(a[x])):
            city = int(a[x][y])
            if y+1 < len(a[x]):
                after = int(a[x][y+1])
            else:
                after = int(a[x][0])
            # A M[city][after] viene sommato 1 / distanza di a[n]
            M[city][after] = M[city][after] + 10/distance
            M[after][city] = M[city][after]

    
        
# Calcola la distanza totale di un percorso
def z (patt, problem):
    tot = 0
    for i in range(len(patt)):
        if i+1 < len(patt):
            edge = int(patt[i]), int(patt[i+1])
        else:
            edge = int(patt[i]), int(patt[0])
        weight = problem.get_weight(*edge)
        tot = tot + weight
    return tot
    

# Vengono caricati tre problemi diversi e fatti alcuni test
print("")
print("Il primo grafo conta 17 città, il miglior percorso è lungo 2085")
problem = tsplib95.load('./gr17.tsp')
ACO(problem, 5, 10)
ACO(problem, 25, 30)
ACO(problem, 50, 60)
print("")

print("")
print("Il secondo grafo conta 21 città, il miglior percorso è lungo 2707")
problem = tsplib95.load('./gr21.tsp')
ACO(problem, 5, 10)
ACO(problem, 25, 30)
ACO(problem, 50, 60)
print("")

print("")
print("Il terzoo grafo conta 24 città, il miglior percorso è lungo 1272")
problem = tsplib95.load('./gr24.tsp')
ACO(problem, 5, 10)
ACO(problem, 25, 30)
ACO(problem, 50, 60)