# referee.py
import uvicorn
import random
from fastapi import FastAPI
from contextlib import asynccontextmanager
from shared import JSONRPCRequest, JSONRPCResponse, send_mcp_request, MANAGER_URL

MY_PORT = 8002
MY_URL = f"http://localhost:{MY_PORT}/mcp"

# --- Lifespan Logic (מחליף את on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # קוד שרץ בעלייה (Startup)
    print(f"Referee starting on port {MY_PORT}...")
    try:
        # ניסיון הרשמה למנהל
        response = send_mcp_request(MANAGER_URL, "register_referee", {
            "referee_meta": {"display_name": "Ref1", "contact_endpoint": MY_URL}
        })
        if response:
            print(f"Registered successfully: {response}")
        else:
            print("Failed to register (No response from Manager)")
    except Exception as e:
        print(f"Connection error during registration: {e}")
    
    yield # כאן השרת רץ
    
    # קוד שרץ בירידה (Shutdown) - כרגע לא נדרש
    print("Referee shutting down...")

app = FastAPI(lifespan=lifespan)

# --- MCP Handler ---
@app.post("/mcp")
async def handle_mcp(req: JSONRPCRequest):
    if req.method == "start_match_command":
        # המנהל פוקד על השופט להתחיל משחק
        p_a = req.params["player_a"]
        p_b = req.params["player_b"]
        url_a = req.params["player_a_url"]
        url_b = req.params["player_b_url"]
        m_id = req.params["match_id"]
        
        # הרצת המשחק
        run_match(m_id, p_a, url_a, p_b, url_b)
        return JSONRPCResponse(result={"status": "STARTED"})
    
    return JSONRPCResponse(result={"error": "Method not found"})

# --- Game Logic ---
def run_match(m_id, id_a, url_a, id_b, url_b):
    print(f"--- Starting Match {m_id}: {id_a} vs {id_b} ---")
    
    # שלב 1: הזמנה (Game Invitation)
    # הערה: בתרגיל מלא היינו בודקים את התשובה (ACK), כאן מניחים שהיא חיובית
    send_mcp_request(url_a, "handle_game_invitation", {"match_id": m_id, "opponent": id_b})
    send_mcp_request(url_b, "handle_game_invitation", {"match_id": m_id, "opponent": id_a})
    
    # שלב 2: איסוף בחירות (Collect Choices)
    # אנו מצפים לתשובה במבנה: {"result": {"choice": "even"}}
    resp_a = send_mcp_request(url_a, "choose_parity", {"match_id": m_id})
    resp_b = send_mcp_request(url_b, "choose_parity", {"match_id": m_id})
    
    choice_a = resp_a["result"]["choice"] if resp_a else "none"
    choice_b = resp_b["result"]["choice"] if resp_b else "none"
    
    # שלב 3: הגרלה וקביעת מנצח
    number = random.randint(1, 10)
    parity = "even" if number % 2 == 0 else "odd"
    
    winner = "DRAW"
    
    # לוגיקה: אם יצא זוגי - מי שבחר זוגי מנצח (אם השני לא בחר גם זוגי)
    is_a_correct = (choice_a == parity)
    is_b_correct = (choice_b == parity)
    
    if is_a_correct and not is_b_correct:
        winner = id_a
    elif is_b_correct and not is_a_correct:
        winner = id_b
    # אחרת (שניהם צדקו או שניהם טעו) -> תיקו
    
    print(f"Number drawn: {number} ({parity})")
    print(f"{id_a} chose: {choice_a}, {id_b} chose: {choice_b} -> Winner: {winner}")

    # שלב 4: דיווח למנהל
    send_mcp_request(MANAGER_URL, "report_match_result", {
        "result": {
            "winner": winner,
            "score": {id_a: choice_a, id_b: choice_b} # דיווח בחירות לצרכי לוג
        }
    })

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=MY_PORT)