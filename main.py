import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI, HTTPException, Request
from scripts import request_site
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import dotenv_values

config = dotenv_values(".env")

app = FastAPI(
    title="99reviews API",
    description="API para coletar e retornar reviews do 99freelas",
    version="3.0.0"
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"99reviews": "Made by: github.com/titiomathias"}


@app.post("/flag")
def read_root(password: str):
    if password == config["PASSWORD"]:
        return {"flag": config["FLAG"]}
    else:
        return {"status": 400, "message": "wrong password!"}


@app.get("/reviews", summary="Get Reviews", tags=["Reviews"])
def get_reviews():
    feedbacks = request_site.get_feedbacks()
    if "error" in feedbacks:
        raise HTTPException(status_code=500, detail=feedbacks["error"])
    return feedbacks


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)