'''
Cristiceps australis, the crested weedfish, is a species of clinid.

This fish HIGH ON WEED, probably Stockfish's cousin

'''
import customEngine
from customEngine import Engine
import chess
import chess.pgn
# from minimax import MiniMax
import uci
import re
import os
import math
class CristicepsEngine(customEngine.Engine):

    def __init__(self, depth=5, engineColor=chess.BLACK):
        self.depth = depth
        self.engineColor = engineColor
        self.PST = customEngine.Engine.PST
        self.board = chess.Board()

    def getMove(self, fen):
        root = chess.pgn.Game()
        root.setup(chess.Board(fen))
        mm = MiniMax(engine=self, engineColor=self.engineColor)
        return mm.minimaxRoot(self.depth, root.board(), True)


    def play(self):
        uci.main(self)

    def cmdPlay(self):
        board = chess.Board()
        while not board.is_game_over():
            os.system("cls") if os.name=="nt" else os.system("clear")
            print(board)
            move = self.getMoveFromCMD()
            while move not in board.legal_moves:
                print("Enter legal move")
                move = self.getMoveFromCMD()
            board.push(move)
            os.system("cls") if os.name=="nt" else os.system("clear")
            print(board)
            engineMove = self.getMove(board.fen())
            board.push(engineMove)

    def getMoveFromCMD(self):
        move = None
        while move is None:
            match = re.match('([a-h][1-8])'*2, input('Your move: '))
            if match:
                move = chess.Move.from_uci(match.string)
            else:
                # Inform the user when invalid input (e.g. "help") is entered
                print("Please enter a move like g8f6")
        return move

class MiniMax():
    # assuming gametree is a game in
    def __init__(self, engine, engineColor=chess.WHITE, gametree=chess.pgn.Game()):
        self.gametree = gametree
        self.parentNode = gametree.parent
        self.currentNode = None
        self.successors = []
        self.color = engineColor
        self.engine = engine

    def getSuccessorsFromFEN(self, fen):
        node = chess.pgn.Game()
        node.setup(fen)
        legal_moves = node.board().legal_moves
        children = []
        for move in legal_moves:
            newGame = chess.pgn.Game()
            newBoard = newGame.board()
            newBoard.push(move)
            children.append(newBoard.fen())
        return children

    def minimaxRoot(self, depth, board,isMaximizing):
        possibleMoves = board.legal_moves
        bestMove = -999999999999
        bestMoveFinal = None
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            value = max(bestMove, self.minimax(depth - 1, board,-10000,10000, not isMaximizing))
            board.pop()
            if( value > bestMove):
                bestMove = value
                bestMoveFinal = move
                print("info score cp" ,str(bestMove))
                print("info currmove",str(bestMoveFinal))
        return bestMoveFinal

    def minimax(self, depth, board, alpha, beta, is_maximizing):
        if(depth == 0):
            return -self.engine.evaluation(board, self.color)
        possibleMoves = board.legal_moves
        if(is_maximizing):
            bestMove = -999999999999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMove = max(bestMove, self.minimax(depth - 1, board,alpha,beta, not is_maximizing))
                board.pop()
                alpha = max(alpha,bestMove)
                if beta <= alpha:
                    return bestMove
            return bestMove
        else:
            bestMove = 999999999999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMove = min(bestMove, self.minimax(depth - 1, board,alpha,beta, not is_maximizing))
                board.pop()
                beta = min(beta,bestMove)
                if(beta <= alpha):
                    return bestMove
            return bestMove



def main():
    cs = CristicepsEngine(depth=5, engineColor=chess.BLACK)
    print('ok to play')
    cs.cmdPlay()

if __name__=="__main__":
    main()
