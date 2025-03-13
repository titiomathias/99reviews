from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from scripts import request_site
import uvicorn

app = FastAPI(
    title="99reviews API",
    description="API para coletar e retornar reviews do 99freelas",
    version="1.0.0"
)

app.add_middleware(
        CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)