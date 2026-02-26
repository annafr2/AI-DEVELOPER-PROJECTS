# shared.py
from pydantic import BaseModel
from typing import Dict, Any, Optional

# הגדרת פורטים זוגיים כבקשתך
MANAGER_URL = "http://localhost:8000/mcp"

class JSONRPCRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any]
    id: int = 1

class JSONRPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: int = 1

# פונקציית עזר לשליחת הודעות
import requests
def send_mcp_request(url: str, method: str, params: dict):
    payload = JSONRPCRequest(method=method, params=params).dict()
    try:
        resp = requests.post(url, json=payload, timeout=5)
        return resp.json()
    except Exception as e:
        print(f"Error communicating with {url}: {e}")
        return None