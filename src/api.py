import http.client
import ast

URL = "/aip2pgaming/api/index.php"
USER_ID = "3732"
API_KEY = "cf69bbdf6985a8666c55"

headers = {
    "userId": USER_ID,
    "x-api-key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded",
}


def make_post_request(parameters: str) -> dict:
    conn = http.client.HTTPSConnection("www.notexponential.com")
    conn.request("POST", URL, parameters, headers)
    response = conn.getresponse()
    data = response.read().decode()
    conn.close()
    return ast.literal_eval(data)


def make_get_request(parameters: str) -> dict:
    conn = http.client.HTTPSConnection("www.notexponential.com")
    full_path = URL + "?" + parameters
    conn.request("GET", full_path, None, headers)
    response = conn.getresponse()
    data = response.read().decode()
    conn.close()
    return ast.literal_eval(data)


def create_team(tname: str) -> str:
    payload = f"type=team&name={tname}"
    res = make_post_request(payload)
    print("create_team:", res)
    if res.get("code") != "OK":
        raise ValueError(f"create_team failed: {res}")
    return str(res["teamId"])


def add_team_member(teamId: str, userId: str) -> dict:
    payload = f"type=member&userId={userId}&teamId={teamId}"
    res = make_post_request(payload)
    print("add_team_member:", res)
    if res.get("code") != "OK":
        raise ValueError(f"add_team_member failed: {res}")
    return res


def get_team_members(teamId: str) -> dict:
    payload = f"type=team&teamId={teamId}"
    res = make_get_request(payload)
    print("get_team_members:", res)
    if res.get("code") != "OK":
        raise ValueError(f"get_team_members failed: {res}")
    return res


def get_my_team() -> dict:
    payload = "type=myTeams"
    res = make_get_request(payload)
    print("get_my_team:", res)
    if res.get("code") != "OK":
        raise ValueError(f"get_my_team failed: {res}")
    return res


def create_game(teamId1: str, teamId2: str, boardSize: int, target: int) -> str:
    payload = (
        f"type=game&teamId1={teamId1}&teamId2={teamId2}"
        f"&gameType=TTT&boardSize={boardSize}&target={target}"
    )
    res = make_post_request(payload)
    print("create_game:", res)
    if res.get("code") != "OK":
        raise ValueError(f"create_game failed: {res}")
    return str(res["gameId"])


def get_my_games() -> dict:
    payload = "type=myGames"
    res = make_get_request(payload)
    print("get_my_games:", res)
    if res.get("code") != "OK":
        raise ValueError(f"get_my_games failed: {res}")
    return res


def make_move(gameId: str, teamId: str, move: str) -> str:
    payload = f"type=move&gameId={gameId}&teamId={teamId}&move={move}"
    res = make_post_request(payload)
    print("make_move:", res)
    if res.get("code") != "OK":
        raise ValueError(f"make_move failed: {res}")
    return str(res["moveId"])


def get_moves(gameId: str, count: str = "1"):
    payload = f"type=moves&gameId={gameId}&count={count}"
    res = make_get_request(payload)
    print("get_moves:", res)

    if res.get("code") != "OK":
        raise ValueError(f"get_moves failed: {res}")

    if "moves" not in res or not res["moves"]:
        return None

    return res["moves"][0]


def get_game_details(gameId: str) -> dict:
    payload = f"type=gameDetails&gameId={gameId}"
    res = make_get_request(payload)
    print("get_game_details:", res)
    if res.get("code") != "OK":
        raise ValueError(f"get_game_details failed: {res}")
    return res


def get_board_string(gameId: str) -> dict:
    payload = f"type=boardString&gameId={gameId}"
    res = make_get_request(payload)
    print("get_board_string:", res)
    if res.get("code") != "OK":
        raise ValueError(f"get_board_string failed: {res}")
    return res


def get_board_map(gameId: str) -> dict:
    payload = f"type=boardMap&gameId={gameId}"
    res = make_get_request(payload)
    print("get_board_map:", res)
    if res.get("code") != "OK":
        raise ValueError(f"get_board_map failed: {res}")
    return res
