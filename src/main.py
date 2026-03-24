from genT import GeneralizedTicTacToe


if __name__ == "__main__":
    n, m = map(int, input("Select n, m: ").split())
    game = GeneralizedTicTacToe(n, m)

    print("Select mode:")
    print("1 - Local Human vs AI")
    print("2 - Online/API")

    mode = input("Enter mode: ").strip()

    if mode == "1":
        game.human_vs_ai()

    elif mode == "2":
        team_id_1 = input("Enter your team ID: ").strip()
        team_id_2 = input("Enter opponent team ID: ").strip()
        game.ai_vs_online(team_id_1, team_id_2)

    else:
        print("Invalid mode.")
