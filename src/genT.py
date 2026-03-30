import math
from copy import deepcopy
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

    def human_vs_ai(self, ai_symbol=PLAYER_O, depth=3):
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
                move = ai.choose_move(self)
                if move is None:
                    print("No valid move found.")
                    break
                print(f"AI plays: {move}")
                self.make_move(move[0], move[1], ai_symbol)
    
    def ai_vs_online(self, team_id_1, team_id_2, game_id, depth=2):
        import time
        import json
        import api

        processed_move_ids = set()

        # Figure out symbols from the latest move if possible
        moves = api.get_moves(game_id, "100")


        latest = None
        if moves:
            latest = moves[-1]
        if latest is not None:
            latest_team = str(latest["teamId"])
            latest_symbol = latest["symbol"]

            if latest_team == str(team_id_1):
                ai_symbol = latest_symbol
                opponent = PLAYER_O if ai_symbol == PLAYER_X else PLAYER_X
            elif latest_team == str(team_id_2):
                opponent = latest_symbol
                ai_symbol = PLAYER_O if opponent == PLAYER_X else PLAYER_X
            else:
                ai_symbol = PLAYER_X
                opponent = PLAYER_O
        else:
            # fallback
            ai_symbol = PLAYER_X
            opponent = PLAYER_O

        ai = MinimaxAgent(ai_symbol, max_depth=depth)

        print(f"\nConnected to game {game_id}")
        print(f"AI is {ai_symbol}, Opponent is {opponent}\n")

        while True:
            details = api.get_game_details(game_id)
            game_data = details["game"]


            if isinstance(game_data, str):
                import json
                game_info = json.loads(game_data)
            else:
                game_info = game_data

            status = game_info.get("status")
            winner_team_id = game_info.get("winnerteamid")
            turn_team_id = str(game_info.get("turnteamid"))

            if status != "O":
                self.print_board()
                if winner_team_id is None:
                    print("Game finished: Draw")
                elif str(winner_team_id) == str(team_id_1):
                    print("Game finished: Your team won")
                else:
                    print("Game finished: Opponent won")
                break

            moves = api.get_moves(game_id, "100")


            # rebuild board from scratch
            self.board = [[EMPTY for _ in range(self.n)] for _ in range(self.n)]
            self.current_player = PLAYER_X

            for mv in moves:
                move_id = str(mv["moveId"])
                processed_move_ids.add(move_id)

                r, c = map(int, mv["move"].split(","))
                symbol = mv["symbol"]

                if 0 <= r < self.n and 0 <= c < self.n:
                    self.board[r][c] = symbol

            # ADD THIS HERE
            terminal, winner = self.is_terminal()
            if terminal:
                self.print_board()
                if winner == "DRAW":
                    print("Game finished: Draw")
                else:
                    print(f"Game finished: Winner is {winner}")
                break
            # set current player based on turn
            if turn_team_id == str(team_id_1):
                self.current_player = ai_symbol
            else:
                self.current_player = opponent

            self.print_board()

            if turn_team_id != str(team_id_1):
                print("Waiting for opponent move...")
                time.sleep(1)
                continue

            move = ai.choose_move(self)
            if move is None:
                print("No valid move available.")
                break

            # final local safety check
            if self.board[move[0]][move[1]] != EMPTY:
                print("Chosen move is already occupied locally:", move)
                time.sleep(1)
                continue

            print("AI plays:", move)

            try:
                new_move_id = api.make_move(
                    game_id, team_id_1, f"{move[0]},{move[1]}")
            except Exception as e:
                print("Move failed:", e)
                time.sleep(1)
                continue

            # only update local board after server accepts
            self.make_move(move[0], move[1], ai_symbol)
            processed_move_ids.add(str(new_move_id))

            time.sleep(1)
    


class MinimaxAgent:
    def __init__(self, player_symbol, max_depth=3):
        self.player = player_symbol
        self.opponent = PLAYER_O if player_symbol == PLAYER_X else PLAYER_X
        self.max_depth = max_depth

    def choose_move(self, game):
        best_score = -math.inf
        best_move = None

        moves = self.order_moves(game, game.available_moves())

        for r, c in moves:
            previous_player = game.current_player
            game.make_move(r, c, self.player)

            score = self.minimax(
                game=game,
                depth=self.max_depth - 1,
                alpha=-math.inf,
                beta=math.inf,
                maximizing=False,
            )

            game.undo_move(r, c, previous_player)

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing):
        terminal, winner = game.is_terminal()
        if terminal:
            if winner == self.player:
                return 1_000_000
            if winner == self.opponent:
                return -1_000_000
            return 0

        if depth == 0:
            return self.evaluate(game)

        if maximizing:
            value = -math.inf
            for r, c in self.order_moves(game, game.available_moves()):
                previous_player = game.current_player
                game.make_move(r, c, self.player)

                value = max(
                    value,
                    self.minimax(game, depth - 1, alpha, beta, False)
                )

                game.undo_move(r, c, previous_player)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            return value

        value = math.inf
        for r, c in self.order_moves(game, game.available_moves()):
            previous_player = game.current_player
            game.make_move(r, c, self.opponent)

            value = min(
                value,
                self.minimax(game, depth - 1, alpha, beta, True)
            )

            game.undo_move(r, c, previous_player)
            beta = min(beta, value)
            if beta <= alpha:
                break

        return value

    def evaluate(self, game):
        winner = game.check_winner()
        if winner == self.player:
            return 1_000_000
        if winner == self.opponent:
            return -1_000_000

        score = 0

        for segment in game.get_all_length_m_segments():
            cells = [game.board[r][c] for r, c in segment]
            player_count = cells.count(self.player)
            opponent_count = cells.count(self.opponent)
            empty_count = cells.count(EMPTY)

            # Blocked line
            if player_count > 0 and opponent_count > 0:
                continue

            # Useful for AI
            if player_count > 0 and opponent_count == 0:
                score += self.segment_score(player_count, empty_count)

            # Dangerous for AI
            elif opponent_count > 0 and player_count == 0:
                score -= self.segment_score(opponent_count, empty_count)

        score += self.center_control_bonus(game)
        return score

    def segment_score(self, marks, empties):
        return (10 ** marks) + empties

    def center_control_bonus(self, game):
        center = (game.n - 1) / 2
        bonus = 0

        for r in range(game.n):
            for c in range(game.n):
                cell = game.board[r][c]
                if cell == EMPTY:
                    continue

                dist = abs(r - center) + abs(c - center)
                value = max(0, game.n - dist)

                if cell == self.player:
                    bonus += value
                elif cell == self.opponent:
                    bonus -= value

        return bonus

    def order_moves(self, game, moves):
        center = (game.n - 1) / 2

        def neighbor_count(r, c):
            count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < game.n and 0 <= nc < game.n:
                        if game.board[nr][nc] != EMPTY:
                            count += 1
            return count

        return sorted(
            moves,
            key=lambda move: (
                -neighbor_count(move[0], move[1]),
                abs(move[0] - center) + abs(move[1] - center),
            ),
        )
