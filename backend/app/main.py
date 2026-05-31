from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import api_router

app = FastAPI(
    title="Recall IO API", description="Backend API for Recall IO", version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React server
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "RecallIO up and running."}
