'''
Cristiceps australis, the crested weedfish, is a species of clinid.

This fish HIGH ON WEED, probably Stockfish's cousin

'''
import customEngine
import chess
import minimax
import uci

class CristicepsEngine(customEngine.Engine):

    def __init__(self, depth=5, engineColor=chess.BLACK):
        self.depth = depth
        self.engineColor = engineColor
        self.PST = customEngine.Engine.PST
        self.board = chess.Board()

    def getMove(self, fen):
        root = chess.pgn.Game()
        root.setup(chess.Board(fen))
        mm = minimax.MiniMax(engine=self)
        return mm.minimaxRoot(self.depth, root.board(), True)


    def play(self):
        uci.main(self)


def main():
    cs = CristicepsEngine(engineColor=chess.WHITE)
    print('ok to play')
    cs.play()
main()
