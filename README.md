# Generalized Tic Tac Toe (AI Project 3)

This project implements a generalized Tic Tac Toe game with an AI agent using the **Minimax algorithm with alpha-beta pruning**.

The game supports:
- Any board size `n x n`
- Winning condition of `m` in a row
- Local play (Human vs AI)
- Online play using API (AI vs another team)

---

## Project Structure
main.py          → Entry point to run the game <br>
genT.py     → Game logic + AI (Minimax) <br>
api.py           → API communication (for online mode) <br>

##  How to Run

```
git clone https://github.com/AysuSerkerova0625/AiP3
cd src
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


### 3. Choose mode
1 - Local Human vs AI <br>
2 - Online/API
<br>



## Mode 1: Local (Human vs AI)
- You play against the AI in the terminal  
- Enter moves like:
<br>
Enter row col: 1 2

## Mode 2: Online (API)

- Your AI plays against another team  
- You will be asked for:

    Your team ID: <br>
    Opponent team ID:


- The game runs automatically (no manual input)


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
```
## Code Explanation

### 1. Game Representation
The board is stored as a 2D grid:
- `"X"` → Player 1  
- `"O"` → Player 2  
- `"."` → Empty  

The game supports any size `n × n` and a win condition of `m` in a row.

---

### 2. Game Logic
The system:
- Tracks available moves (empty cells)
- Applies moves and switches turns
- Checks for a winner in 4 directions:
  - Horizontal
  - Vertical
  - Diagonal
  - Anti-diagonal
- Detects terminal states (win or draw)

---

### 3. AI Decision-Making (Minimax)
The AI uses the **Minimax algorithm** to simulate future moves and choose the best one.

- Maximizes its own score  
- Minimizes opponent’s score  
- Uses **alpha-beta pruning** to skip unnecessary branches and improve performance  

---

### 4. Heuristic Evaluation
When full search is not possible, the AI evaluates the board based on:
- Length of its own sequences (good)
- Opponent sequences (dangerous)
- Open spaces for future moves
- Position (center control is preferred)

---

### 5. Online Mode (API)
In online play, the system:
1. Fetches all moves from the server  
2. Reconstructs the board from move history  
3. Checks whose turn it is  
4. If it’s the AI’s turn → selects and sends a move  
5. Otherwise → waits for opponent  

This ensures the local board always matches the server state.

---

### 6. API Communication
The `api.py` module:
- Sends requests to the game server  
- Retrieves game details and moves  
- Submits moves  
- Handles retries and parsing issues  

This allows real-time gameplay between teams.