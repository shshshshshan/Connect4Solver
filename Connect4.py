from typing import Final
from random import choice as random_choice

player_dict = {
  1: 'X',
  2: 'O'
}

class Solver():
  HEIGHT: Final[int] = 6
  WIDTH: Final[int] = 7
  MAX_MOVES: Final[int] = HEIGHT * WIDTH

  def __init__(self, board, protagonist, antagonist, max_depth, current_columns, win_conditions):
    self.board = board
    self.protagonist = protagonist
    self.antagonist = antagonist
    self.max_depth = max_depth
    self.current_columns = current_columns
    self.win_conditions = win_conditions

  def solve(self):
    move = self.__minimaxMove()
    return move

  def __minimaxMove(self):
    moves = self.__minimax(self.board)
    best_moves = [move for move, score in moves[1].items() if score == moves[0]]

    return random_choice(best_moves)

  def __minimax(self, board, depth = 0, alpha = float('-inf'), beta = float('inf')):
    if (depth == self.max_depth or self.__terminal(board)):
      points = self.__evaluate(board)

      return points, None
    
    current_player = self.__turn(board)

    if current_player == self.protagonist:
      best_score = float('-inf')
      legal_moves = self.__get_legal_moves(board)
      best_moves = {}

      for move in legal_moves:
        future_board = self.__future(board, move, self.protagonist)
        score, _ = self.__minimax(future_board, depth=depth + 1, alpha=alpha, beta=beta)

        if score >= best_score:
          best_score = score
          best_moves[move] = score

        alpha = max(alpha, best_score)

        if alpha > beta:
          break

      return best_score, best_moves
    
    if current_player == self.antagonist:
      worst_score = float('inf')
      legal_moves = self.__get_legal_moves(board)
      worst_moves = {}

      for move in legal_moves:
        future_board = self.__future(board, move, self.antagonist)
        score, _ = self.__minimax(future_board, depth=depth + 1, alpha=alpha, beta=beta)

        if score <= worst_score:
          worst_score = score
          worst_moves[move] = score

        beta = min(beta, worst_score)

        if alpha > beta:
          break

      return worst_score, worst_moves
    
    return 0, None

  def __terminal(self, board):
    return self.__check_win(board, self.protagonist) or self.__check_win(board, self.antagonist) or self.__check_tie(board)
  
  def __check_win(self, board, player):
    for combination in self.win_conditions:
      if all(board[i] == player_dict[player] for i in combination):
        return True
      
    return False
  
  def __check_tie(self, board):
    return ' ' not in board
  
  def __evaluate(self, board):
    points = 0

    if self.__check_win(board, self.protagonist):
      points += 100

    elif self.__check_win(board, self.antagonist):
      points -= 100
    
    return points

  def __turn(self, board):
    return self.antagonist if len([symbol for symbol in board if symbol == ' ']) % 2 == 0 else self.protagonist
  
  def __get_legal_moves(self, board):
    legal = []

    for c in range(Solver.WIDTH):
      if board[c] == ' ':
        legal.append(c)

    return legal
  
  def __future(self, board, move, player):
    copyboard = [symbol for symbol in board]

    for i in range(Solver.HEIGHT):
      if board[(i * Solver.WIDTH) + move] != ' ':
        copyboard[((i - 1) * Solver.WIDTH) + move] = player_dict[player]
        break
      elif board[(i * Solver.WIDTH) + move] == ' ' and i == Solver.HEIGHT - 1:
        copyboard[(i * Solver.WIDTH) + move] = player_dict[player]
        break

    return copyboard
  
  def __print_board(self, board):
    board_str = ''

    for i, symbol in enumerate(board):
      board_str += symbol + '\t' if symbol != ' ' else str(i) + '\t'

      if (i + 1) % Solver.WIDTH == 0:
        board_str += '\n'

    with open('logs.txt', 'a') as f:
      f.writelines(board_str)

    print(board_str)

  def __log_board(self, board, info, value):
    board_str = ''

    for i, symbol in enumerate(board):
      board_str += symbol + '\t' if symbol != ' ' else str(i) + '\t'

      if (i + 1) % Solver.WIDTH == 0:
        board_str += '\n'

    with open('logs.txt', 'a') as f:
      f.writelines(f'{info}: ' + str(value) + '\n')
      f.writelines(board_str + '\n')