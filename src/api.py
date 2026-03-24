import http.client
import ast

# ---- CONFIG (you will fill these) ----
HOST = "www.notexponential.com"
URL = "/aip2pgaming/api/index.php"

USER_ID = "3672"
API_KEY = "6f7504789dda4c53374b"

HEADERS = {
    "userId": USER_ID,
    "x-api-key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded",
}


# ---- INTERNAL HELPERS ----
def _parse(data: str):
    try:
        return ast.literal_eval(data)
    except:
        return {"raw": data}


def _post(payload: str):
    conn = http.client.HTTPSConnection(HOST)
    conn.request("POST", URL, payload, HEADERS)
    res = conn.getresponse()
    data = res.read().decode()
    conn.close()
    return _parse(data)


def _get(query: str):
    conn = http.client.HTTPSConnection(HOST)
    full_url = f"{URL}?{query}"
    conn.request("GET", full_url, None, HEADERS)
    res = conn.getresponse()
    data = res.read().decode()
    conn.close()
    return _parse(data)


# ---- MAIN FUNCTIONS YOU USE ----
def create_game(team1: str, team2: str, n: int, m: int):
    payload = f"type=game&teamId1={team1}&teamId2={team2}&gameType=TTT&boardSize={n}&target={m}"
    res = _post(payload)
    return res["gameId"]


def make_move(game_id: str, team_id: str, move: str):
    payload = f"type=move&gameId={game_id}&teamId={team_id}&move={move}"
    res = _post(payload)
    return res["moveId"]


def get_moves(game_id: str, count: str = "1"):
    query = f"type=moves&gameId={game_id}&count={count}"
    res = _get(query)
    return res["moves"][0]
