# Jan 12, 0952 version
import sys
import random
import math

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
# To refer to neighbor squares we can add a direction to a square.
N, S, E, W = -10, 10, 1, -1
NE, SE, NW, SW = N + E, S + E, N + W, S + W
DIRECTIONS = (N, NE, E, SE, S, SW, W, NW)
PLAYERS = {BLACK: "Black", WHITE: "White"}
CORNERS = (11, 18, 81, 88)
# SCORE_MATRIX = [0, 0,   0,   0,  0,  0,  0,  0,   0,    0,
#                 0, 160, -20, 20, 5,  5,  20, -20, 160,  0,
#                 0, -20, -50, -5, -5, -5, -5, -50, -20,  0,
#                 0, 20,  -5,  15, 3,  3,  15, -5,  20,   0,
#                 0, 5,   -5,  3,  3,  3,  3,  -5,  5,    0,
#                 0, 5,   -5,  3,  3,  3,  3,  -5,  5,    0,
#                 0, 20,  -5,  15, 3,  3,  15, -5,  20,   0,
#                 0, -20, -50, -5, -5, -5, -5, -50, -20,  0,
#                 0, 160, -20, 20, 5,  5,  20, -20, 160,  0,
#                 0, 0,   0,   0,  0,  0,  0,  0,   0,    0]
SCORE_MATRIX = [0, 0,   0,   0,  0,  0,  0,  0,   0,    0,
                0, 210, -20, 30, 15, 15, 30, -20, 210, 0,
                0, -20, -50, -5, -5, -5,  -5, -50, -20, 0,
                0, 30,  -5,  15, 3,  3,  15, -5,  30,   0,
                0, 15,  -5,  3,  3,  3,  3,  -5,  15,   0,
                0, 15,  -5,  3,  3,  3,  3,  -5,  15,   0,
                0, 30,  -5,  15, 3,  3,  15, -5,  30,   0,
                0, -20, -50, -5, -5, -5, -5, -50, -20,  0,
                0, 210, -20, 30, 15, 15,  30, -20, 210, 0,
                0, 0,   0,   0,  0,  0,  0,  0,   0,    0]

########## ########## ########## ########## ########## ##########
# The strategy class for your AI
# You must implement this class
# and the method best_strategy
# Do not tamper with the init method's parameters, or best_strategy's parameters
# But you can change anything inside this you want otherwise
#############################################################
class Node:
    def __init__(self, board, move = None, score = None):   # may/may not have move or score argument
        self.board = board
        self.move = move
        self.score = score
    def __lt__(self, other):
        return self.score < other.score
class Strategy():
    def __init__(self):
        # FILL IN
        self.board = self.get_starting_board()  ## MAY NEED TO FIX THIS

    def get_starting_board(self):
        # Create new board with initial black and white positions filled
        topbottom = 10*OUTER
        midempty = OUTER+(8*EMPTY)+OUTER
        r4 = OUTER+(3*EMPTY)+WHITE+BLACK+(3*EMPTY)+OUTER
        half = topbottom+(3*midempty)+r4
        board = half+half[::-1] # front half and reverse of front half
        return board

    ##########################################################
    def convert_size8_to_size10(self, board8):
        # HELPER -- format
        # converts 8x8 board to 10x10 board (with border)
        topbottom = 10*OUTER
        middle = "".join([OUTER + board8[x*8:(x+1)*8] + OUTER for x in range(8)])
        newBoard = topbottom + middle + topbottom

        newBoard = newBoard.replace("X", "@")
        newBoard = newBoard.replace("O", "o")

        return newBoard
    def convert_size10_to_size8(self, board10):
        newBoard = "".join([x for x in board10 if x != OUTER])
        return newBoard
    def convert_index10_to_index8(self, i):
        deduct = 11+2*(int(i/10)-1)
        return i-deduct
    def get_pretty_board(self, board):
        size = int(math.sqrt(len(board)))
        pretty = "".join([" ".join(board[x*size:(x+1)*size])+'\n' for x in range(size)])
        pretty = pretty[:len(pretty)-1]
        return pretty

    ##########################################################

    def opponent(self, player):
        # HELPER
        # Get player's opponent
        if player == BLACK: return WHITE
        elif player == WHITE: return BLACK

    def find_match(self, board, player, square, direction):
        # HELPER
        # assumes square is blank, looking for existing piece to close bracket
        # returns None if no square exists to close bracket
        opp = self.opponent(player)
        stepD = 1
        sq = board[square+stepD*direction]
        while sq == opp:
            stepD+=1
            sq = board[square+stepD*direction]
        if sq == player and stepD != 1:
            return square+stepD*direction # if possible to close bracket
        return None

    def is_move_valid(self, board, player, move):
        # Is move legal for current player? AKA any possible bracket if that move is made?
        assert (board[move] == EMPTY)   # check is move position empty
        for d in DIRECTIONS:    # check all dirs from move for a bracket
            if self.find_match(board, player, move, d) is not None: # if bracket exists
                return True
        return False

    def make_move(self, board, player, move):   # move is blank space
        # Update board to reflect the move by current player
        # returns a new board/string
        boardList = list(board)
        for d in DIRECTIONS:
            m = self.find_match(board, player, move, d)
            if m is not None:   # AKA if bracket exists in that direction
                for x in range(move, m, d):    # for everything in btwn curr(move) and closing(m); step is direction
                    boardList[x] = player   # changing colors of opponents w/in bracket to player's color
        return "".join(boardList)   # new board w/ updated spots

    def get_valid_moves(self, board, player):
        # Get a list of all legal moves for player
        # For blank squares, check every dir; if match exists in dir, put in list of possible
        possible = []
        blankIndex = [x for x in range(len(board)) if board[x]==EMPTY]
        for b in blankIndex:
            if self.is_move_valid(board, player, b):    # AKA if bracket exists if starting at current blank
                possible.append(b)
        return possible

    def has_any_valid_moves(self, board, player):
        # Can player make any moves?
        return len(self.get_valid_moves(board, player)) > 0 # AKA if at least one possible move

    def next_player(self, board, prev_player):
        # Determines which player should move next?  Returns None if no legal moves exist
        if self.has_any_valid_moves(board, self.opponent(prev_player)): # if next player has a move
            return self.opponent(prev_player)
        else:   # if next player has no move, it's orig player's turn again
            if self.has_any_valid_moves(board, prev_player):
                return prev_player
        return None
    def MAINscorechoose(self, board, player, myMoves):
        count = 64-board.count(".")
        if count < 16:  # beginning of game -- mobility
            return self.mobility_score(board, player, myMoves)
        elif count in range(16, 65):  # middle of game -- weighted positions
            return self.weighted_score(board)
    def mobility_score(self, board, player, myMoves):
        posneg = {BLACK: 1, WHITE: -1}
        opp = self.opponent(player)
        newBoards = [self.make_move(board, player, m) for m in myMoves]
        # oppposs = [self.get_valid_moves(b, opp) for b in newBoards]
        # sum = 0
        # for vm in oppposs:
        #     if len(set(CORNERS).intersection(vm)) == 0: # opponent can't go to corners
        #         sum+=len(vm)
        #     else:
        #         sum+=len(vm)*10
        # return posneg[player] * (1000 - sum)
        oppnumposs = [len(self.get_valid_moves(b, opp)) for b in newBoards]
        # return posneg[player]*(1000-sum(oppnumposs))
        return (sum(oppnumposs))
        # END OFF HERE
    def number_board(self, board):
        VALS = {BLACK:1, WHITE:-1, EMPTY:0, OUTER:0}
        boardList = [VALS[x] for x in board]
        return boardList
    def weighted_score(self, board, player=BLACK):
        boardList = self.number_board(board)
        a = boardList
        b = SCORE_MATRIX
        return sum( [a[x]*b[y] for x in range(len(a)) for y in range(len(b))] )
    def tilescore(self, board, player=BLACK):
        # Compute player's score (number of player's pieces minus opponent's).
        playerNum = board.count(player)
        oppNum = board.count(self.opponent(player))
        return playerNum-oppNum

    def game_over(self, board, player):
        # Return true if player and opponent have no valid moves
        if self.next_player(board, player) is None:
            return True
        return False

    ### Monitoring players

    class IllegalMoveError(Exception):
        def __init__(self, player, move, board):
            self.player = player
            self.move = move
            self.board = board

        def __str__(self):
            return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

    ################ strategies #################

    def alphabeta_minmax_search(self, node, player, depth, alpha, beta):
        best = {BLACK: max, WHITE: min}
        # posneg = {BLACK: 1, WHITE: -1}
        board = node.board
        my_moves = self.get_valid_moves(board, player)
        # their_moves = self.get_valid_moves(board, self.opponent(player))
        if depth == 0:  # score the node and return it
            node.score = self.MAINscorechoose(board, player, my_moves)
            return node
        children = []
        for m in my_moves:
            next_board = self.make_move(board, player, m)
            next_player = self.next_player(next_board, player)
            if next_player is None: # AKA if game over
                c = Node(next_board, move = m, score = 1000*self.tilescore(next_board)) # want largest tile margin at end of game
                children.append(c)
            else:   # AKA if game still going
                c = Node(next_board, move = m)
                c.score = self.alphabeta_minmax_search(c, next_player, depth-1, alpha, beta).score
                children.append(c)
            kid = children[-1]
            if player == BLACK:
                if kid.score > alpha:   alpha = kid.score
            elif player == WHITE:
                if kid.score < beta:    beta = kid.score
            if alpha > beta: break
            if m in CORNERS:    return c
        winner = best[player](children)
        node.score = winner.score
        return winner

    def alphabeta_minmax_strategy(self, board, player, depth=3):  # calls minmax_search; returns an integer move
        n = Node(board)
        newN = self.alphabeta_minmax_search(n, player, depth, -100000, 100000)
        return newN

    def corner_random_strategy(self, board, player):
        moves = self.get_valid_moves(board, player)
        for m in moves:
            if m in CORNERS:    return m
        return random.choice(moves)

    def best_strategy(self, board, player, best_move, running):
        ## THIS IS the public function you must implement
        ## Run your best search in a loop and update best_move.value
        while (True):
            if running.value:
                n = 15
                # best_move.value = self.corner_random_strategy(board, player)
                best_move.value = self.alphabeta_minmax_strategy(board, player).move
                if board.count('.') < n:
                    best_move.value = self.alphabeta_minmax_strategy(board, player, depth=65).move

    # standard_strategy = random_strategy # may need to change this
    standard_strategy = alphabeta_minmax_strategy

######################################################################################################

def main():
    s = Strategy()
    # test: ...........................OX......XO........................... X
    #       X...X...OOOOO..X.OXOO.X..XXOXXOX.OOXXXX..OOXXXXX..OOXXX...X.X.X. O
    #       ...oooooox.xoooooxxxxooooxoxxxoooxxxxooooxxoxooooxxxxxoooooooooo o
    board8 = sys.argv[1].upper()
    player = sys.argv[2].upper()
    if player == "X":   player = BLACK
    elif player == "O": player = WHITE
    board10 = s.convert_size8_to_size10(board8)

    print()
    # 2D representation of board
    print(s.get_pretty_board(board8))

    # list of possible moves
    print()
    possMovesList = [str(s.convert_index10_to_index8(x)) for x in s.get_valid_moves(board10, player)]
    possMovesStr = " ".join(possMovesList)
    print("Possible moves", possMovesStr)

    # chooseMove = s.convert_index10_to_index8(s.corner_random_strategy(board10, player))
    chooseMove = s.convert_index10_to_index8(s.alphabeta_minmax_strategy(board10, player).move)
    print("My heuristic choice is", chooseMove)

    # run minimax for full tree if there's less than n spaces left on board
    n = 15
    if board10.count('.') < n:
        node = s.alphabeta_minmax_strategy(board10, player, depth=65)
        move = s.convert_index10_to_index8(node.move)
        if player == BLACK:
            print("Minimax", int(node.score/1000), move)
        elif player == WHITE:
            print("Minimax", -1*int(node.score/1000), move)

if __name__ == "__main__":
    main()