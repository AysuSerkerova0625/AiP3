import http.client
import time
import json
import ast
from urllib.parse import urlencode
from typing import Any, Dict, List, Optional, Tuple, Union

HOST = "www.notexponential.com"
URL = "/aip2pgaming/api/index.php"

USER_ID = "3732"
API_KEY = "cf69bbdf6985a8666c55"

HEADERS = {
    "userId": USER_ID,
    "x-api-key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "humans_21909=1",
}

DEBUG = False

DEFAULT_RETRIES = 5
DEFAULT_TIMEOUT = 25
BACKOFF_BASE_SECONDS = 2
MAX_BACKOFF_SECONDS = 10

WAIT_POLL_SECONDS = 3.0
ERROR_SLEEP_SECONDS = 4.0
DETAILS_EVERY_N_POLLS = 5


class ApiError(Exception):
    pass


def debug_print(*args):
    if DEBUG:
        print(*args)


def _safe_parse_response(raw_data: str) -> Dict[str, Any]:
    try:
        parsed = json.loads(raw_data)
        if isinstance(parsed, dict):
            return parsed
        return {"code": "OK", "data": parsed}
    except Exception:
        pass

    try:
        parsed = ast.literal_eval(raw_data)
        if isinstance(parsed, dict):
            return parsed
        return {"code": "OK", "data": parsed}
    except Exception:
        pass

    return {"code": "FAIL", "raw": raw_data}


def _request(
    method: str,
    path: str,
    body: Optional[str] = None,
    retries: int = DEFAULT_RETRIES,
    timeout: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    last_error = None

    for attempt in range(1, retries + 1):
        conn = None
        raw_data = ""

        try:
            conn = http.client.HTTPSConnection(HOST, timeout=timeout)
            conn.request(method, path, body=body, headers=HEADERS)
            response = conn.getresponse()

            status = response.status
            reason = response.reason
            raw_data = response.read().decode("utf-8", errors="replace")

            debug_print(f"[{attempt}/{retries}] {method} {path}")
            debug_print(f"HTTP {status} {reason}")
            debug_print("RAW RESPONSE:", repr(raw_data[:500]))

            if not raw_data.strip():
                last_error = {
                    "code": "FAIL",
                    "message": "Empty response from server",
                    "http_status": status,
                }
                time.sleep(min(BACKOFF_BASE_SECONDS **
                           attempt, MAX_BACKOFF_SECONDS))
                continue

            lowered = raw_data.lower().strip()
            if lowered.startswith("<script>") or lowered.startswith("<html") or "<html" in lowered:
                last_error = {
                    "code": "FAIL",
                    "message": "Server returned HTML/script page instead of API response",
                    "http_status": status,
                    "raw": raw_data[:500],
                }
                time.sleep(min(BACKOFF_BASE_SECONDS **
                           attempt, MAX_BACKOFF_SECONDS))
                continue

            if status >= 500:
                last_error = {
                    "code": "FAIL",
                    "message": f"Server error {status}: {reason}",
                    "http_status": status,
                    "raw": raw_data[:500],
                }
                time.sleep(min(BACKOFF_BASE_SECONDS **
                           attempt, MAX_BACKOFF_SECONDS))
                continue

            parsed = _safe_parse_response(raw_data)
            parsed.setdefault("http_status", status)
            return parsed

        except Exception as e:
            last_error = {
                "code": "FAIL",
                "message": "Exception during request",
                "details": repr(e),
            }
            debug_print(f"Request exception on attempt {attempt}: {repr(e)}")
            time.sleep(min(BACKOFF_BASE_SECONDS **
                       attempt, MAX_BACKOFF_SECONDS))

        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    if isinstance(last_error, dict):
        return last_error

    return {"code": "FAIL", "message": "Request failed after retries"}


def make_post_request(params: Dict[str, Any]) -> Dict[str, Any]:
    body = urlencode(params)
    return _request("POST", URL, body=body)


def make_get_request(params: Dict[str, Any]) -> Dict[str, Any]:
    query = urlencode(params)
    return _request("GET", f"{URL}?{query}")


def _ensure_ok(res: Dict[str, Any], context: str) -> Dict[str, Any]:
    if res.get("code") != "OK":
        raise ApiError(f"{context} failed: {res}")
    return res


# -------------------------
# API FUNCTIONS
# -------------------------

def create_team(tname: str) -> str:
    res = make_post_request({"type": "team", "name": tname})
    _ensure_ok(res, "create_team")
    return str(res["teamId"])


def add_team_member(team_id: str, user_id: str) -> Dict[str, Any]:
    res = make_post_request({
        "type": "member",
        "userId": user_id,
        "teamId": team_id,
    })
    return _ensure_ok(res, "add_team_member")


def get_my_team() -> Dict[str, Any]:
    res = make_get_request({"type": "myTeams"})
    return _ensure_ok(res, "get_my_team")


def create_game(team_id1: str, team_id2: str, board_size: int, target: int) -> str:
    res = make_post_request({
        "type": "game",
        "teamId1": team_id1,
        "teamId2": team_id2,
        "gameType": "TTT",
        "boardSize": board_size,
        "target": target,
    })
    _ensure_ok(res, "create_game")
    return str(res["gameId"])


def get_my_games() -> Dict[str, Any]:
    res = make_get_request({"type": "myGames"})
    return _ensure_ok(res, "get_my_games")


def normalize_move(move: Union[str, Tuple[int, int], List[int]]) -> str:
    if isinstance(move, str):
        cleaned = move.replace("(", "").replace(")", "").replace(" ", "")
        x_str, y_str = cleaned.split(",")
        return f"{int(x_str)},{int(y_str)}"

    if isinstance(move, (tuple, list)) and len(move) == 2:
        return f"{int(move[0])},{int(move[1])}"

    raise ValueError(f"Unsupported move format: {move}")


def make_move(game_id: str, team_id: str, move: Union[str, Tuple[int, int], List[int]]) -> str:
    move_str = normalize_move(move)
    res = make_post_request({
        "type": "move",
        "gameId": game_id,
        "teamId": team_id,
        "move": move_str,
    })
    _ensure_ok(res, "make_move")
    return str(res["moveId"])


def get_moves(game_id: str, count: int = 300) -> List[Dict[str, Any]]:
    res = make_get_request({
        "type": "moves",
        "gameId": game_id,
        "count": count,
    })

    if res.get("code") == "FAIL" and res.get("message") == "No moves":
        return []

    _ensure_ok(res, "get_moves")
    return res.get("moves", [])


def get_game_details(game_id: str) -> Dict[str, Any]:
    res = make_get_request({
        "type": "gameDetails",
        "gameId": game_id,
    })
    _ensure_ok(res, "get_game_details")

    if "game" in res and isinstance(res["game"], str):
        try:
            res["game"] = json.loads(res["game"])
        except Exception:
            pass

    return res


def get_all_moves(game_id: str) -> List[Dict[str, Any]]:
    details = get_game_details(game_id)
    game = details.get("game", {})

    total_moves = int(
        game.get("moves")
        or game.get("Moves")
        or 0
    )

    return get_moves(game_id, count=max(total_moves + 5, 50))


# -------------------------
# LOCAL BOARD HELPERS
# -------------------------

def create_empty_board(board_size: int) -> List[List[str]]:
    return [["." for _ in range(board_size)] for _ in range(board_size)]


def print_board(board: List[List[str]]) -> None:
    size = len(board)
    print()
    print("   " + " ".join(f"{i:2d}" for i in range(size)))
    for i, row in enumerate(board):
        print(f"{i:2d} " + " ".join(f"{cell:2s}" for cell in row))
    print()


def parse_move_string(move_str: str) -> Tuple[int, int]:
    cleaned = normalize_move(move_str)
    x_str, y_str = cleaned.split(",")
    return int(x_str), int(y_str)


def apply_move_to_board(board: List[List[str]], move_str: str, symbol: str) -> None:
    x, y = parse_move_string(move_str)
    if 0 <= x < len(board) and 0 <= y < len(board):
        board[x][y] = symbol
    else:
        raise ValueError(f"Move out of board range: {move_str}")


def is_cell_empty(board: List[List[str]], move: Union[str, Tuple[int, int], List[int]]) -> bool:
    move_str = normalize_move(move)
    x, y = parse_move_string(move_str)
    return board[x][y] == "."


def infer_turn_team_id(game: Dict[str, Any]) -> Optional[str]:
    for key in ["turnTeamId", "turnteamid", "turn", "nextTeamId"]:
        if key in game and game[key] not in (None, ""):
            return str(game[key])
    return None


def infer_game_status(game: Dict[str, Any]) -> str:
    for key in ["status", "gameStatus"]:
        if key in game and game[key] is not None:
            return str(game[key]).lower()
    return ""


def get_move_id(move_obj: Dict[str, Any]) -> str:
    for key in ["moveId", "id"]:
        if key in move_obj:
            return str(move_obj[key])
    raise ValueError(f"Move object has no move id: {move_obj}")


def get_move_team_id(move_obj: Dict[str, Any]) -> str:
    for key in ["teamId", "team", "playerId"]:
        if key in move_obj:
            return str(move_obj[key])
    raise ValueError(f"Move object has no team id: {move_obj}")


def get_move_string(move_obj: Dict[str, Any]) -> str:
    for key in ["move", "position"]:
        if key in move_obj:
            return normalize_move(str(move_obj[key]))
    raise ValueError(f"Move object has no move string: {move_obj}")


# -------------------------
# SIMPLE AI
# Replace with your own logic
# -------------------------

def choose_ai_move(board: List[List[str]]) -> Tuple[int, int]:
    size = len(board)
    center = size // 2

    if board[center][center] == ".":
        return center, center

    for radius in range(size):
        for i in range(max(0, center - radius), min(size, center + radius + 1)):
            for j in range(max(0, center - radius), min(size, center + radius + 1)):
                if board[i][j] == ".":
                    return i, j

    raise ValueError("No legal moves available")


def choose_ai_move_with_exclusions(board: List[List[str]], excluded_moves: set[str]) -> Tuple[int, int]:
    size = len(board)
    center = size // 2

    candidates = []

    if board[center][center] == ".":
        candidates.append((center, center))

    for radius in range(size):
        for i in range(max(0, center - radius), min(size, center + radius + 1)):
            for j in range(max(0, center - radius), min(size, center + radius + 1)):
                if board[i][j] == ".":
                    candidates.append((i, j))

    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            unique_candidates.append(c)
            seen.add(c)

    for move in unique_candidates:
        move_str = normalize_move(move)
        if move_str not in excluded_moves:
            return move

    raise ValueError("No legal non-excluded moves available")


# -------------------------
# GAME LOOP
# -------------------------

def play_game_light(game_id: str, my_team_id: str, show_board: bool = False) -> None:
    details = get_game_details(game_id)
    game = details.get("game", {})

    board_size = int(game.get("boardSize") or game.get("boardsize"))
    team1_id = str(game.get("teamId1") or game.get("team1id"))
    team2_id = str(game.get("teamId2") or game.get("team2id"))

    my_symbol = "X" if str(my_team_id) == team1_id else "O"
    opp_symbol = "O" if my_symbol == "X" else "X"

    board = create_empty_board(board_size)
    seen_move_ids = set()
    failed_moves_for_current_state = set()

    initial_moves = get_all_moves(game_id)
    for move_obj in reversed(initial_moves):
        move_id = get_move_id(move_obj)
        move_str = get_move_string(move_obj)
        move_team = get_move_team_id(move_obj)

        symbol = my_symbol if move_team == str(my_team_id) else opp_symbol
        apply_move_to_board(board, move_str, symbol)
        seen_move_ids.add(move_id)

    print(f"Game {game_id} started. Board size: {board_size}x{board_size}")
    print(f"My team: {my_team_id}, My symbol: {my_symbol}")

    if show_board:
        print_board(board)

    waiting_printed = False
    poll_counter = 0
    last_known_turn_team_id = infer_turn_team_id(game)
    last_known_status = infer_game_status(game)

    while True:
        try:
            moves = get_all_moves(game_id)
            poll_counter += 1
            new_moves = []

            for move_obj in reversed(moves):
                move_id = get_move_id(move_obj)
                if move_id not in seen_move_ids:
                    new_moves.append(move_obj)
                    seen_move_ids.add(move_id)

            if new_moves:
                waiting_printed = False
                failed_moves_for_current_state.clear()

                for move_obj in new_moves:
                    move_str = get_move_string(move_obj)
                    move_team = get_move_team_id(move_obj)

                    if move_team == str(my_team_id):
                        apply_move_to_board(board, move_str, my_symbol)
                        print(f"AI played: {move_str}")
                    else:
                        apply_move_to_board(board, move_str, opp_symbol)
                        print(f"Opponent played: {move_str}")

                if show_board:
                    print_board(board)

            if poll_counter % DETAILS_EVERY_N_POLLS == 0 or last_known_turn_team_id is None:
                details = get_game_details(game_id)
                game = details.get("game", {})
                new_status = infer_game_status(game)
                new_turn = infer_turn_team_id(game)

                if new_status:
                    last_known_status = new_status
                if new_turn:
                    last_known_turn_team_id = new_turn

            if last_known_status in {"finished", "complete", "done"}:
                print("Game finished.")
                if show_board:
                    print_board(board)
                break

            if last_known_turn_team_id == str(my_team_id):
                try:
                    candidate_move = choose_ai_move_with_exclusions(
                        board, failed_moves_for_current_state)
                    move_str = normalize_move(candidate_move)

                    if not is_cell_empty(board, move_str):
                        failed_moves_for_current_state.add(move_str)
                        debug_print(
                            f"Chosen move is not empty locally: {move_str}")
                        time.sleep(1)
                        continue

                    print(f"AI wants to play: {move_str}")
                    move_id = make_move(game_id, my_team_id, move_str)

                    apply_move_to_board(board, move_str, my_symbol)
                    seen_move_ids.add(str(move_id))
                    failed_moves_for_current_state.clear()

                    print(f"AI played: {move_str}")
                    if show_board:
                        print_board(board)

                    waiting_printed = False
                    time.sleep(1.0)

                except Exception as e:
                    if "move_str" in locals():
                        failed_moves_for_current_state.add(move_str)
                        print(f"Move failed: {move_str} -> {e}")
                    else:
                        print(f"Move failed: {e}")

                    time.sleep(2.0)
            else:
                if not waiting_printed:
                    print("Waiting for opponent...")
                    waiting_printed = True
                time.sleep(WAIT_POLL_SECONDS)

        except Exception as e:
            print("Loop error:", e)
            time.sleep(ERROR_SLEEP_SECONDS)


if __name__ == "__main__":
    try:
        print("Connected.")
        print("My teams:", get_my_team())
        print("My games:", get_my_games())

        # Example:
        # GAME_ID = "5716"
        # MY_TEAM_ID = "1481"
        # play_game_light(GAME_ID, MY_TEAM_ID, show_board=False)

    except Exception as e:
        print("ERROR:", e)
