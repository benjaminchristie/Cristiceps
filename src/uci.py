#!/usr/bin/env pypy -u
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import importlib
import re
import sys
import time
import logging
import argparse

import tools
#import sunfish
import customEngine

from tools import WHITE, BLACK, Unbuffered

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('module', help='chessEngine.py file (without .py)', type=str, default='crapbox', nargs='?')
    args = parser.parse_args()
    ''' look at this later
    sunfish = importlib.import_module(args.module)
    if args.tables is not None:
        pst_module = importlib.import_module(args.tables)
        sunfish.pst = pst_module.pst

    logging.basicConfig(filename='sunfish.log', level=logging.DEBUG)
    '''
    out = Unbuffered(sys.stdout)

    def output(line):
        print(line)
        #print(line, file=out)
        #logging.debug(line)
    pos = tools.parseFEN(tools.FEN_INITIAL)
    '''
    searcher = sunfish.Searcher()
    '''
    color = WHITE
    our_time, opp_time = 1000, 1000 # time in centi-seconds
    show_thinking = False

    stack = []
    while True:
        if stack:
            smove = stack.pop()
        else:
            smove = input()

        logging.debug(f'>>> {smove} ')

        if smove == 'quit':
            break

        elif smove == 'uci':
            output('id name Crapbox')
            output('id author Benjamin Christie')
            output('uciok')

        elif smove == 'isready':
            output('readyok')

        elif smove == 'ucinewgame':
            stack.append('position fen ' + tools.FEN_INITIAL)

        # syntax specified in UCI
        # position [fen  | startpos ]  moves  ....

        elif smove.startswith('position'):
            params = smove.split(' ')
            idx = smove.find('moves')

            if idx >= 0:
                moveslist = smove[idx:].split()[1:]
            else:
                moveslist = []

            if params[1] == 'fen':
                if idx >= 0:
                    fenpart = smove[:idx]
                else:
                    fenpart = smove

                _, _, fen = fenpart.split(' ', 2)

            elif params[1] == 'startpos':
                fen = tools.FEN_INITIAL
            else:
                pass

            pos = tools.parseFEN(fen)
            color = WHITE if fen.split()[1] == 'w' else BLACK

            for move in moveslist:
                pos = pos.move(tools.mparse(color, move))
                color = 1 - color

        elif smove.startswith('go'):
            #  default options
            depth = 1000
            movetime = -1

            _, *params = smove.split(' ')
            for param, val in zip(*2*(iter(params),)):
                if param == 'depth':
                    depth = int(val)
                if param == 'movetime':
                    movetime = int(val)
                if param == 'wtime':
                    our_time = int(val)
                if param == 'btime':
                    opp_time = int(val)

            moves_remain = 40

            start = time.time()
            ponder = None
            renderedFen = tools.renderFEN(pos)
            eng = customEngine.Engine()
            currMove = str(eng.getMove(renderedFen))
            output("info currmove " + currMove)
            time.sleep(0.1)
            output("bestmove " + currMove)
            '''
            if sdepth >= depth:
                break
            '''

        elif smove.startswith('stop'):
            output("bestmove " + currMove)
        elif smove.startswith('time'):
            our_time = int(smove.split()[1])

        elif smove.startswith('otim'):
            opp_time = int(smove.split()[1])

        else:
            pass

if __name__ == '__main__':
    main()
