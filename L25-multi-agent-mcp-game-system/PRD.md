# Product Requirements Document (PRD)
## Even or Odd Game League System

---

## 1. What Are We Building? 🎯

We're building a **computer game system** where robot players compete in an "Even or Odd" guessing game! Think of it like a mini sports league, but for computers instead of people.

**Simple Version:** Imagine a teacher organizing a tournament where students play a guessing game. That's what we're making, but with programs!

---

## 2. Why Are We Building This? 🤔

### Learning Goals:
- Learn how different programs talk to each other (like friends texting!)
- Understand how to organize competitions
- Practice building systems with multiple parts
- See how real-world apps work (like multiplayer games!)

### What Problem Does It Solve?
In real life, many systems need different programs to work together:
- Online games (players, servers, game masters)
- Banking systems (your app, bank server, payment checker)
- Social media (your phone, message server, friend's phone)

This project teaches you how to build that!

---

## 3. Who Will Use This? 👥

### Primary Users:
1. **Students** learning about distributed systems
2. **Developers** practicing server communication
3. **Teachers** demonstrating system architecture

### How They'll Use It:
- Run the programs on their computer
- Watch how messages flow between parts
- Learn how competitions are organized
- Modify the code to add new features

---

## 4. The Main Parts (Components) 🧩

### 4.1 Manager Component
**What It Does:** The boss who runs everything!

**Jobs:**
1. ✅ Register players who want to join
2. ✅ Register referees who can run games
3. ✅ Create a list of matches to play
4. ✅ Keep track of scores
5. ✅ Start matches one by one
6. ✅ Show final results

**Technical Details:**
- **File:** `manager.py`
- **Port:** 8000
- **Type:** FastAPI web server
- **Endpoints:** `/mcp` (receives all messages)

**Key Features:**
- Match queue system (list of upcoming games)
- Standings dictionary (score tracking)
- Background task system (starts games automatically)

### 4.2 Player Component
**What It Does:** A player in the game!

**Jobs:**
1. ✅ Register with the Manager when starting
2. ✅ Accept game invitations
3. ✅ Choose "even" or "odd" when asked
4. ✅ Use configuration file to get name and port

**Technical Details:**
- **File:** `player.py`
- **Ports:** Configurable (8100, 8102, etc.)
- **Type:** FastAPI web server
- **Configuration:** JSON files in `JSON/` folder

**Key Features:**
- Reads config from command line argument
- Random choice between "even" and "odd"
- Lifespan events (auto-registration on startup)

### 4.3 Referee Component
**What It Does:** Runs the actual games!

**Jobs:**
1. ✅ Register with the Manager when starting
2. ✅ Receive "start match" commands from Manager
3. ✅ Invite both players to the game
4. ✅ Collect each player's choice
5. ✅ Pick a random number (1-10)
6. ✅ Decide who wins
7. ✅ Report results to Manager

**Technical Details:**
- **File:** `referee.py`
- **Port:** 8002
- **Type:** FastAPI web server
- **Game Logic:** Even/Odd matching algorithm

**Key Features:**
- Random number generation (1-10)
- Winner determination logic
- Match result reporting

### 4.4 Shared Component
**What It Does:** Communication tools everyone uses!

**Jobs:**
1. ✅ Define message format (JSON-RPC)
2. ✅ Provide helper function to send messages
3. ✅ Store Manager's address

**Technical Details:**
- **File:** `shared.py`
- **Protocol:** JSON-RPC 2.0
- **Transport:** HTTP POST requests

**Key Features:**
- Request/Response models (Pydantic)
- Error handling
- Timeout protection (5 seconds)

---

## 5. How They Communicate (MCP Protocol) 📡

### What is MCP?
MCP is our name for the **Message Communication Protocol** - the rules for how our programs talk!

**Simple Explanation:** It's like a language all the parts understand. When they want to talk, they use special formatted messages.

### Message Format (JSON-RPC 2.0)

#### Request Message:
```json
{
    "jsonrpc": "2.0",
    "method": "register_player",
    "params": {
        "player_meta": {
            "display_name": "AnnaBot_1",
            "contact_endpoint": "http://localhost:8100/mcp"
        }
    },
    "id": 1
}
```

**What This Means:**
- **jsonrpc:** "We're using version 2.0 of JSON-RPC"
- **method:** "I want to do this action: register_player"
- **params:** "Here's the information you need"
- **id:** "This is message number 1"

#### Response Message:
```json
{
    "jsonrpc": "2.0",
    "result": {
        "status": "ACCEPTED",
        "player_id": "AnnaBot_1"
    },
    "id": 1
}
```

**What This Means:**
- **result:** "Here's what happened - you're accepted!"
- **id:** "This is the answer to message 1"

### Connection Map:

```
Component    →   Address                    →   What It Receives
------------------------------------------------------------------------
Manager      →   http://localhost:8000/mcp  →   register_player
                                                 register_referee
                                                 report_match_result

Player 1     →   http://localhost:8100/mcp  →   handle_game_invitation
                                                 choose_parity

Player 2     →   http://localhost:8102/mcp  →   handle_game_invitation
                                                 choose_parity

Referee      →   http://localhost:8002/mcp  →   start_match_command
```

---

## 6. The Flow (Step by Step) 🌊

### Phase 1: Startup (Everyone Joins!)

```
Step 1: User starts Manager
        → Manager runs and waits at port 8000

Step 2: User starts Referee
        → Referee sends: "register_referee" to Manager
        → Manager responds: "ACCEPTED"
        → Referee is ready!

Step 3: User starts Player 1
        → Player 1 reads JSON/player1.json
        → Player 1 sends: "register_player" to Manager
        → Manager responds: "ACCEPTED"
        → Manager has 1 player (needs 2 to start)

Step 4: User starts Player 2
        → Player 2 reads JSON/player2.json
        → Player 2 sends: "register_player" to Manager
        → Manager responds: "ACCEPTED"
        → Manager has 2 players! 🎉
        → Manager creates 3 matches in queue
        → Manager tells Referee: "start_match_command" for Match M1
```

### Phase 2: Playing a Match

```
Step 1: Referee receives start command
        → Match M1: AnnaBot_1 vs AnnaBot_2

Step 2: Referee invites players
        → Sends "handle_game_invitation" to Player 1
        → Sends "handle_game_invitation" to Player 2
        → Both accept (return {"accept": True})

Step 3: Referee asks for choices
        → Sends "choose_parity" to Player 1
        → Player 1 responds: {"choice": "even"}
        → Sends "choose_parity" to Player 2
        → Player 2 responds: {"choice": "odd"}

Step 4: Referee decides winner
        → Picks random number: 7
        → Checks: 7 is odd
        → Player 1 chose "even" (wrong)
        → Player 2 chose "odd" (correct)
        → Winner: AnnaBot_2!

Step 5: Referee reports to Manager
        → Sends "report_match_result"
        → Result: {"winner": "AnnaBot_2"}
        → Manager adds 3 points to AnnaBot_2
        → Manager starts next match!
```

### Phase 3: League Continues

```
Step 1: Manager starts Match M2
        → Same process repeats
        → New winner, points updated

Step 2: Manager starts Match M3
        → Same process repeats
        → Final match played!

Step 3: League Ends
        → No more matches in queue
        → Manager prints: "LEAGUE FINISHED"
        → Manager shows final standings
```

---

## 7. Features List ✨

### Must Have (✅ Already Built!):
1. ✅ Player registration system
2. ✅ Referee registration system
3. ✅ Match queue management
4. ✅ Score tracking (standings)
5. ✅ Automatic league progression
6. ✅ Even/Odd game logic
7. ✅ Random choice selection (players)
8. ✅ Random number generation (referee)
9. ✅ Winner determination
10. ✅ Multiple match support (league format)

### Nice to Have (Future Ideas! 🚀):
1. 🎯 Web dashboard to watch games
2. 🎯 More game types (rock-paper-scissors, etc.)
3. 🎯 More than 2 players per match
4. 🎯 Tournament bracket system
5. 🎯 Player statistics (wins, losses, win rate)
6. 🎯 Smart player strategies (not just random)
7. 🎯 Save/load league state
8. 🎯 Replay system
9. 🎯 Different point systems
10. 🎯 Time limits for decisions

---

## 8. Technical Requirements 🔧

### Software Needed:
- **Python:** Version 3.8 or newer
- **Libraries:**
  - `fastapi` - Web framework
  - `uvicorn` - Server runner
  - `requests` - HTTP communication
  - `pydantic` - Data validation

### Hardware Needed:
- **Computer:** Any modern PC/Mac/Linux
- **RAM:** 1GB minimum
- **Network:** All parts run on same computer (localhost)

### Ports Used:
- **8000:** Manager
- **8002:** Referee
- **8100:** Player 1
- **8102:** Player 2

---

## 9. Input/Output Examples 📊

### Input 1: Player Configuration File
**File:** `JSON/player1.json`
```json
{
    "name": "AnnaBot_1",
    "port": 8100
}
```
**What It Means:** "My name is AnnaBot_1 and I listen on port 8100"

### Input 2: Starting a Player
**Command:**
```bash
python player.py JSON/player1.json
```
**Output:**
```
Starting Player AnnaBot_1 on port 8100
Player AnnaBot_1 registering...
```

### Input 3: MCP Request (Player Registration)
**Sent to:** `http://localhost:8000/mcp`
```json
{
    "jsonrpc": "2.0",
    "method": "register_player",
    "params": {
        "player_meta": {
            "display_name": "AnnaBot_1",
            "contact_endpoint": "http://localhost:8100/mcp"
        }
    },
    "id": 1
}
```

**Response:**
```json
{
    "jsonrpc": "2.0",
    "result": {
        "status": "ACCEPTED",
        "player_id": "AnnaBot_1"
    },
    "id": 1
}
```

### Input 4: MCP Request (Choose Parity)
**Sent to:** `http://localhost:8100/mcp`
```json
{
    "jsonrpc": "2.0",
    "method": "choose_parity",
    "params": {
        "match_id": "M1"
    },
    "id": 1
}
```

**Response:**
```json
{
    "jsonrpc": "2.0",
    "result": {
        "choice": "even"
    },
    "id": 1
}
```

### Output: Final League Results
```
=== LEAGUE FINISHED ===
Final Standings: {'AnnaBot_1': 6, 'AnnaBot_2': 3}
```
**What It Means:** "AnnaBot_1 won with 6 points! AnnaBot_2 got 3 points."

---

## 10. Success Criteria ✅

### The System Works If:
1. ✅ All 4 components start without errors
2. ✅ Players successfully register with Manager
3. ✅ Referee successfully registers with Manager
4. ✅ League starts automatically with 2 players
5. ✅ All 3 matches are played
6. ✅ Winners are determined correctly
7. ✅ Points are tracked accurately
8. ✅ Final standings are displayed
9. ✅ No crashes or hanging
10. ✅ All MCP messages succeed

### Performance Goals:
- Each match completes in under 5 seconds
- No timeout errors
- Smooth progression through all matches

---

## 11. System Architecture 🏗️

### Architecture Type:
**Distributed Multi-Agent System**

### Pattern Used:
**Client-Server with Message Passing**

### Diagram:
```
                    ┌─────────────┐
                    │   MANAGER   │
                    │  (Port 8000)│
                    │   The Boss  │
                    └──────┬──────┘
                           │
                           │ MCP Messages
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ PLAYER 1 │    │ PLAYER 2 │    │ REFEREE  │
    │(Port 8100│    │(Port 8102│    │(Port 8002│
    │AnnaBot_1)│    │AnnaBot_2)│    │  Ref1)   │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                    MCP Messages
                  (during matches)
```

### Communication Protocol Stack:
```
Application Layer:    Game Logic (even/odd, winner selection)
Protocol Layer:       JSON-RPC 2.0 (MCP)
Transport Layer:      HTTP POST
Network Layer:        TCP/IP (localhost)
```

---

## 12. Error Handling 🛡️

### What Could Go Wrong:

1. **Connection Errors:**
   - Problem: Manager not started yet
   - Solution: Start Manager first, then others
   - Code: Try-except blocks with error messages

2. **Timeout Errors:**
   - Problem: A component doesn't respond
   - Solution: 5-second timeout in requests
   - Code: `timeout=5` in `send_mcp_request()`

3. **Port Already Used:**
   - Problem: Another program using the port
   - Solution: Change port in config file
   - Code: User must close conflicting program

4. **Invalid Choice:**
   - Problem: Player sends wrong choice
   - Solution: Only "even" or "odd" accepted
   - Code: Random choice ensures valid options

---

## 13. Future Improvements 🚀

### Phase 2 Features:
1. **Web Interface:** See games in browser
2. **Player Strategies:** Smart players that learn
3. **More Games:** Different game types
4. **Statistics:** Track win rates and history

### Phase 3 Features:
1. **Multiplayer:** More than 2 players
2. **Tournaments:** Brackets and elimination
3. **Persistence:** Save and load games
4. **Network Play:** Play over real internet

---

## 14. Testing Guide 🧪

### How to Test:

**Test 1: Basic Flow**
```
1. Start Manager → Should print "Starting"
2. Start Referee → Should print "Registered successfully"
3. Start Player 1 → Should print "Player registered"
4. Start Player 2 → Should print "Player registered" + "League initialized"
5. Wait → Should see 3 matches played
6. Check → Should see "LEAGUE FINISHED" with standings
```

**Test 2: Winner Logic**
```
Scenario 1: Both choose odd, number is 7 (odd)
Expected: DRAW (both correct)

Scenario 2: P1 chooses even, P2 chooses odd, number is 6 (even)
Expected: P1 wins (only P1 correct)

Scenario 3: P1 chooses even, P2 chooses even, number is 3 (odd)
Expected: DRAW (both wrong)
```

**Test 3: Score Tracking**
```
1. Player wins Match 1 → Gets 3 points
2. Same player wins Match 2 → Gets 6 points total
3. Other player wins Match 3 → First player still has 6, second has 3
```

---

## 15. Glossary 📖

**Simple Definitions:**

- **MCP:** Message Communication Protocol - How our programs talk
- **JSON-RPC:** A format for sending messages (like a letter template)
- **Port:** A number that identifies a program (like an apartment number)
- **Localhost:** Your own computer (not the internet)
- **FastAPI:** A Python tool for making web servers
- **Endpoint:** A specific address where messages go (like `/mcp`)
- **Match Queue:** A waiting line of games to play
- **Standings:** The scoreboard showing points
- **Lifespan:** Code that runs when a program starts/stops
- **Background Task:** Work happening "behind the scenes"
- **Parity:** Whether a number is even or odd

---

## 16. Connection Between MCP and Players 🔗

### The Magic of MCP Communication:

**Think of it like a phone system:**

1. **Everyone has a phone number (URL):**
   - Manager: 8000
   - Player 1: 8100
   - Player 2: 8102
   - Referee: 8002

2. **Everyone speaks the same language (JSON-RPC):**
   - When Player 1 calls Manager, they use proper format
   - Manager understands and replies in same format
   - It's like everyone speaking English (not confusing French/Spanish/etc.)

3. **Each phone has specific functions (methods):**
   - Call Manager → Can do: register_player, register_referee, report_match_result
   - Call Player → Can do: handle_game_invitation, choose_parity
   - Call Referee → Can do: start_match_command

4. **Messages get delivered and answered:**
   - Player sends: "register_player" → Manager receives → Manager sends back: "ACCEPTED"
   - It's like: You call pizza shop → Order pizza → They say "OK, 30 minutes!"

### Why MCP Makes This Work:

**Without MCP:**
- Programs would need to guess how to talk
- Messages could be misunderstood
- No standard format = chaos!

**With MCP:**
- Clear rules for messages
- Everyone knows what to expect
- Reliable communication
- Easy to add new features

**Real-World Example:**
```
Player wants to join:
1. Player creates message: "I'm AnnaBot_1, my address is localhost:8100"
2. Player sends to Manager using MCP format
3. MCP ensures message arrives correctly
4. Manager reads message (knows format thanks to MCP)
5. Manager records player
6. Manager creates reply: "ACCEPTED, your ID is AnnaBot_1"
7. Reply sent back using MCP format
8. Player receives confirmation
9. Player is now registered! ✨
```

---

## 17. Project Status 📊

**Current Version:** 1.0
**Status:** ✅ Fully Functional
**Last Updated:** December 2024

**What Works:**
- ✅ All core features implemented
- ✅ 3-match league system
- ✅ Automatic progression
- ✅ Score tracking
- ✅ Winner determination

**Known Limitations:**
- Only 2 players supported
- Only 1 game type (even/odd)
- No GUI (text only)
- No persistence (resets on restart)

---

## 18. Conclusion 🎓

This project demonstrates a **real distributed system** where multiple programs work together through message passing. It's simple enough to understand, but uses the same patterns as real-world applications like:

- Online multiplayer games
- Chat applications
- Banking systems
- E-commerce platforms

By building this, you learn:
- How servers communicate
- How to organize competitions
- How to handle async operations
- Real software architecture

**Most Important:** You learn that building complex systems is just like building with LEGO - you create small pieces that work together! 🧩

---

**Happy Coding!** 🚀✨
