import chess
import chess.engine
import uci
import multiprocessing
import random
import threading
import logging

class Engine:
    def __init__(self):
        pass

    def getMove(self, fen):
        board = chess.Board(fen)
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves).uci()



def main():
    uci_thread = threading.Thread(target=uci.main())
    uci_thread.start()





if __name__ == "__main__":
    main()
else:
    pass
