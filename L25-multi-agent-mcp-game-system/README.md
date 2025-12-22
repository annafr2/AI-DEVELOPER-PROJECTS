# Even or Odd Game League 🎲

## What is This?

Imagine you're playing a guessing game with your friends! You need to guess if a mystery number will be **even** (like 2, 4, 6) or **odd** (like 1, 3, 5). That's exactly what this project does, but with computer programs playing instead of people!

## The Game Parts (Like LEGO Blocks!)

### 1. The Manager 👔
**File:** `manager.py`

Think of the Manager as the **teacher** who organizes everything:
- Writes down who wants to play (registers players)
- Writes down who will be the referee
- Creates a list of games to play (match queue)
- Keeps track of scores (standings)
- Announces the final winner!

**Port:** Runs on `localhost:8000`

### 2. The Players 🎮
**File:** `player.py`

Players are like **kids playing the game**:
- Each player gets a name (like "AnnaBot_1" or "AnnaBot_2")
- When asked, they choose either "even" or "odd"
- They accept invitations to play games
- Each player runs on their own port (like having their own phone number!)

**Example Players:**
- Player 1: AnnaBot_1 on port `8100`
- Player 2: AnnaBot_2 on port `8102`

### 3. The Referee 🏆
**File:** `referee.py`

The Referee is like the **game master**:
- Invites both players to a match
- Asks each player to choose "even" or "odd"
- Picks a random number between 1 and 10
- Checks who guessed correctly
- Tells the Manager who won

**Port:** Runs on `localhost:8002`

### 4. The Shared Tools 🔧
**File:** `shared.py`

This file has the **rules for talking** between all the programs:
- How to send messages (JSON-RPC format)
- How to receive answers
- Where the Manager lives (URL)

## How Do They Talk? (MCP Connection) 📞

**MCP** means everyone talks using special messages, like sending letters!

### The MCP Communication Flow:

```
1. STARTUP (Everyone says "Hello!")
   Player 1 → Manager: "Hi! I'm AnnaBot_1, I want to play!"
   Player 2 → Manager: "Hi! I'm AnnaBot_2, I want to play!"
   Referee  → Manager: "Hi! I'm Ref1, I can run games!"

2. GAME START (Manager organizes games)
   Manager → Referee: "Start Match M1 between AnnaBot_1 and AnnaBot_2!"

3. INVITATION (Referee invites players)
   Referee → Player 1: "You're invited to play against AnnaBot_2!"
   Referee → Player 2: "You're invited to play against AnnaBot_1!"

4. CHOICE TIME (Players make their picks)
   Referee → Player 1: "Choose: even or odd?"
   Player 1 → Referee: "I choose even!"
   Referee → Player 2: "Choose: even or odd?"
   Player 2 → Referee: "I choose odd!"

5. RESULT (Referee decides winner)
   Referee draws number: 7 (odd!)
   Referee → Manager: "Player 2 won! They chose odd and the number was 7!"

6. NEXT GAME (Manager starts next match)
   Manager → Referee: "Start Match M2 between AnnaBot_1 and AnnaBot_2!"
```

### How MCP Works (Super Simple!)

Every message is sent to a special address called `/mcp` using the internet:
- **Manager:** `http://localhost:8000/mcp`
- **Player 1:** `http://localhost:8100/mcp`
- **Player 2:** `http://localhost:8102/mcp`
- **Referee:** `http://localhost:8002/mcp`

It's like everyone has their own mailbox!

## How to Run the Game 🚀

### Step 1: Start the Manager
```bash
python manager.py
```
The Manager starts and waits for players and referees to join.

### Step 2: Start the Referee
```bash
python referee.py
```
The Referee registers with the Manager.

### Step 3: Start Player 1
```bash
python player.py JSON/player1.json
```
Player 1 (AnnaBot_1) joins the game!

### Step 4: Start Player 2
```bash
python player.py JSON/player2.json
```
Player 2 (AnnaBot_2) joins the game! **The league starts automatically!**

## What You'll See 👀

### Manager Window:
```
Player registered: AnnaBot_1
Player registered: AnnaBot_2
Referee registered: Ref1
League initialized with 3 matches.
--- Triggering Match M1 ---
Match Result Processed. Current Standings: {'AnnaBot_2': 3}
--- Triggering Match M2 ---
Match Result Processed. Current Standings: {'AnnaBot_2': 6}
--- Triggering Match M3 ---
Match Result Processed. Current Standings: {'AnnaBot_1': 3, 'AnnaBot_2': 6}
=== LEAGUE FINISHED ===
Final Standings: {'AnnaBot_1': 3, 'AnnaBot_2': 6}
```

### Referee Window:
```
--- Starting Match M1: AnnaBot_1 vs AnnaBot_2 ---
Number drawn: 7 (odd)
AnnaBot_1 chose: even, AnnaBot_2 chose: odd -> Winner: AnnaBot_2
```

### Player Windows:
```
Player AnnaBot_1 registering...
Invited to match against AnnaBot_2
Asking for move... I chose: even
```

## Game Rules 📜

1. **Choosing:** Each player picks "even" or "odd"
2. **Drawing:** Referee picks a random number (1-10)
3. **Winning:**
   - If the number is even and YOU chose even (but opponent didn't) → You win! 🎉
   - If the number is odd and YOU chose odd (but opponent didn't) → You win! 🎉
   - If both chose right OR both chose wrong → It's a tie! 🤝
4. **Points:** Winner gets 3 points
5. **League:** Play 3 matches, highest score wins!

## Example Game 🎯

**Match 1:**
- AnnaBot_1 chooses: "even"
- AnnaBot_2 chooses: "odd"
- Referee draws: **7** (odd)
- **Winner:** AnnaBot_2 (gets 3 points!)

**Match 2:**
- AnnaBot_1 chooses: "odd"
- AnnaBot_2 chooses: "odd"
- Referee draws: **4** (even)
- **Winner:** DRAW (nobody chose right!)

**Match 3:**
- AnnaBot_1 chooses: "even"
- AnnaBot_2 chooses: "odd"
- Referee draws: **6** (even)
- **Winner:** AnnaBot_1 (gets 3 points!)

**Final Score:**
- AnnaBot_1: 3 points
- AnnaBot_2: 3 points
- It's a tie!

## Input Examples 📝

### Player Configuration (JSON/player1.json):
```json
{
    "name": "AnnaBot_1",
    "port": 8100
}
```

This tells the player:
- **name:** "My name is AnnaBot_1"
- **port:** "I listen on port 8100"

### Player Configuration (JSON/player2.json):
```json
{
    "name": "AnnaBot_2",
    "port": 8102
}
```

## File Structure 📁

```
D25/
├── manager.py          # The boss who organizes everything
├── player.py           # The player program (run twice for 2 players)
├── referee.py          # The game master who runs matches
├── shared.py           # Communication tools everyone uses
└── JSON/
    ├── player1.json    # Config for Player 1
    └── player2.json    # Config for Player 2
```

## Requirements 📦

You need these Python packages (libraries) to run the game:
- `fastapi` - For creating web servers
- `uvicorn` - For running the servers
- `requests` - For sending messages between programs
- `pydantic` - For organizing data nicely

Install with:
```bash
pip install fastapi uvicorn requests pydantic
```

## Troubleshooting 🔧

**Problem:** "Connection error during registration"
**Solution:** Make sure you start the Manager FIRST, then others!

**Problem:** "Address already in use"
**Solution:** Another program is using that port. Close it or change the port number!

**Problem:** "League doesn't start"
**Solution:** You need at least 1 referee and 2 players. Make sure all are running!

## How It All Connects (The Big Picture) 🌟

```
        MANAGER (The Boss)
       /       |        \
      /        |         \
PLAYER 1   PLAYER 2    REFEREE
(AnnaBot_1) (AnnaBot_2) (Ref1)
     \         /          /
      \       /          /
       \     /          /
        \   /          /
         MCP Messages (Like sending letters!)
```

Everyone talks through MCP messages:
- Players tell Manager "I want to play!"
- Manager tells Referee "Start a game!"
- Referee asks Players "Choose even or odd!"
- Referee tells Manager "Here's who won!"
- Manager tells Referee "Start the next game!"

It's like a dance where everyone knows their steps! 💃🕺

## Fun Facts 🎈

- The game plays 3 matches automatically (you can change this in `manager.py` line 22!)
- Players choose randomly between "even" and "odd" (look at `player.py` line 43!)
- The referee picks numbers from 1 to 10 (check `referee.py` line 70!)
- Winners get 3 points (like in soccer/football!)

## What Can We Add Later? 🚀

### Playing with External Players (Over the Internet!)

Right now, all our programs run on the same computer (localhost). But in the future, **we can have players from anywhere in the world!**

**Why is this possible?**
- Our MCP system uses **web addresses (URLs)** to talk
- Currently we use: `http://localhost:8100` (same computer)
- We could use: `http://anna-computer.com:8100` (different computer!)

**Example:**
```
Before (All on same computer):
Player 1: http://localhost:8100
Player 2: http://localhost:8102
Manager: http://localhost:8000

After (Players anywhere!):
Player 1: http://player1.germany.com:8100  🇩🇪
Player 2: http://player2.japan.com:8102    🇯🇵
Manager: http://game-server.usa.com:8000   🇺🇸
```

**What You'd Need:**
- Real internet addresses (not localhost)
- Open ports on your router
- Maybe a cloud server (like AWS, Azure, or Google Cloud)
- Security (passwords, encryption) to keep it safe!

**Why This Works:**
The MCP messages are just **HTTP requests** - the same thing your web browser uses! If you can visit a website, you can send MCP messages to it. That's the magic! ✨

### Playing Different Games with Different Strategies

Right now we only play "Even or Odd" with random choices. But we can add **many different games!**

**Why is this possible?**
- The **structure is flexible** - Manager, Players, and Referee can handle any game
- Only the **game rules** need to change (in referee.py)
- Only the **strategy** needs to change (in player.py)

**Example Games We Could Add:**

1. **Rock, Paper, Scissors** 🪨📄✂️
   ```
   Player chooses: "rock", "paper", or "scissors"
   Referee compares choices
   Winner determined by: rock beats scissors, etc.
   ```

2. **Number Guessing Game** 🔢
   ```
   Referee picks secret number 1-100
   Players guess numbers
   Referee says "higher" or "lower"
   First to guess wins!
   ```

3. **Tic-Tac-Toe** ❌⭕
   ```
   Players take turns choosing positions
   Referee tracks the board
   First to get 3 in a row wins!
   ```

**Different Strategies We Could Add:**

Right now, players choose **randomly**. But we could make them smarter!

**1. Pattern Strategy** 🧠
```python
# Instead of random choice
choice = random.choice(["even", "odd"])

# Smart strategy: alternate choices
if last_choice == "even":
    choice = "odd"
else:
    choice = "even"
```

**2. Learning Strategy** 🎓
```python
# Remember what opponent chose before
# If they often choose "even", we choose "odd"
if opponent_history.count("even") > opponent_history.count("odd"):
    choice = "odd"  # Counter their pattern!
```

**3. Probability Strategy** 📊
```python
# Use math to calculate best choice
# Based on past game results
win_rate_even = wins_with_even / total_even_choices
win_rate_odd = wins_with_odd / total_odd_choices
choice = "even" if win_rate_even > win_rate_odd else "odd"
```

**Why Adding Strategies is Easy:**
- All the **communication code stays the same** (MCP messages)
- Only change the **choice logic** in `player.py` line 43
- The Manager and Referee don't care HOW players decide
- They just care that players send "even" or "odd"

**Why This Architecture is Powerful:**
```
SEPARATE CONCERNS:
├── Manager: Organizes games (doesn't care about game rules)
├── Referee: Runs games (doesn't care about player strategy)
└── Player: Makes choices (doesn't care about other players)

This is called "MODULAR DESIGN" - each part does ONE job!
```

**Real-World Example:**
Think about online poker:
- The **server** (Manager) organizes tables
- The **dealer** (Referee) deals cards and decides winners
- The **players** (Players) make betting decisions with their own strategies
- Some players are beginners (random choices)
- Some players are experts (smart strategies)
- But they all use the **same communication system**!

That's exactly what we built! 🎉

### Future Enhancement Ideas:

**Easy to Add:** ⭐
- More player bots with different strategies
- Different game types (rock-paper-scissors)
- Statistics dashboard (who wins most?)
- Save game history to a file

**Medium Difficulty:** ⭐⭐
- Web interface to watch games in browser
- Multiple games running at same time
- Tournament brackets (winner advances)
- Player rankings (ELO system)

**Advanced:** ⭐⭐⭐
- Machine learning players (AI that learns!)
- Real internet play (external players)
- Mobile app for players
- Database for storing everything
- Live streaming of matches

## What Makes This Cool? ✨

This project shows you how to build a **distributed system** - that's when different programs work together by talking to each other, just like a team! You learn:
- How servers communicate (MCP/JSON-RPC)
- How to organize a competition (queue, standings)
- How to make programs work together
- Real-world architecture patterns
- **Why this architecture makes it easy to add external players and new games!**

The best part? Because we used **modular design**, you can:
- Change ONE part without breaking others
- Add new games without rewriting everything
- Connect players from anywhere in the world
- Test different strategies easily

This is how real software is built! 🏗️

Have fun playing! 🎮🎉
