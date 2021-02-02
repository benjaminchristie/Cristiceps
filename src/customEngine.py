import chess
import chess.engine
import uci
import multiprocessing
import random
import threading
import logging
import os

class Engine():
    piece = { 'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000 , '': 0, ' ': 0}
    PST = {
    'B' : [-40, -20, -20, -20, -20, -20, -20, -40 ,
             -20,   0,   0,   0,   0,   0,   0, -20 ,
             -20,   0,  10,  20,  20,  10,   0, -20 ,
             -20,  10,  10,  20,  20,  10,  10, -20 ,
             -20,   0,  20,  20,  20,  20,   0, -20 ,
             -20,  20,  20,  20,  20,  20,  20, -20 ,
             -20,  10,   0,   0,   0,   0,  10, -20 ,
             -40, -20, -20, -20, -20, -20, -20, -40 ],
    'N' : [-20, -80, -60, -60, -60, -60, -80, -20 ,
             -80, -40,   0,   0,   0,   0, -40, -80 ,
             -60,   0,  20,  30,  30,  20,   0, -60 ,
             -60,  10,  30,  40,  40,  30,  10, -60 ,
             -60,   0,  30,  40,  40,  30,   0, -60 ,
             -60,  10,  20,  30,  30,  30,   1, -60 ,
             -80, -40,   0,  10,  10,   0,  -4, -80 ,
             -20, -80, -60, -60, -60, -60, -80, -20 ,],
    'P' : [9000,9000,9000,9000,9000,9000,9000,9000 ,
             200, 200, 200, 200, 200, 200, 200, 200 ,
             100, 100, 100, 100, 100, 100, 100, 100 ,
              40,  40,  90, 100, 100,  90,  40,  40 ,
              20,  20,  20, 100, 150,  20,  20,  20 ,
               2,   4,   0,  15,   4,   0,   4,   2 ,
             -10, -10, -10, -20, -35, -10, -10, -10 ,
               0,   0,   0,   0,   0,   0,   0,   0 ],
    'Q' : [-40, -20, -20, -10, -10, -20, -20, -40 ,
             -20,   0,   0,   0,   0,   0,   0, -20 ,
             -20,   0,  10,  10,  10,  10,   0, -20 ,
             -10,   0,  10,  10,  10,  10,   0, -10 ,
               0,   0,  10,  10,  10,  10,   0, -10 ,
             -20,  10,  10,  10,  10,  10,   0, -20 ,
             -20,   0,  10,   0,   0,   0,   0, -20 ,
             -40, -20, -20, -10, -10, -20, -20, -40 ],
    'R' : [0,  0,  0,  0,  0,  0,  0,   0 ,
              10, 20, 20, 20, 20, 20, 20,  10 ,
             -10,  0,  0,  0,  0,  0,  0, -10 ,
             -10,  0,  0,  0,  0,  0,  0, -10 ,
             -10,  0,  0,  0,  0,  0,  0, -10 ,
             -10,  0,  0,  0,  0,  0,  0, -10 ,
             -10,  0,  0,  0,  0,  0,  0, -10 ,
             -30, 30, 40, 10, 10,  0,  0, -30],
     'K' : [-60, -80, -80, -2, -20, -80, -80, -60,
             -60, -80, -80, -2, -20, -80, -80, -60 ,
             -60, -80, -80, -2, -20, -80, -80, -60 ,
             -60, -80, -80, -2, -20, -80, -80, -60 ,
             -40, -60, -60, -8, -80, -60, -60, -40 ,
             -20, -40, -40, -40,-40, -40, -40, -20 ,
              40,  40,   0,   0,  0,   0,  40,  40 ,
              40,  60,  20,   0,  0,  20,  60,  40 ],
      '' : [0] * 64,
      ' ' : [0] *64
    }

    def __init__(self, engineColor):
        self.engineColor = engineColor

    # position is from 0 to 63, from top left corner
    def evalPiecePosition(self, pieceStr, position, perspectiveColor):
        if pieceStr.isupper() and perspectiveColor == chess.WHITE: # white
            return Engine.piece[pieceStr] * Engine.PST[pieceStr][position]
        elif pieceStr.isupper() and perspectiveColor == chess.BLACK:
            return -Engine.piece[pieceStr] * Engine.PST[pieceStr][position]
        elif pieceStr.islower() and perspectiveColor == chess.WHITE:
            pieceStr = pieceStr.upper()
            return -Engine.piece[pieceStr] * Engine.PST[pieceStr][position]
        else: # black
            pieceStr = pieceStr.upper()
            #position = (position + 56 - int( position / 8 ) * 16)
            return Engine.piece[pieceStr] * Engine.PST[pieceStr][position]

    def evalPosition(self, fen, perspectiveColor):
        eval = 0
        arr = self.fen2array(fen)
        for n in range(len(arr)):
            eval+=self.evalPiecePosition(arr[n], n, perspectiveColor)
        return eval

    def evaluation(self, board, perspectiveColor):
        #os.system("cls") if os.name=="nt" else os.system("clear")
        #print(board)
        return self.evalPosition(board.fen(), perspectiveColor)

    def fen2array(self, fen):
        old_board = fen.split('/')
        new_board = []
        for n in range(7): # row
            row = old_board[n]
            # eigth row will be weird
            for square in row:
                try:
                    spacing = int(square)
                    for c in range(spacing):
                        new_board.append('')
                except:
                    new_board.append(square)
        # handle last row logic
        for n in range(len(old_board[7])):
            square = old_board[7][n]
            if square == ' ':
                break
            try:
                spacing = int(square)
                for c in range(spacing):
                    new_board.append('')
            except:
                new_board.append(square)
        return new_board

    def getRandomMove(self, fen):
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
