# # # import math
# # # from copy import deepcopy
# # # import api

# # # EMPTY = "."
# # # PLAYER_X = "X"
# # # PLAYER_O = "O"


# # # class GeneralizedTicTacToe:
# # #     def __init__(self, n=3, m=3):
# # #         if m > n:
# # #             raise ValueError("Target m cannot be greater than board size n.")
# # #         self.n = n
# # #         self.m = m
# # #         self.board = [[EMPTY for _ in range(n)] for _ in range(n)]
# # #         self.current_player = PLAYER_X

# # #     def clone(self):
# # #         new_game = GeneralizedTicTacToe(self.n, self.m)
# # #         new_game.board = deepcopy(self.board)
# # #         new_game.current_player = self.current_player
# # #         return new_game

# # #     def print_board(self):
# # #         print("\n   " + " ".join(f"{i:2}" for i in range(self.n)))
# # #         for i, row in enumerate(self.board):
# # #             print(f"{i:2} " + " ".join(f"{cell:2}" for cell in row))
# # #         print()

# # #     def available_moves(self):
# # #         return [
# # #             (r, c)
# # #             for r in range(self.n)
# # #             for c in range(self.n)
# # #             if self.board[r][c] == EMPTY
# # #         ]

# # #     def make_move(self, row, col, player=None):
# # #         if not (0 <= row < self.n and 0 <= col < self.n):
# # #             return False

# # #         if player is None:
# # #             player = self.current_player

# # #         if self.board[row][col] != EMPTY:
# # #             return False

# # #         self.board[row][col] = player
# # #         self.current_player = PLAYER_O if player == PLAYER_X else PLAYER_X
# # #         return True

# # #     def undo_move(self, row, col, previous_player):
# # #         self.board[row][col] = EMPTY
# # #         self.current_player = previous_player

# # #     def is_full(self):
# # #         return all(
# # #             self.board[r][c] != EMPTY
# # #             for r in range(self.n)
# # #             for c in range(self.n)
# # #         )

# # #     def check_winner(self):
# # #         directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

# # #         for r in range(self.n):
# # #             for c in range(self.n):
# # #                 if self.board[r][c] == EMPTY:
# # #                     continue

# # #                 symbol = self.board[r][c]

# # #                 for dr, dc in directions:
# # #                     count = 1
# # #                     nr, nc = r + dr, c + dc

# # #                     while (
# # #                         0 <= nr < self.n
# # #                         and 0 <= nc < self.n
# # #                         and self.board[nr][nc] == symbol
# # #                     ):
# # #                         count += 1
# # #                         if count >= self.m:
# # #                             return symbol
# # #                         nr += dr
# # #                         nc += dc

# # #         return None

# # #     def is_terminal(self):
# # #         winner = self.check_winner()
# # #         if winner is not None:
# # #             return True, winner
# # #         if self.is_full():
# # #             return True, "DRAW"
# # #         return False, None

# # #     def get_all_length_m_segments(self):
# # #         segments = []

# # #         # Rows
# # #         for r in range(self.n):
# # #             for c in range(self.n - self.m + 1):
# # #                 segments.append([(r, c + i) for i in range(self.m)])

# # #         # Columns
# # #         for c in range(self.n):
# # #             for r in range(self.n - self.m + 1):
# # #                 segments.append([(r + i, c) for i in range(self.m)])

# # #         # Main diagonals
# # #         for r in range(self.n - self.m + 1):
# # #             for c in range(self.n - self.m + 1):
# # #                 segments.append([(r + i, c + i) for i in range(self.m)])

# # #         # Anti-diagonals
# # #         for r in range(self.n - self.m + 1):
# # #             for c in range(self.m - 1, self.n):
# # #                 segments.append([(r + i, c - i) for i in range(self.m)])

# # #         return segments

# # #     def human_vs_ai(self, ai_symbol=PLAYER_O, depth=3):
# # #         ai = MinimaxAgent(ai_symbol, max_depth=depth)
# # #         human = PLAYER_X if ai_symbol == PLAYER_O else PLAYER_O

# # #         print(f"\nGame {self.n}x{self.n}, target={self.m}")
# # #         print(f"You are {human}, AI is {ai_symbol}\n")

# # #         while True:
# # #             self.print_board()

# # #             terminal, winner = self.is_terminal()
# # #             if terminal:
# # #                 if winner == "DRAW":
# # #                     print("Draw!")
# # #                 else:
# # #                     print(f"Winner: {winner}")
# # #                 break

# # #             if self.current_player == human:
# # #                 try:
# # #                     r, c = map(int, input("Enter row col: ").split())
# # #                 except ValueError:
# # #                     print("Invalid input. Please enter: row col")
# # #                     continue

# # #                 if not self.make_move(r, c, human):
# # #                     print("Invalid move")
# # #             else:
# # #                 move = ai.choose_move(self)
# # #                 if move is None:
# # #                     print("No valid move found.")
# # #                     break
# # #                 print(f"AI plays: {move}")
# # #                 self.make_move(move[0], move[1], ai_symbol)
    
# # #     def ai_vs_online(self, team_id_1, team_id_2, game_id, depth=2):
# # #         import time
# # #         import api

# # #         ai_symbol = None
# # #         opponent = None
# # #         ai = None

# # #         print(f"\nConnected to game {game_id}\n")

# # #         while True:
# # #             # -------------------------
# # #             # 1. GET GAME DETAILS
# # #             # -------------------------
# # #             details = api.get_game_details(game_id)
# # #             game_info = details["game"]

# # #             status = game_info.get("status")
# # #             turn_team_id = str(game_info.get("turnteamid"))
# # #             winner_team_id = game_info.get("winnerteamid")

# # #             # -------------------------
# # #             # 2. STOP IF GAME FINISHED (SERVER SIDE)
# # #             # -------------------------
# # #             if status != "O":
# # #                 self.print_board()
# # #                 print("\nGame finished!")

# # #                 if winner_team_id is None:
# # #                     print("Result: DRAW")
# # #                 elif str(winner_team_id) == str(team_id_1):
# # #                     print("You WIN 🎉")
# # #                 else:
# # #                     print("You LOSE ❌")

# # #                 break

# # #             # -------------------------
# # #             # 3. SYNC FULL BOARD FROM SERVER
# # #             # -------------------------
# # #             moves = api.get_moves(game_id, "300")

# # #             self.board = [[EMPTY for _ in range(self.n)] for _ in range(self.n)]

# # #             for mv in moves:
# # #                 r, c = map(int, mv["move"].split(","))
# # #                 symbol = mv["symbol"]

# # #                 if 0 <= r < self.n and 0 <= c < self.n:
# # #                     self.board[r][c] = symbol

# # #             # -------------------------
# # #             # 4. STOP IF GAME FINISHED (LOCAL CHECK)
# # #             # -------------------------
# # #             terminal, winner = self.is_terminal()
# # #             if terminal:
# # #                 self.print_board()
# # #                 print("\nGame finished!")

# # #                 if winner == "DRAW":
# # #                     print("Result: DRAW")
# # #                 else:
# # #                     print(f"Winner: {winner}")

# # #                 break

# # #             # -------------------------
# # #             # 5. DETERMINE SYMBOLS ONCE
# # #             # -------------------------
# # #             if ai_symbol is None:
# # #                 if moves:
# # #                     last_move = moves[-1]
# # #                     last_team = str(last_move["teamId"])
# # #                     last_symbol = last_move["symbol"]

# # #                     if last_team == str(team_id_1):
# # #                         ai_symbol = last_symbol
# # #                         opponent = PLAYER_O if ai_symbol == PLAYER_X else PLAYER_X
# # #                     else:
# # #                         opponent = last_symbol
# # #                         ai_symbol = PLAYER_O if opponent == PLAYER_X else PLAYER_X
# # #                 else:
# # #                     # no moves yet: team1 starts as X, team2 as O
# # #                     if str(team_id_1) == str(game_info["team1id"]):
# # #                         ai_symbol = PLAYER_X
# # #                         opponent = PLAYER_O
# # #                     else:
# # #                         ai_symbol = PLAYER_O
# # #                         opponent = PLAYER_X

# # #                 ai = MinimaxAgent(ai_symbol, max_depth=depth)
# # #                 print(f"AI is {ai_symbol}, Opponent is {opponent}\n")

# # #             self.print_board()

# # #             # -------------------------
# # #             # 6. WAIT IF NOT YOUR TURN
# # #             # -------------------------
# # #             if turn_team_id != str(team_id_1):
# # #                 print("Waiting for opponent move...\n")
# # #                 time.sleep(2)
# # #                 continue

# # #             # -------------------------
# # #             # 7. YOUR TURN -> AI PLAYS
# # #             # -------------------------
# # #             move = ai.choose_move(self)

# # #             if move is None:
# # #                 print("No valid move available.")
# # #                 break

# # #             if self.board[move[0]][move[1]] != EMPTY:
# # #                 print("Invalid move (already occupied):", move)
# # #                 time.sleep(2)
# # #                 continue

# # #             print("AI plays:", move)

# # #             try:
# # #                 api.make_move(game_id, team_id_1, f"{move[0]},{move[1]}")
# # #             except Exception as e:
# # #                 print("Move failed:", e)
# # #                 time.sleep(2)
# # #                 continue

# # #             # update local board only after successful API submission
# # #             self.make_move(move[0], move[1], ai_symbol)

# # #             # small delay to avoid excessive polling
# # #             time.sleep(2)
# # # class MinimaxAgent:
# # #     def __init__(self, player_symbol, max_depth=3):
# # #         self.player = player_symbol
# # #         self.opponent = PLAYER_O if player_symbol == PLAYER_X else PLAYER_X
# # #         self.max_depth = max_depth

# # #     def choose_move(self, game):
# # #         best_score = -math.inf
# # #         best_move = None

# # #         moves = self.order_moves(game, game.available_moves())

# # #         for r, c in moves:
# # #             previous_player = game.current_player
# # #             game.make_move(r, c, self.player)

# # #             score = self.minimax(
# # #                 game=game,
# # #                 depth=self.max_depth - 1,
# # #                 alpha=-math.inf,
# # #                 beta=math.inf,
# # #                 maximizing=False,
# # #             )

# # #             game.undo_move(r, c, previous_player)

# # #             if score > best_score:
# # #                 best_score = score
# # #                 best_move = (r, c)

# # #         return best_move

# # #     def minimax(self, game, depth, alpha, beta, maximizing):
# # #         terminal, winner = game.is_terminal()
# # #         if terminal:
# # #             if winner == self.player:
# # #                 return 1_000_000
# # #             if winner == self.opponent:
# # #                 return -1_000_000
# # #             return 0

# # #         if depth == 0:
# # #             return self.evaluate(game)

# # #         if maximizing:
# # #             value = -math.inf
# # #             for r, c in self.order_moves(game, game.available_moves()):
# # #                 previous_player = game.current_player
# # #                 game.make_move(r, c, self.player)

# # #                 value = max(
# # #                     value,
# # #                     self.minimax(game, depth - 1, alpha, beta, False)
# # #                 )

# # #                 game.undo_move(r, c, previous_player)
# # #                 alpha = max(alpha, value)
# # #                 if beta <= alpha:
# # #                     break

# # #             return value

# # #         value = math.inf
# # #         for r, c in self.order_moves(game, game.available_moves()):
# # #             previous_player = game.current_player
# # #             game.make_move(r, c, self.opponent)

# # #             value = min(
# # #                 value,
# # #                 self.minimax(game, depth - 1, alpha, beta, True)
# # #             )

# # #             game.undo_move(r, c, previous_player)
# # #             beta = min(beta, value)
# # #             if beta <= alpha:
# # #                 break

# # #         return value

# # #     def evaluate(self, game):
# # #         winner = game.check_winner()
# # #         if winner == self.player:
# # #             return 1_000_000
# # #         if winner == self.opponent:
# # #             return -1_000_000

# # #         score = 0

# # #         for segment in game.get_all_length_m_segments():
# # #             cells = [game.board[r][c] for r, c in segment]
# # #             player_count = cells.count(self.player)
# # #             opponent_count = cells.count(self.opponent)
# # #             empty_count = cells.count(EMPTY)

# # #             # Blocked line
# # #             if player_count > 0 and opponent_count > 0:
# # #                 continue

# # #             # Useful for AI
# # #             if player_count > 0 and opponent_count == 0:
# # #                 score += self.segment_score(player_count, empty_count)

# # #             # Dangerous for AI
# # #             elif opponent_count > 0 and player_count == 0:
# # #                 score -= self.segment_score(opponent_count, empty_count)

# # #         score += self.center_control_bonus(game)
# # #         return score

# # #     def segment_score(self, marks, empties):
# # #         return (10 ** marks) + empties

# # #     def center_control_bonus(self, game):
# # #         center = (game.n - 1) / 2
# # #         bonus = 0

# # #         for r in range(game.n):
# # #             for c in range(game.n):
# # #                 cell = game.board[r][c]
# # #                 if cell == EMPTY:
# # #                     continue

# # #                 dist = abs(r - center) + abs(c - center)
# # #                 value = max(0, game.n - dist)

# # #                 if cell == self.player:
# # #                     bonus += value
# # #                 elif cell == self.opponent:
# # #                     bonus -= value

# # #         return bonus

# # #     def order_moves(self, game, moves):
# # #         center = (game.n - 1) / 2

# # #         def neighbor_count(r, c):
# # #             count = 0
# # #             for dr in (-1, 0, 1):
# # #                 for dc in (-1, 0, 1):
# # #                     if dr == 0 and dc == 0:
# # #                         continue
# # #                     nr, nc = r + dr, c + dc
# # #                     if 0 <= nr < game.n and 0 <= nc < game.n:
# # #                         if game.board[nr][nc] != EMPTY:
# # #                             count += 1
# # #             return count

# # #         return sorted(
# # #             moves,
# # #             key=lambda move: (
# # #                 -neighbor_count(move[0], move[1]),
# # #                 abs(move[0] - center) + abs(move[1] - center),
# # #             ),
# # #         )

# # import math
# # from copy import deepcopy
# # import time
# # import api

# # EMPTY = "."
# # PLAYER_X = "X"
# # PLAYER_O = "O"


# # class GeneralizedTicTacToe:
# #     def __init__(self, n=3, m=3):
# #         if m > n:
# #             raise ValueError("Target m cannot be greater than board size n.")
# #         self.n = n
# #         self.m = m
# #         self.board = [[EMPTY for _ in range(n)] for _ in range(n)]
# #         self.current_player = PLAYER_X

# #     def clone(self):
# #         new_game = GeneralizedTicTacToe(self.n, self.m)
# #         new_game.board = deepcopy(self.board)
# #         new_game.current_player = self.current_player
# #         return new_game

# #     def print_board(self):
# #         print("\n   " + " ".join(f"{i:2}" for i in range(self.n)))
# #         for i, row in enumerate(self.board):
# #             print(f"{i:2} " + " ".join(f"{cell:2}" for cell in row))
# #         print()

# #     def available_moves(self):
# #         return [
# #             (r, c)
# #             for r in range(self.n)
# #             for c in range(self.n)
# #             if self.board[r][c] == EMPTY
# #         ]

# #     def make_move(self, row, col, player=None):
# #         if not (0 <= row < self.n and 0 <= col < self.n):
# #             return False

# #         if player is None:
# #             player = self.current_player

# #         if self.board[row][col] != EMPTY:
# #             return False

# #         self.board[row][col] = player
# #         self.current_player = PLAYER_O if player == PLAYER_X else PLAYER_X
# #         return True

# #     def undo_move(self, row, col, previous_player):
# #         self.board[row][col] = EMPTY
# #         self.current_player = previous_player

# #     def is_full(self):
# #         return all(
# #             self.board[r][c] != EMPTY
# #             for r in range(self.n)
# #             for c in range(self.n)
# #         )

# #     def check_winner(self):
# #         directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

# #         for r in range(self.n):
# #             for c in range(self.n):
# #                 if self.board[r][c] == EMPTY:
# #                     continue

# #                 symbol = self.board[r][c]

# #                 for dr, dc in directions:
# #                     count = 1
# #                     nr, nc = r + dr, c + dc

# #                     while (
# #                         0 <= nr < self.n
# #                         and 0 <= nc < self.n
# #                         and self.board[nr][nc] == symbol
# #                     ):
# #                         count += 1
# #                         if count >= self.m:
# #                             return symbol
# #                         nr += dr
# #                         nc += dc

# #         return None

# #     def is_terminal(self):
# #         winner = self.check_winner()
# #         if winner is not None:
# #             return True, winner
# #         if self.is_full():
# #             return True, "DRAW"
# #         return False, None

# #     def get_all_length_m_segments(self):
# #         segments = []

# #         # Rows
# #         for r in range(self.n):
# #             for c in range(self.n - self.m + 1):
# #                 segments.append([(r, c + i) for i in range(self.m)])

# #         # Columns
# #         for c in range(self.n):
# #             for r in range(self.n - self.m + 1):
# #                 segments.append([(r + i, c) for i in range(self.m)])

# #         # Main diagonals
# #         for r in range(self.n - self.m + 1):
# #             for c in range(self.n - self.m + 1):
# #                 segments.append([(r + i, c + i) for i in range(self.m)])

# #         # Anti-diagonals
# #         for r in range(self.n - self.m + 1):
# #             for c in range(self.m - 1, self.n):
# #                 segments.append([(r + i, c - i) for i in range(self.m)])

# #         return segments

# #     def human_vs_ai(self, ai_symbol=PLAYER_O, depth=4):
# #         ai = MinimaxAgent(ai_symbol, max_depth=depth)
# #         human = PLAYER_X if ai_symbol == PLAYER_O else PLAYER_O

# #         print(f"\nGame {self.n}x{self.n}, target={self.m}")
# #         print(f"You are {human}, AI is {ai_symbol}\n")

# #         while True:
# #             self.print_board()

# #             terminal, winner = self.is_terminal()
# #             if terminal:
# #                 if winner == "DRAW":
# #                     print("Draw!")
# #                 else:
# #                     print(f"Winner: {winner}")
# #                 break

# #             if self.current_player == human:
# #                 try:
# #                     r, c = map(int, input("Enter row col: ").split())
# #                 except ValueError:
# #                     print("Invalid input. Please enter: row col")
# #                     continue

# #                 if not self.make_move(r, c, human):
# #                     print("Invalid move")
# #             else:
# #                 move = ai.choose_move(self)
# #                 if move is None:
# #                     print("No valid move found.")
# #                     break
# #                 print(f"AI plays: {move}")
# #                 self.make_move(move[0], move[1], ai_symbol)

# #     def ai_vs_online(self, team_id_1, team_id_2, game_id, depth=4):
# #         ai_symbol = None
# #         opponent = None
# #         ai = None

# #         print(f"\nConnected to game {game_id}\n")

# #         while True:
# #             details = api.get_game_details(game_id)
# #             game_info = details["game"]

# #             status = game_info.get("status")
# #             turn_team_id = str(game_info.get("turnteamid"))
# #             winner_team_id = game_info.get("winnerteamid")

# #             if status != "O":
# #                 self.print_board()
# #                 print("\nGame finished!")

# #                 if winner_team_id is None:
# #                     print("Result: DRAW")
# #                 elif str(winner_team_id) == str(team_id_1):
# #                     print("You WIN")
# #                 else:
# #                     print("You LOSE")

# #                 break

# #             moves = api.get_moves(game_id, "300")
# #             self.board = [[EMPTY for _ in range(self.n)]
# #                           for _ in range(self.n)]

# #             for mv in moves:
# #                 r, c = map(int, mv["move"].split(","))
# #                 symbol = mv["symbol"]
# #                 if 0 <= r < self.n and 0 <= c < self.n:
# #                     self.board[r][c] = symbol

# #             terminal, winner = self.is_terminal()
# #             if terminal:
# #                 self.print_board()
# #                 print("\nGame finished!")

# #                 if winner == "DRAW":
# #                     print("Result: DRAW")
# #                 else:
# #                     print(f"Winner: {winner}")
# #                 break

# #             if ai_symbol is None:
# #                 if moves:
# #                     last_move = moves[-1]
# #                     last_team = str(last_move["teamId"])
# #                     last_symbol = last_move["symbol"]

# #                     if last_team == str(team_id_1):
# #                         ai_symbol = last_symbol
# #                         opponent = PLAYER_O if ai_symbol == PLAYER_X else PLAYER_X
# #                     else:
# #                         opponent = last_symbol
# #                         ai_symbol = PLAYER_O if opponent == PLAYER_X else PLAYER_X
# #                 else:
# #                     if str(team_id_1) == str(game_info["team1id"]):
# #                         ai_symbol = PLAYER_X
# #                         opponent = PLAYER_O
# #                     else:
# #                         ai_symbol = PLAYER_O
# #                         opponent = PLAYER_X

# #                 ai = MinimaxAgent(ai_symbol, max_depth=depth)
# #                 print(f"AI is {ai_symbol}, Opponent is {opponent}\n")

# #             if ai_symbol is not None and opponent is not None:
# #                 if turn_team_id == str(team_id_1):
# #                     self.current_player = ai_symbol
# #                 else:
# #                     self.current_player = opponent

# #             self.print_board()

# #             if turn_team_id != str(team_id_1):
# #                 print("Waiting for opponent move...\n")
# #                 time.sleep(2)
# #                 continue

# #             move = ai.choose_move(self)

# #             if move is None:
# #                 print("No valid move available.")
# #                 break

# #             if self.board[move[0]][move[1]] != EMPTY:
# #                 print("Invalid move (already occupied):", move)
# #                 time.sleep(2)
# #                 continue

# #             print("AI plays:", move)

# #             try:
# #                 api.make_move(game_id, team_id_1, f"{move[0]},{move[1]}")
# #             except Exception as e:
# #                 print("Move failed:", e)
# #                 time.sleep(2)
# #                 continue

# #             self.make_move(move[0], move[1], ai_symbol)
# #             time.sleep(2)


# # class MinimaxAgent:
# #     def __init__(self, player_symbol, max_depth=4):
# #         self.player = player_symbol
# #         self.opponent = PLAYER_O if player_symbol == PLAYER_X else PLAYER_X
# #         self.max_depth = max_depth
# #         self.transposition = {}

# #     def choose_move(self, game):
# #         self.transposition.clear()

# #         win_move = self.find_immediate_win(game, self.player)
# #         if win_move is not None:
# #             return win_move

# #         block_move = self.find_immediate_win(game, self.opponent)
# #         if block_move is not None:
# #             return block_move

# #         best_score = -math.inf
# #         best_move = None

# #         moves = self.order_moves(game, self.get_candidate_moves(game))

# #         for r, c in moves:
# #             previous_player = game.current_player
# #             game.make_move(r, c, self.player)

# #             score = self.minimax(
# #                 game=game,
# #                 depth=self.max_depth - 1,
# #                 alpha=-math.inf,
# #                 beta=math.inf,
# #                 maximizing=False,
# #             )

# #             game.undo_move(r, c, previous_player)

# #             if score > best_score:
# #                 best_score = score
# #                 best_move = (r, c)

# #         return best_move

# #     def minimax(self, game, depth, alpha, beta, maximizing):
# #         key = self.board_key(game, depth, maximizing)
# #         if key in self.transposition:
# #             return self.transposition[key]

# #         terminal, winner = game.is_terminal()
# #         if terminal:
# #             if winner == self.player:
# #                 return 1_000_000
# #             if winner == self.opponent:
# #                 return -1_000_000
# #             return 0

# #         if depth == 0:
# #             value = self.evaluate(game)
# #             self.transposition[key] = value
# #             return value

# #         moves = self.order_moves(game, self.get_candidate_moves(game))

# #         if maximizing:
# #             value = -math.inf
# #             for r, c in moves:
# #                 previous_player = game.current_player
# #                 game.make_move(r, c, self.player)

# #                 value = max(
# #                     value,
# #                     self.minimax(game, depth - 1, alpha, beta, False)
# #                 )

# #                 game.undo_move(r, c, previous_player)
# #                 alpha = max(alpha, value)
# #                 if beta <= alpha:
# #                     break
# #         else:
# #             value = math.inf
# #             for r, c in moves:
# #                 previous_player = game.current_player
# #                 game.make_move(r, c, self.opponent)

# #                 value = min(
# #                     value,
# #                     self.minimax(game, depth - 1, alpha, beta, True)
# #                 )

# #                 game.undo_move(r, c, previous_player)
# #                 beta = min(beta, value)
# #                 if beta <= alpha:
# #                     break

# #         self.transposition[key] = value
# #         return value

# #     def board_key(self, game, depth, maximizing):
# #         return (
# #             tuple(tuple(row) for row in game.board),
# #             depth,
# #             maximizing,
# #             game.current_player,
# #         )

# #     def find_immediate_win(self, game, symbol):
# #         for r, c in game.available_moves():
# #             previous_player = game.current_player
# #             game.make_move(r, c, symbol)
# #             winner = game.check_winner()
# #             game.undo_move(r, c, previous_player)

# #             if winner == symbol:
# #                 return (r, c)
# #         return None

# #     def get_candidate_moves(self, game, radius=1):
# #         occupied = []

# #         for r in range(game.n):
# #             for c in range(game.n):
# #                 if game.board[r][c] != EMPTY:
# #                     occupied.append((r, c))

# #         if not occupied:
# #             center = game.n // 2
# #             return [(center, center)]

# #         candidates = set()

# #         for r, c in occupied:
# #             for dr in range(-radius, radius + 1):
# #                 for dc in range(-radius, radius + 1):
# #                     nr, nc = r + dr, c + dc
# #                     if 0 <= nr < game.n and 0 <= nc < game.n:
# #                         if game.board[nr][nc] == EMPTY:
# #                             candidates.add((nr, nc))

# #         if not candidates:
# #             return game.available_moves()

# #         return list(candidates)

# #     def evaluate(self, game):
# #         winner = game.check_winner()
# #         if winner == self.player:
# #             return 1_000_000
# #         if winner == self.opponent:
# #             return -1_000_000

# #         score = 0

# #         for segment in game.get_all_length_m_segments():
# #             cells = [game.board[r][c] for r, c in segment]

# #             player_count = cells.count(self.player)
# #             opponent_count = cells.count(self.opponent)
# #             empty_count = cells.count(EMPTY)

# #             if player_count > 0 and opponent_count > 0:
# #                 continue

# #             if player_count > 0 and opponent_count == 0:
# #                 score += self.segment_score(player_count, game.m)
# #                 if player_count == game.m - 1 and empty_count == 1:
# #                     score += 50_000

# #             elif opponent_count > 0 and player_count == 0:
# #                 score -= self.segment_score(opponent_count, game.m)
# #                 if opponent_count == game.m - 1 and empty_count == 1:
# #                     score -= 70_000

# #         score += self.center_control_bonus(game)
# #         score += self.mobility_bonus(game)
# #         return score

# #     def segment_score(self, marks, target):
# #         if marks >= target:
# #             return 1_000_000
# #         if marks == target - 1:
# #             return 10_000
# #         if marks == target - 2:
# #             return 1_000
# #         if marks == 1:
# #             return 10
# #         return 10 ** marks

# #     def center_control_bonus(self, game):
# #         center = (game.n - 1) / 2
# #         bonus = 0

# #         for r in range(game.n):
# #             for c in range(game.n):
# #                 cell = game.board[r][c]
# #                 if cell == EMPTY:
# #                     continue

# #                 dist = abs(r - center) + abs(c - center)
# #                 value = max(0, int((game.n * 2) - dist * 2))

# #                 if cell == self.player:
# #                     bonus += value
# #                 elif cell == self.opponent:
# #                     bonus -= value

# #         return bonus

# #     def mobility_bonus(self, game):
# #         bonus = 0
# #         for r, c in self.get_candidate_moves(game):
# #             neighbors_player = 0
# #             neighbors_opponent = 0

# #             for dr in (-1, 0, 1):
# #                 for dc in (-1, 0, 1):
# #                     if dr == 0 and dc == 0:
# #                         continue
# #                     nr, nc = r + dr, c + dc
# #                     if 0 <= nr < game.n and 0 <= nc < game.n:
# #                         if game.board[nr][nc] == self.player:
# #                             neighbors_player += 1
# #                         elif game.board[nr][nc] == self.opponent:
# #                             neighbors_opponent += 1

# #             bonus += neighbors_player * 2
# #             bonus -= neighbors_opponent

# #         return bonus

# #     def order_moves(self, game, moves):
# #         center = (game.n - 1) / 2

# #         def move_priority(move):
# #             r, c = move

# #             previous_player = game.current_player

# #             game.make_move(r, c, self.player)
# #             if game.check_winner() == self.player:
# #                 game.undo_move(r, c, previous_player)
# #                 return (-1_000_000_000, 0, 0)
# #             game.undo_move(r, c, previous_player)

# #             game.make_move(r, c, self.opponent)
# #             if game.check_winner() == self.opponent:
# #                 game.undo_move(r, c, previous_player)
# #                 return (-900_000_000, 0, 0)
# #             game.undo_move(r, c, previous_player)

# #             neighbor_score = 0
# #             for dr in (-1, 0, 1):
# #                 for dc in (-1, 0, 1):
# #                     if dr == 0 and dc == 0:
# #                         continue
# #                     nr, nc = r + dr, c + dc
# #                     if 0 <= nr < game.n and 0 <= nc < game.n:
# #                         if game.board[nr][nc] == self.player:
# #                             neighbor_score += 3
# #                         elif game.board[nr][nc] == self.opponent:
# #                             neighbor_score += 2

# #             dist_to_center = abs(r - center) + abs(c - center)
# #             return (-neighbor_score, dist_to_center, r + c)

# #         return sorted(moves, key=move_priority)


# # # Example local run:
# # # game = GeneralizedTicTacToe(n=12, m=5)
# # # game.human_vs_ai(ai_symbol=PLAYER_O, depth=4)

# # # Example online run:
# # # game = GeneralizedTicTacToe(n=12, m=5)
# # # game.ai_vs_online(team_id_1="YOUR_TEAM_ID", team_id_2="OTHER_TEAM_ID", game_id="GAME_ID", depth=4)


# import math


# class MinimaxAgent:
#     def __init__(self, player_symbol, max_depth=2):
#         self.player = player_symbol
#         self.opponent = PLAYER_O if player_symbol == PLAYER_X else PLAYER_X
#         self.max_depth = max_depth

#     def choose_move(self, game):
#         # 1. Win now if possible
#         move = self.find_immediate_win(game, self.player)
#         if move is not None:
#             return move

#         # 2. Block opponent win
#         move = self.find_immediate_win(game, self.opponent)
#         if move is not None:
#             return move

#         # 3. Otherwise do shallow minimax
#         best_score = -math.inf
#         best_move = None

#         moves = self.get_candidate_moves(game)

#         for r, c in moves:
#             previous_player = game.current_player
#             game.make_move(r, c, self.player)

#             score = self.minimax(
#                 game=game,
#                 depth=self.max_depth - 1,
#                 maximizing=False
#             )

#             game.undo_move(r, c, previous_player)

#             if score > best_score:
#                 best_score = score
#                 best_move = (r, c)

#         return best_move

#     def minimax(self, game, depth, maximizing):
#         terminal, winner = game.is_terminal()

#         if terminal:
#             if winner == self.player:
#                 return 100000
#             elif winner == self.opponent:
#                 return -100000
#             else:
#                 return 0

#         if depth == 0:
#             return self.evaluate(game)

#         moves = self.get_candidate_moves(game)

#         if maximizing:
#             best = -math.inf
#             for r, c in moves:
#                 previous_player = game.current_player
#                 game.make_move(r, c, self.player)
#                 score = self.minimax(game, depth - 1, False)
#                 game.undo_move(r, c, previous_player)
#                 best = max(best, score)
#             return best
#         else:
#             best = math.inf
#             for r, c in moves:
#                 previous_player = game.current_player
#                 game.make_move(r, c, self.opponent)
#                 score = self.minimax(game, depth - 1, True)
#                 game.undo_move(r, c, previous_player)
#                 best = min(best, score)
#             return best

#     def find_immediate_win(self, game, symbol):
#         for r, c in game.available_moves():
#             previous_player = game.current_player
#             game.make_move(r, c, symbol)
#             winner = game.check_winner()
#             game.undo_move(r, c, previous_player)

#             if winner == symbol:
#                 return (r, c)

#         return None

#     def get_candidate_moves(self, game):
#         occupied = []

#         for r in range(game.n):
#             for c in range(game.n):
#                 if game.board[r][c] != EMPTY:
#                     occupied.append((r, c))

#         # if board empty, play center
#         if not occupied:
#             center = game.n // 2
#             return [(center, center)]

#         candidates = set()

#         # only consider moves around existing pieces
#         for r, c in occupied:
#             for dr in (-1, 0, 1):
#                 for dc in (-1, 0, 1):
#                     nr, nc = r + dr, c + dc
#                     if 0 <= nr < game.n and 0 <= nc < game.n:
#                         if game.board[nr][nc] == EMPTY:
#                             candidates.add((nr, nc))

#         return list(candidates) if candidates else game.available_moves()

#     def evaluate(self, game):
#         score = 0

#         for segment in game.get_all_length_m_segments():
#             cells = [game.board[r][c] for r, c in segment]

#             player_count = cells.count(self.player)
#             opponent_count = cells.count(self.opponent)

#             # blocked segment
#             if player_count > 0 and opponent_count > 0:
#                 continue

#             if player_count > 0:
#                 score += 10 ** player_count
#             elif opponent_count > 0:
#                 score -= 10 ** opponent_count

#         return score
import math
from copy import deepcopy
import time
import api

EMPTY = "."
PLAYER_X = "X"
PLAYER_O = "O"


class GeneralizedTicTacToe:
    def __init__(self, n=3, m=3):
        if m > n:
            raise ValueError("Target m cannot be greater than board size n.")
        self.n = n
        self.m = m
        self.board = [[EMPTY for _ in range(n)] for _ in range(n)]
        self.current_player = PLAYER_X

    def clone(self):
        new_game = GeneralizedTicTacToe(self.n, self.m)
        new_game.board = deepcopy(self.board)
        new_game.current_player = self.current_player
        return new_game

    def print_board(self):
        print("\n   " + " ".join(f"{i:2}" for i in range(self.n)))
        for i, row in enumerate(self.board):
            print(f"{i:2} " + " ".join(f"{cell:2}" for cell in row))
        print()

    def available_moves(self):
        return [
            (r, c)
            for r in range(self.n)
            for c in range(self.n)
            if self.board[r][c] == EMPTY
        ]

    def make_move(self, row, col, player=None):
        if not (0 <= row < self.n and 0 <= col < self.n):
            return False

        if player is None:
            player = self.current_player

        if self.board[row][col] != EMPTY:
            return False

        self.board[row][col] = player
        self.current_player = PLAYER_O if player == PLAYER_X else PLAYER_X
        return True

    def undo_move(self, row, col, previous_player):
        self.board[row][col] = EMPTY
        self.current_player = previous_player

    def is_full(self):
        return all(
            self.board[r][c] != EMPTY
            for r in range(self.n)
            for c in range(self.n)
        )

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] == EMPTY:
                    continue

                symbol = self.board[r][c]

                for dr, dc in directions:
                    count = 1
                    nr, nc = r + dr, c + dc

                    while (
                        0 <= nr < self.n
                        and 0 <= nc < self.n
                        and self.board[nr][nc] == symbol
                    ):
                        count += 1
                        if count >= self.m:
                            return symbol
                        nr += dr
                        nc += dc

        return None

    def is_terminal(self):
        winner = self.check_winner()
        if winner is not None:
            return True, winner
        if self.is_full():
            return True, "DRAW"
        return False, None

    def get_all_length_m_segments(self):
        segments = []

        # Rows
        for r in range(self.n):
            for c in range(self.n - self.m + 1):
                segments.append([(r, c + i) for i in range(self.m)])

        # Columns
        for c in range(self.n):
            for r in range(self.n - self.m + 1):
                segments.append([(r + i, c) for i in range(self.m)])

        # Main diagonals
        for r in range(self.n - self.m + 1):
            for c in range(self.n - self.m + 1):
                segments.append([(r + i, c + i) for i in range(self.m)])

        # Anti-diagonals
        for r in range(self.n - self.m + 1):
            for c in range(self.m - 1, self.n):
                segments.append([(r + i, c - i) for i in range(self.m)])

        return segments

    def human_vs_ai(self, ai_symbol=PLAYER_O, depth=2):
        ai = MinimaxAgent(ai_symbol, max_depth=depth)
        human = PLAYER_X if ai_symbol == PLAYER_O else PLAYER_O

        print(f"\nGame {self.n}x{self.n}, target={self.m}")
        print(f"You are {human}, AI is {ai_symbol}\n")

        while True:
            self.print_board()

            terminal, winner = self.is_terminal()
            if terminal:
                if winner == "DRAW":
                    print("Draw!")
                else:
                    print(f"Winner: {winner}")
                break

            if self.current_player == human:
                try:
                    r, c = map(int, input("Enter row col: ").split())
                except ValueError:
                    print("Invalid input. Please enter: row col")
                    continue

                if not self.make_move(r, c, human):
                    print("Invalid move")
            else:
                start = time.time()
                move = ai.choose_move(self)
                end = time.time()

                if move is None:
                    print("No valid move found.")
                    break

                print(f"AI plays: {move}")
                print(f"Thinking time: {end - start:.4f} seconds")
                self.make_move(move[0], move[1], ai_symbol)

    def ai_vs_online(self, team_id_1, team_id_2, game_id, depth=2):
        ai_symbol = None
        opponent = None
        ai = None

        print(f"\nConnected to game {game_id}\n")

        while True:
            details = api.get_game_details(game_id)
            game_info = details["game"]

            status = game_info.get("status")
            turn_team_id = str(game_info.get("turnteamid"))
            winner_team_id = game_info.get("winnerteamid")

            if status != "O":
                self.print_board()
                print("\nGame finished!")

                if winner_team_id is None:
                    print("Result: DRAW")
                elif str(winner_team_id) == str(team_id_1):
                    print("You WIN")
                else:
                    print("You LOSE")

                break

            moves = api.get_moves(game_id, "300")
            self.board = [[EMPTY for _ in range(self.n)]
                          for _ in range(self.n)]

            for mv in moves:
                r, c = map(int, mv["move"].split(","))
                symbol = mv["symbol"]
                if 0 <= r < self.n and 0 <= c < self.n:
                    self.board[r][c] = symbol

            terminal, winner = self.is_terminal()
            if terminal:
                self.print_board()
                print("\nGame finished!")

                if winner == "DRAW":
                    print("Result: DRAW")
                else:
                    print(f"Winner: {winner}")
                break

            if ai_symbol is None:
                if moves:
                    last_move = moves[-1]
                    last_team = str(last_move["teamId"])
                    last_symbol = last_move["symbol"]

                    if last_team == str(team_id_1):
                        ai_symbol = last_symbol
                        opponent = PLAYER_O if ai_symbol == PLAYER_X else PLAYER_X
                    else:
                        opponent = last_symbol
                        ai_symbol = PLAYER_O if opponent == PLAYER_X else PLAYER_X
                else:
                    if str(team_id_1) == str(game_info["team1id"]):
                        ai_symbol = PLAYER_X
                        opponent = PLAYER_O
                    else:
                        ai_symbol = PLAYER_O
                        opponent = PLAYER_X

                ai = MinimaxAgent(ai_symbol, max_depth=depth)
                print(f"AI is {ai_symbol}, Opponent is {opponent}\n")

            if ai_symbol is not None and opponent is not None:
                if turn_team_id == str(team_id_1):
                    self.current_player = ai_symbol
                else:
                    self.current_player = opponent

            self.print_board()

            if turn_team_id != str(team_id_1):
                print("Waiting for opponent move...\n")
                time.sleep(2)
                continue

            start = time.time()
            move = ai.choose_move(self)
            end = time.time()

            if move is None:
                print("No valid move available.")
                break

            if self.board[move[0]][move[1]] != EMPTY:
                print("Invalid move (already occupied):", move)
                time.sleep(2)
                continue

            print("AI plays:", move)
            print(f"Thinking time: {end - start:.4f} seconds")

            try:
                api.make_move(game_id, team_id_1, f"{move[0]},{move[1]}")
            except Exception as e:
                print("Move failed:", e)
                time.sleep(2)
                continue

            self.make_move(move[0], move[1], ai_symbol)
            time.sleep(2)


class MinimaxAgent:
    def __init__(self, player_symbol, max_depth=2):
        self.player = player_symbol
        self.opponent = PLAYER_O if player_symbol == PLAYER_X else PLAYER_X
        self.max_depth = max_depth

    def choose_move(self, game):
        # win immediately
        move = self.find_immediate_win(game, self.player)
        if move is not None:
            return move

        # block opponent immediate win
        move = self.find_immediate_win(game, self.opponent)
        if move is not None:
            return move

        best_score = -math.inf
        best_move = None

        moves = self.get_candidate_moves(game)

        for r, c in moves:
            previous_player = game.current_player
            game.make_move(r, c, self.player)

            score = self.minimax(
                game=game,
                depth=self.max_depth - 1,
                maximizing=False
            )

            game.undo_move(r, c, previous_player)

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    def minimax(self, game, depth, maximizing):
        terminal, winner = game.is_terminal()

        if terminal:
            if winner == self.player:
                return 100000
            if winner == self.opponent:
                return -100000
            return 0

        if depth == 0:
            return self.evaluate(game)

        moves = self.get_candidate_moves(game)

        if maximizing:
            best = -math.inf
            for r, c in moves:
                previous_player = game.current_player
                game.make_move(r, c, self.player)
                score = self.minimax(game, depth - 1, False)
                game.undo_move(r, c, previous_player)
                best = max(best, score)
            return best
        else:
            best = math.inf
            for r, c in moves:
                previous_player = game.current_player
                game.make_move(r, c, self.opponent)
                score = self.minimax(game, depth - 1, True)
                game.undo_move(r, c, previous_player)
                best = min(best, score)
            return best

    def find_immediate_win(self, game, symbol):
        for r, c in game.available_moves():
            previous_player = game.current_player
            game.make_move(r, c, symbol)
            winner = game.check_winner()
            game.undo_move(r, c, previous_player)

            if winner == symbol:
                return (r, c)

        return None

    def get_candidate_moves(self, game):
        occupied = []

        for r in range(game.n):
            for c in range(game.n):
                if game.board[r][c] != EMPTY:
                    occupied.append((r, c))

        if not occupied:
            center = game.n // 2
            return [(center, center)]

        candidates = set()

        for r, c in occupied:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < game.n and 0 <= nc < game.n:
                        if game.board[nr][nc] == EMPTY:
                            candidates.add((nr, nc))

        if candidates:
            return list(candidates)

        return game.available_moves()

    def evaluate(self, game):
        score = 0

        for segment in game.get_all_length_m_segments():
            cells = [game.board[r][c] for r, c in segment]

            player_count = cells.count(self.player)
            opponent_count = cells.count(self.opponent)

            # blocked segment
            if player_count > 0 and opponent_count > 0:
                continue

            if player_count > 0:
                score += 10 ** player_count
            elif opponent_count > 0:
                score -= 10 ** opponent_count

        return score


# Example local run:
# game = GeneralizedTicTacToe(n=12, m=5)
# game.human_vs_ai(ai_symbol=PLAYER_O, depth=2)

# Example online run:
# game = GeneralizedTicTacToe(n=12, m=5)
# game.ai_vs_online(team_id_1="YOUR_TEAM_ID", team_id_2="OTHER_TEAM_ID", game_id="GAME_ID", depth=2)
