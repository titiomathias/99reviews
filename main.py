import os
import json
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI, HTTPException, Request
from scripts import request_site
from slowapi import Limiter
from slowapi.util import get_remote_address

BLACKLIST_FILE = "ip_blacklist.json"

def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as f:
            return json.load(f)
    return []

def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, 'w') as f:
        json.dump(blacklist, f)

def add_to_blacklist(ip_address):
    blacklist = load_blacklist()
    if ip_address not in blacklist:
        blacklist.append(ip_address)
        save_blacklist(blacklist)

app = FastAPI(
    title="99reviews API",
    description="API para coletar e retornar reviews do 99freelas",
    version="2.0.1",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

logging.basicConfig(filename='api_security.log', level=logging.WARNING)

@app.middleware("http")
async def log_suspicious_requests(request: Request, call_next):
    response = await call_next(request)
    client_host = request.client.host
    if response.status_code in (403, 429, 401):
        logging.warning(f"Suspicious request from {client_host} to {request.url}")
    return response


@app.middleware("http")
async def check_blacklist(request: Request, call_next):
    client_ip = request.client.host
    blacklist = load_blacklist()
    
    if client_ip in blacklist:
        logging.warning(f"Blacklisted IP tried to access: {client_ip}")
        raise HTTPException(
            status_code=403,
            detail="Seu IP foi banido permanentemente. Boa sorte tentando acessar de novo :)"
        )
    
    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"99reviews": "Made by: github.com/titiomathias"}


@app.get("/reviews", summary="Get Reviews", tags=["Reviews"])
def get_reviews():
    feedbacks = request_site.get_feedbacks()
    if "error" in feedbacks:
        raise HTTPException(status_code=500, detail=feedbacks["error"])
    return feedbacks


@app.post("/admin")
@limiter.limit("10/minute")
def admin(request: Request, password: str):
    client_ip = request.client.host

    if password == "admin":
        add_to_blacklist(client_ip)
        logging.critical(f"Honeypot triggered by IP: {client_ip}")
        return {
            "logged": "Olá, lammerzinho! Você conseguiu. Agora seu IP está BANIDO para toda a eternidade. :)",
            "your_ip": client_ip,
            "status": "BANNED"
        }
    else:
        raise HTTPException(status_code=400, detail="Boa tentativa. Continua assim. Daqui há uns mil anos você consegue, se bem que... acho que nem com todo esse tempo alguém burro como você conseguiria permissão de administrador. :)")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)