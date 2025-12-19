# player.py
import sys, json, random, uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager # ייבוא חדש
from shared import JSONRPCRequest, JSONRPCResponse, send_mcp_request, MANAGER_URL

if len(sys.argv) < 2:
    print("Usage: python player.py <config_file>")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    config = json.load(f)

MY_ID = config["name"]
MY_PORT = config["port"]
MY_URL = f"http://localhost:{MY_PORT}/mcp"

# זה מחליף את @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # קוד שרץ בעלייה
    print(f"Player {MY_ID} registering...")
    try:
        send_mcp_request(MANAGER_URL, "register_player", {
            "player_meta": {"display_name": MY_ID, "contact_endpoint": MY_URL}
        })
    except Exception as e:
        print(f"Failed to register: {e}")
    yield
    # כאן יכול לבוא קוד שרץ בירידה (shutdown)

app = FastAPI(lifespan=lifespan) # חיבור ה-lifespan לאפליקציה

@app.post("/mcp")
async def handle_mcp(req: JSONRPCRequest):
    method = req.method
    
    if method == "handle_game_invitation":
        print(f"Invited to match against {req.params.get('opponent')}")
        return JSONRPCResponse(result={"accept": True})
    
    elif method == "choose_parity":
        choice = random.choice(["even", "odd"])
        print(f"Asking for move... I chose: {choice}")
        return JSONRPCResponse(result={"choice": choice})

    return JSONRPCResponse(result={"error": "Unknown method"})

if __name__ == "__main__":
    print(f"Starting Player {MY_ID} on port {MY_PORT}")
    uvicorn.run(app, host="localhost", port=MY_PORT)