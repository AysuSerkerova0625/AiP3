import http.client
import time
import json
import ast

HOST = "www.notexponential.com"
URL = "/aip2pgaming/api/index.php"

USER_ID = "3732"
API_KEY = "cf69bbdf6985a8666c55"

headers = {
    "userId": USER_ID,
    "x-api-key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "humans_21909=1",
}


# ---------------------------------
# CORE REQUEST FUNCTION (FIXED)
# ---------------------------------
def _request(method: str, path: str, body=None, retries=3) -> dict:
    for attempt in range(retries):
        raw_data = ""

        try:
            conn = http.client.HTTPSConnection(HOST)
            conn.request(method, path, body, headers)

            response = conn.getresponse()
            raw_data = response.read().decode()
            conn.close()

            # 🔥 bypass cookie script
            if raw_data.startswith("<script>"):
                print("Cookie check triggered, retrying...")
                time.sleep(1)
                continue

            # ✅ try JSON first
            try:
                return json.loads(raw_data)
            except Exception:
                pass

            # ✅ fallback (sometimes API returns python-like dict)
            try:
                return ast.literal_eval(raw_data)
            except Exception:
                print("RAW RESPONSE:", repr(raw_data))
                return {"code": "FAIL", "raw": raw_data}

        except Exception as e:
            print(f"Request error (attempt {attempt+1}):", e)
            if raw_data:
                print("RAW RESPONSE:", repr(raw_data))
            time.sleep(1)

    return {"code": "FAIL", "message": "Request failed after retries"}


# ---------------------------------
# WRAPPERS
# ---------------------------------
def make_post_request(parameters: str) -> dict:
    return _request("POST", URL, parameters)


def make_get_request(parameters: str) -> dict:
    return _request("GET", URL + "?" + parameters)


# ---------------------------------
# API FUNCTIONS
# ---------------------------------
def create_team(tname: str) -> str:
    res = make_post_request(f"type=team&name={tname}")
    print("create_team:", res)
    if res.get("code") != "OK":
        raise ValueError(res)
    return str(res["teamId"])


def add_team_member(teamId: str, userId: str) -> dict:
    res = make_post_request(f"type=member&userId={userId}&teamId={teamId}")
    print("add_team_member:", res)
    if res.get("code") != "OK":
        raise ValueError(res)
    return res


def get_my_team() -> dict:
    res = make_get_request("type=myTeams")
    print("get_my_team:", res)
    if res.get("code") != "OK":
        raise ValueError(res)
    return res


def create_game(teamId1: str, teamId2: str, boardSize: int, target: int) -> str:
    payload = (
        f"type=game&teamId1={teamId1}&teamId2={teamId2}"
        f"&gameType=TTT&boardSize={boardSize}&target={target}"
    )
    res = make_post_request(payload)
    print("create_game:", res)
    if res.get("code") != "OK":
        raise ValueError(res)
    return str(res["gameId"])


def get_my_games() -> dict:
    res = make_get_request("type=myGames")
    print("get_my_games:", res)
    if res.get("code") != "OK":
        raise ValueError(res)
    return res


def make_move(gameId: str, teamId: str, move: str) -> str:
    payload = f"type=move&gameId={gameId}&teamId={teamId}&move={move}"
    res = make_post_request(payload)
    print("make_move:", res)

    if res.get("code") != "OK":
        print("❌ MOVE FAILED:", res)
        raise ValueError(res)

    return str(res["moveId"])


# 🔥 IMPORTANT FIX: RETURN FULL MOVE LIST
def get_moves(gameId: str, count: str = "100"):
    res = make_get_request(f"type=moves&gameId={gameId}&count={count}")
    print("get_moves:", res)

    if res.get("code") != "OK":
        raise ValueError(res)

    return res.get("moves", [])


def get_game_details(gameId: str) -> dict:
    res = make_get_request(f"type=gameDetails&gameId={gameId}")
    print("get_game_details:", res)

    if res.get("code") != "OK":
        raise ValueError(res)

    # 🔥 FIX: parse inner JSON string
    try:
        res["game"] = json.loads(res["game"])
    except Exception:
        pass

    return res


def get_board_string(gameId: str) -> dict:
    res = make_get_request(f"type=boardString&gameId={gameId}")
    print("get_board_string:", res)
    if res.get("code") != "OK":
        raise ValueError(res)
    return res


def get_board_map(gameId: str) -> dict:
    res = make_get_request(f"type=boardMap&gameId={gameId}")
    print("get_board_map:", res)
    if res.get("code") != "OK":
        raise ValueError(res)
    return res
