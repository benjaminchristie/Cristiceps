import math
import chess
import chess.pgn
from customEngine import Engine
i = 0
class MiniMax:
    # assuming gametree is a game in
    def __init__(self, engine=Engine(), gametree=chess.pgn.Game(), color=chess.WHITE):
        self.gametree = gametree
        self.parentNode = gametree.parent
        self.currentNode = None
        self.successors = []
        self.color = color
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
                print("info score " ,str(bestMove))
                print("info currmove ",str(bestMoveFinal))
        return bestMoveFinal

    def minimax(self, depth, board, alpha, beta, is_maximizing):
        if(depth == 0):
            return -self.engine.evaluation(board)
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
    mm = MiniMax()
    print(mm.minimaxRoot(5, chess.pgn.Game().board(), True))

if __name__=="__main__":
    main()
else:
    pass
