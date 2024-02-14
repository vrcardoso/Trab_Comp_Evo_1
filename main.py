import random
import math

def create_board(boards,n_queens):
    n_matrix= n_queens * n_queens
    num_list = random.sample(range(n_matrix), n_queens)
    board = [[0 for _ in range(n_queens)] for _ in range(n_queens)]

    for i in num_list:
        board[(i//n_queens)][(i % n_queens)] = 1

    boards.append(board)


def queens_pos(board, n_queens):
    positions = []

    for i in range(n_queens):
        for j in range(n_queens):
           if board[i][j] == 1:
               positions.append([(i,j)])

    return positions





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




def veryfi(board, n_queens):
    crashs =0
    positions = queens_pos(board, n_queens)
    for i in range(n_queens):
        [(row, col)] = positions[i]
        crashs+= is_safe(board, row, col)

    
    return crashs



def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))


def chose_parents(colisions,n_parents):
    colisions_ord = colisions.copy()
    colisions_rem = colisions.copy()
    colisions_ord.sort()
    parents =[]

    for i in range(n_parents):
       parents.append(colisions_rem.index(colisions_ord[i]))
       colisions_rem[parents[i]] = math.inf

    return parents

    


def gen_childs(boards, colisions,n_parents,n_queens):
    parents = chose_parents(colisions,n_parents)
    n_matrix= n_queens * n_queens

    for i in range(len(boards)):
        if i in parents:
            continue
        
        child = [[0 for _ in range(n_queens)] for _ in range(n_queens)]
        chosens= random.sample(parents, 2)
        partition = random.randrange(n_matrix)
        parent1= boards[chosens[0]]
        parent2= boards[chosens[1]]
        
        for row in range(0,(partition//n_queens)):
          for col in range(n_queens):
            child[row][col]=parent1[row][col]

        for row in range((partition//n_queens),n_queens):
          for col in range(n_queens):
            child[row][col]=parent2[row][col]

        boards[i] = child




    
def mutation_childs(boards, colisions,n_parents,n_queens):
    parents = chose_parents(colisions,n_parents)
    n_matrix= n_queens * n_queens
    mutate_chance=50

    for i in range(len(boards)):
        if i in parents:
            continue
        
        child= boards[i]
        positions = queens_pos(child, n_queens)

        while len(positions) > n_queens:
            chosen= random.sample(positions, 1)
            [(row, col)] = positions[positions.index(chosen[0])]
            child[row][col] = 0
            positions = queens_pos(child, n_queens)

        while len(positions) < n_queens:
            i = random.sample(range(n_matrix), 1)
            child[(i[0]//n_queens)][(i[0] % n_queens)] = 1 
            positions = queens_pos(child, n_queens)

        if len(positions) == n_queens:
            if  random.randrange(100) < mutate_chance:
                continue

            chosen= random.randrange(len(positions))
            [(row, col)] = positions[chosen]
            child[row][col] = 0

            positions = queens_pos(child, n_queens)
            while len(positions) < n_queens:
                i = random.randrange(n_matrix)
                child[(i//n_queens)][(i % n_queens)] = 1 
                positions = queens_pos(child, n_queens)
         




    

def eight_queens():
    n_queens= 8
    boards=[]
    n_boards= 11
    colisions_initial=[]
    colisions=[]
    n_parents = 5
    max_gen= 200
    for i in range(n_boards):
        create_board(boards,n_queens)
        print("Board", i+1)
        print_board(boards[i])
        print()
        colisions.append(veryfi(boards[i], n_queens))

    colisions_initial =colisions.copy()
    print(colisions)
    print()
    for gen in range(max_gen):
        gen_childs(boards, colisions,n_parents,n_queens)
        mutation_childs(boards, colisions,n_parents,n_queens)
        colisions.clear()
        for j in range(n_boards):
           colisions.append(veryfi(boards[j], n_queens))

        print("Gen: ",gen,"Colisions: ", colisions)



    for i in range(n_boards):
        print("New ",i+1)
        print_board(boards[i])
        print()

    print("Initial Colisions: ", colisions_initial)
    print("Final Colisions: ", colisions)
    print()

    index_winner = chose_parents(colisions,n_parents)

    print("Best :", index_winner[0]+1)
    print_board(boards[index_winner[0]])
    print()

eight_queens()
