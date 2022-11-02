import chess
import chess.engine
import time
import chess.svg
from IPython.display import SVG, display

engine = chess.engine.SimpleEngine.popen_uci(
    r"C:\Users\anton\OneDrive\Документи\KPI\3 курс\1 semester\ПІІС\piisLabs\lab3\chess\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")


def stockfish_eval(board_instance, isMax):
    info = engine.analyse(board_instance, chess.engine.Limit(depth=1))

    if not isMax:
        result = chess.engine.PovScore(info['score'], chess.BLACK).pov(chess.BLACK).relative.score()
    else:
        result = chess.engine.PovScore(info['score'], chess.WHITE).pov(chess.WHITE).relative.score()
    # print(result)
    if result is None:
        result = 0
    return result


def best_move_using_negaMax(board_instance, depth):
    def negaMax(board, depth, is_max):
        if depth == 0:
            return stockfish_eval(board, is_max)

        maxValueIn = -1_000_000
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            boardCopy = board.copy()
            boardCopy.push(move)
            value = -negaMax(boardCopy, depth - 1, 1 - is_max)
            if value > maxValueIn:
                maxValueIn = value
        return maxValueIn

    maxValue = -1_000_000
    bestMove = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        boardCopy = board_instance.copy()
        boardCopy.push(move)
        value = -negaMax(boardCopy, depth, 1 - boardCopy.turn)
        if value > maxValue:
            maxValue = value
            bestMove = move
    return bestMove


def best_move_using_negaScout(board_instance, depth, alpha=-999999, beta=999999):
    def negaScout(board, depthIn, alphaIn, betaIn):
        if depthIn == 0:
            return stockfish_eval(board, board.turn)
        scoreIn = -1_000_000
        n = betaIn
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            boardCopy = board.copy()
            boardCopy.push(move)
            cur = -negaScout(boardCopy, depthIn - 1, -n, -alphaIn)
            if cur > scoreIn:
                if n == beta or depthIn <= 2:
                    scoreIn = cur
                else:
                    scoreIn = -negaScout(boardCopy, depthIn - 1, -betaIn, -cur)
            if scoreIn > alphaIn:
                alphaIn = scoreIn
            if alphaIn >= betaIn:
                return alphaIn
            n = alphaIn + 1
        return scoreIn

    score = -1_000_000
    bestMove = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        boardCopy = board_instance.copy()
        boardCopy.push(move)
        value = -negaScout(boardCopy, depth, alpha, beta)
        if value > score:
            score = value
            bestMove = move

    return bestMove


def best_move_using_pvs(board_instance, depth, alpha=-999999, beta=999999):
    def pvs(board, depthIn, alphaIn, betaIn):
        if depthIn == 0:
            return stockfish_eval(board, board.turn)
        bSearchPvIn = True
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            boardCopy = board.copy()
            boardCopy.push(move)
            if bSearchPvIn:
                cur = -pvs(boardCopy, depthIn - 1, -betaIn, -alphaIn)
            else:
                cur = -pvs(boardCopy, depthIn - 1, -alphaIn - 1, -alphaIn)
                if alphaIn < cur < betaIn:
                    cur = -pvs(boardCopy, depthIn - 1, -betaIn, -alphaIn)
            if cur >= betaIn:
                return betaIn
            if cur > alphaIn:
                alphaIn = cur
                bSearchPvIn = False

        return alphaIn

    score = -1_000_000
    bestMove = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        boardCopy = board_instance.copy()
        boardCopy.push(move)
        value = -pvs(boardCopy, depth, alpha, beta)
        if value > score:
            score = value
            bestMove = move

    return bestMove


def game_between_two_computers_pvs(depth=1):
    board = chess.Board()
    n = 0

    while board.is_checkmate() != True and board.is_fivefold_repetition() != True and board.is_seventyfive_moves() != True:
        start = time.time()
        if n % 2 == 0:
            print("WHITE Turn")
            move = best_move_using_pvs(board, depth)
        else:

            print("BLACK Turn")
            move = best_move_using_pvs(board, depth)
        end = time.time()

        if move == None:
            print("GG, checkmate")
            break

        print("Move in UCI format:", move)
        print("Time taken by Move:", end - start)
        print("Moves taken:", n)
        print("FiveFold", board.is_fivefold_repetition())

        board.push(move)
        # display(SVG(chess.svg.board(board, size=400)))
        print(board)
        print("\n")
        n = n + 1
    if board.is_fivefold_repetition():
        print("GG, fivefold")


def game_between_two_computers_negaScout(depth=1):
    board = chess.Board()
    n = 0

    while board.is_checkmate() != True and board.is_fivefold_repetition() != True and board.is_seventyfive_moves() != True:
        start = time.time()
        if n % 2 == 0:
            print("WHITE Turn")
            move = best_move_using_negaScout(board, depth)
        else:

            print("BLACK Turn")
            move = best_move_using_negaScout(board, depth)
        end = time.time()

        if move == None:
            print("GG, checkmate")
            break

        print("Move in UCI format:", move)
        print("Time taken by Move:", end - start)
        print("Moves taken:", n)
        print("FiveFold", board.is_fivefold_repetition())

        board.push(move)
        # display(SVG(chess.svg.board(board, size=400)))
        print(board)
        print("\n")
        n = n + 1
    if board.is_fivefold_repetition():
        print("GG, fivefold")


def game_between_two_computers_negaMax(depth=1):
    board = chess.Board()
    n = 0

    while board.is_checkmate() != True and board.is_fivefold_repetition() != True and board.is_seventyfive_moves() != True:
        start = time.time()
        if n % 2 == 0:
            print("WHITE Turn")
            move = best_move_using_negaMax(board, depth)
        else:

            print("BLACK Turn")
            move = best_move_using_negaMax(board, depth)
        end = time.time()

        if move == None:
            print("GG, checkmate")
            break

        print("Move in UCI format:", move)
        print("Time taken by Move:", end - start)
        print("Moves taken:", n)
        print("FiveFold", board.is_fivefold_repetition())

        board.push(move)
        # display(SVG(chess.svg.board(board, size=400)))
        print(board)
        print("\n")
        n = n + 1
    if board.is_fivefold_repetition():
        print("GG, fivefold")


if __name__ == '__main__':
    # game_between_two_computers_negaMax()
    # game_between_two_computers_negaScout()
    game_between_two_computers_pvs()
    engine.quit()
