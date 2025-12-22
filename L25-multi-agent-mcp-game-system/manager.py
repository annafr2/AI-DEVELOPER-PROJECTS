# manager.py מעודכן לריבוי סבבים
from fastapi import FastAPI, BackgroundTasks
from shared import JSONRPCRequest, JSONRPCResponse, send_mcp_request
import uvicorn
import time

app = FastAPI()
players = {}
referees = {}
standings = {}

# תור המשחקים העתידיים
match_queue = []

def start_league_task():
    time.sleep(1.5) # השהייה לוודא שכולם עלו
    
    if len(referees) >= 1 and len(players) >= 2:
        p_ids = list(players.keys())
        # יצירת סדרת משחקים (למשל 3 סבבים)
        # כאן אנחנו יוצרים רשימה של משחקים שנרצה להריץ
        for i in range(1, 4): # Rounds 1, 2, 3
            match_queue.append({
                "match_id": f"M{i}", 
                "player_a": p_ids[0], 
                "player_a_url": players[p_ids[0]],
                "player_b": p_ids[1], 
                "player_b_url": players[p_ids[1]]
            })
        
        print(f"League initialized with {len(match_queue)} matches.")
        play_next_match()

def play_next_match():
    # אם נשארו משחקים בתור, נשלח את הבא לשופט
    if match_queue:
        next_match = match_queue.pop(0) # שולף את הראשון
        ref_url = list(referees.values())[0]
        
        print(f"--- Triggering Match {next_match['match_id']} ---")
        send_mcp_request(ref_url, "start_match_command", next_match)
    else:
        print("=== LEAGUE FINISHED ===")
        print(f"Final Standings: {standings}")

@app.post("/mcp")
async def handle_request(req: JSONRPCRequest, background_tasks: BackgroundTasks):
    method = req.method
    params = req.params
    
    if method == "register_player":
        p_id = params["player_meta"]["display_name"]
        players[p_id] = params["player_meta"]["contact_endpoint"]
        if p_id not in standings: standings[p_id] = 0
        print(f"Player registered: {p_id}")
        
        # מתחילים רק אם יש מספיק שחקנים ועדיין לא התחלנו
        if len(players) == 2: 
             background_tasks.add_task(start_league_task)
        
        return JSONRPCResponse(result={"status": "ACCEPTED", "player_id": p_id})

    elif method == "register_referee":
        r_id = params["referee_meta"]["display_name"]
        referees[r_id] = params["referee_meta"]["contact_endpoint"]
        print(f"Referee registered: {r_id}")
        return JSONRPCResponse(result={"status": "ACCEPTED", "referee_id": r_id})

    elif method == "report_match_result":
        # 1. עדכון ניקוד
        winner = params["result"]["winner"]
        if winner != "DRAW":
            standings[winner] = standings.get(winner, 0) + 3
        
        print(f"Match Result Processed. Current Standings: {standings}")
        
        # 2. הטריגר למשחק הבא!
        # ברגע שהשופט מדווח שהמשחק נגמר, המנהל מפעיל את המשחק הבא בתור
        background_tasks.add_task(play_next_match)
        
        return JSONRPCResponse(result={"status": "OK"})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)