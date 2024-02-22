import random
import math


#funcao que recebe uma lista de tabuleiros e a quantidade de rainhas
#cria um tabuleiro NxN com N rainhas colocadas aleatoriamente, e insere na lista de tabuleiros
def create_board(boards,n_queens):
    n_matrix= n_queens * n_queens
    num_list = random.sample(range(n_matrix), n_queens) #funcao que gera uma lista de numeros de 0 a N, e escolhe N numeros dessa lista
    board = [[0 for _ in range(n_queens)] for _ in range(n_queens)] #funcao que gera uma matriz NxN preenchida com 0s

    #Pega a lista de numeros escolhidos, e insere as rainhas nas posicoes escolhidas, rainhas = 1
    for i in num_list:
        board[(i//n_queens)][(i % n_queens)] = 1 

    boards.append(board)


#funcao que recebe um tabuleiro e a quantidade de rainhas, e retorna uma lista de tuplas com as posicoes das rainhas no tabuleiro
def queens_pos(board, n_queens):
    positions = []

    for i in range(n_queens):
        for j in range(n_queens):
           if board[i][j] == 1:
               positions.append([(i,j)])

    return positions




#funcao que rece um tabuleio, e as cordenadas de uma rainha, e retorna a quantidade de colisoes, para frente, que aquela rainha possui
def is_safe(board, row, col):

    crashs = 0
    # Check for queens in the same row
    for i in range(col+1, len(board)):
        if board[row][i] == 1:
            crashs+=1

    # Check for queens in the same column
    for i in range(row+1, len(board)):
        if board[i][col] == 1:
            crashs+=1

    # Check for queens in the upper-left diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if i== row and j == col:
            continue
        if board[i][j] == 1:
            crashs+=1

    # Check for queens in the upper-right diagonal
    for i, j in zip(range(row, -1, -1), range(col, len(board))):
        if i== row and j == col:
            continue
        if board[i][j] == 1:
            crashs+=1
    
    return crashs




#funcao que recebe um tabuleiro eo numero de rainhas, e retorna o numero de colisoes
def veryfi(board, n_queens):
    crashs =0
    positions = queens_pos(board, n_queens) #pega posicao das rainhas
    for i in range(n_queens):
        [(row, col)] = positions[i]
        crashs+= is_safe(board, row, col) #conta a quantidade de colisoes de cada rainha

    
    return crashs


#funcao que imprime um tabuleiro
def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))



#funcao que recebe uma lista com o numero de colisoes dos tabuleiros e o numero de parentes escolhido pelo usuario
#Retorna uma lista com a posicao dos N tabuleiros com menas colisoes, que seram os novos pais da proxima geracao
def chose_parents(colisions,n_parents):
    colisions_ord = colisions.copy() #copia a lista de colisoes para nao alterar a original
    colisions_rem = colisions.copy() #copia a lsita de colisoes para nao alerar a origial
    colisions_ord.sort() #ordena a lista de colisoes em ordem crescente
    parents =[]
    repetitons=[]

    #pega o index original dos N primeiros elementos da lista ordenada 
    for i in range(n_parents):
       #Cria uma lista com os tabuleiros com o mesmo numero de colisoes e caso tenha repeticoes escolhe aleatoriamente entre eles
       repetitons = [y for x,y in zip(colisions_rem, range(len(colisions))) if x == colisions_ord[i]]
       if len(repetitons) ==1:
           parents.append(repetitons[0])
       else:
           parent = random.sample(repetitons, 1)
           parents.append(parent[0])
       #troca o valor da colisao na lista de colisoes, para evitar repetir o index, de dois tabuleiros com mesmo numero de colisoes
       colisions_rem[parents[i]] = math.inf 

    return parents

    

#funcao que recebe uma lista de tabuleiros, uma lista de colisoes, numero de pais,e numero de rainhas
#gera novos filhos cruzando dois pais, da lista de pais escolhidos, e substitui um tabuleiro nao pai da tabela de tabuleiros
def gen_childs(boards, colisions,n_parents,n_queens):
    parents = chose_parents(colisions,n_parents)
    n_matrix= n_queens * n_queens

    for i in range(len(boards)):
        if i in parents: # verifica se o tabuleiro que esta na posicao i da lista de tabuleiros, nao e um tabuleiro pai
            continue
        
        child = [[0 for _ in range(n_queens)] for _ in range(n_queens)] #funcao que gera uma matriz NxN preenchida com 0s
        chosens= random.sample(parents, 2) #Escolhe aleatoriamente dois pais da lista de pais
        partition = random.randrange(n_matrix) #escolhe um numero de 0 a NxN, para decidir o ponto de particao de cada pai
        parent1= boards[chosens[0]] #pega da lista de tabueliros,os pais escolhidos
        parent2= boards[chosens[1]]
        
     #preenche os tabuleiros filhos com os elementos do pai1, sendo pai1 de 0 a partition
        for row in range(0,(partition//n_queens)):
          for col in range(n_queens):
            child[row][col]=parent1[row][col]

     #preenche os tabuleiros filhos com os elementos dos pai2, sendo pai2 de partiton a NxN
        for row in range((partition//n_queens),n_queens):
          for col in range(n_queens):
            child[row][col]=parent2[row][col]

        boards[i] = child #substitui tabuleiro que esta na posicao i da lista de tabuleiros, pelo novo filho gerado

        return parents




#funcao que recebe uma lista de tabuleiro, uma lista de colisoes, o numeros de pais, numero de rainhas e a chance da mutacao
#E gera mutatoes nos tabuleiros filhos em com uma probabilidade = mutante_chance
#tambem corrigi o numero de rainhas nos filhos, que durante a combinacao dos parentes podem ser gerados com menos de N rainhas
def mutation_childs(boards, parents,n_queens,mutate_chance =50):
    n_matrix= n_queens * n_queens
    for i in range(len(boards)):
        if i in parents:
            continue
        
        child= boards[i]
        positions = queens_pos(child, n_queens)
        
        #verifica se o tabuleiro tem menos de N rainhas, se sim adiciona novas rainhas ate corrigir a quantidade
        while len(positions) > n_queens:
            chosen= random.sample(positions, 1)
            [(row, col)] = positions[positions.index(chosen[0])]
            child[row][col] = 0
            positions = queens_pos(child, n_queens)

    #verifica se o tabuleiro tem mais de N rainhas, se sim retira rainhas aleatoriamente ate corrigir a quantidade
        while len(positions) < n_queens:
            i = random.sample(range(n_matrix), 1)
            child[(i[0]//n_queens)][(i[0] % n_queens)] = 1 
            positions = queens_pos(child, n_queens)
     
     #gera um numero aletorio de 0 a 99 e se for > que mutante_chance, ele nao gera a mutacao
        if  random.randrange(100) > mutate_chance:
            continue

     #Se o numero gerado for menor que mutate_chance, escolhe aleatoriamente a posicao de uma rainha e retira ela
        chosen= random.randrange(len(positions))
        [(row, col)] = positions[chosen]
        child[row][col] = 0
        positions.pop(chosen)

     #Escolhe uma posicao aleatoria e coloca uma nova rainha, caso ja tenha uma rainha nessa posicao faz denovo o processo  
        while len(positions) < n_queens:
            i = random.randrange(n_matrix)
            child[(i//n_queens)][(i % n_queens)] = 1 
            positions = queens_pos(child, n_queens)
         




    

def eight_queens():
    n_queens= 8      #Tamanho do problema, numero de rainhas
    n_parents = 5    #Numero de tabuleiros pais que seram escolhidos
    max_gen= 10000    #Numero maximo de geracoes
    n_boards= 11     #Numero de tabuleiros por geracao
    mutate_chance = 50 #Chance de mutacao
    boards=[]
    colisions_initial=[]
    colisions=[]

 #cria populacao inicial
    for i in range(n_boards):
        create_board(boards,n_queens)
        print("Board", i+1)
        print_board(boards[i])
        print()
        colisions.append(veryfi(boards[i], n_queens))

    colisions_initial =colisions.copy()
    print(colisions)
    print()

   #loop das geracoes 
    for gen in range(max_gen):
        parents = gen_childs(boards, colisions,n_parents,n_queens)
        mutation_childs(boards, parents,n_queens,mutate_chance)
        colisions.clear()
        for j in range(n_boards):
           colisions.append(veryfi(boards[j], n_queens))

        print("Gen: ",gen,"Colisions: ", colisions)
    #para se achar uma solucao
        if 0 in colisions:
            break



 #imprime ultima geracao
    for i in range(n_boards):
        print("New ",i+1)
        print_board(boards[i])
        print()

    print("Initial Colisions: ", colisions_initial)
    print("Final Colisions: ", colisions)
    print()

    index_winner = chose_parents(colisions,n_parents) #pega melhor resultado

    print("Best :", index_winner[0]+1," of gen : " ,gen+1)
    print_board(boards[index_winner[0]])
    print()

eight_queens()
