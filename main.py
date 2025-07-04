import os
import json
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from scripts import request_site

app = FastAPI(
    title="99reviews API",
    description="API para coletar e retornar reviews do 99freelas",
    version="2.0.1",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)