from genT import GeneralizedTicTacToe
import api
import json


def main():
    print("Select mode:")
    print("1 - Local Human vs AI")
    print("2 - Online/API")

    mode = input("Enter mode: ").strip()

    if mode == "1":
        n, m = map(int, input("Select n, m: ").split())
        game = GeneralizedTicTacToe(n, m)
        game.human_vs_ai()

    elif mode == "2":
        team_id_1 = input("Enter your team ID: ").strip()
        team_id_2 = input("Enter opponent team ID: ").strip()
        game_id = input("Enter game ID: ").strip()

        details = api.get_game_details(game_id)

        if details.get("code") != "OK":
            print("Failed to fetch game details:", details)
            return

        if "game" not in details:
            print("Invalid game details response:", details)
            return

        try:
            # 🔥 FIX: use json.loads instead of ast
            game_info = details["game"]
           

            if isinstance(game_info, str):
                import json
                game_info = json.loads(game_info)
            else:
                game_info = game_info

            n = int(game_info["boardsize"])
            m = int(game_info["target"])

        except Exception as e:
            print("Could not parse game details:", details)
            print("Error:", e)
            return

        print(f"\nGame detected: {n}x{n}, target={m}")

        game = GeneralizedTicTacToe(n, m)
        game.ai_vs_online(team_id_1, team_id_2, game_id)

    else:
        print("Invalid mode selected.")


if __name__ == "__main__":
    main()
