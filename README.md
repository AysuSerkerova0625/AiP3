#Generalized Tic Tac Toe (AI Project 3)

This project implements a generalized Tic Tac Toe game with an AI agent using the **Minimax algorithm with alpha-beta pruning**.

The game supports:
- Any board size `n x n`
- Winning condition of `m` in a row
- Local play (Human vs AI)
- Online play using API (AI vs another team)

---

## Project Structure
main.py          → Entry point to run the game
genT.py     → Game logic + AI (Minimax)
api.py           → API communication (for online mode)

##  How to Run

```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
python3 -m venv venv
source venv/bin/activate
```
### 1. Run the program
```
python3 main.py
```
---

### 2. Enter game settings

Example:
Select n, m: 3 3
---

### 3. Choose mode
1 - Local Human vs AI
2 - Online/API
---

## Mode 1: Local (Human vs AI)

- You play against the AI in the terminal  
- Enter moves like:
Enter row col: 1 2
---

## Mode 2: Online (API)

- Your AI plays against another team  
- You will be asked for:

Your team ID:
Opponent team ID:


- The game runs automatically (no manual input)

---

## API Setup

Before using online mode:

1. Go to:  
   https://www.notexponential.com  

2. Login and click:  
   **Keys**

3. Copy:
   - User ID  
   - API Key  

4. Paste them into `api.py`:

```python
USER_ID = "your_id"
API_KEY = "your_key"