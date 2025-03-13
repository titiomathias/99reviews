from fastapi import FastAPI, HTTPException
from scripts import request_site

app = FastAPI(
    title="99reviews API",
    description="API para coletar e retornar reviews do 99freelas",
    version="1.0.0"
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