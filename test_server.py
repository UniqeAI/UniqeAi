#!/usr/bin/env python3
"""
Simple test server to verify FastAPI is working
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Test Server", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "✅ Test server is working!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy", "message": "Server is running"}

if __name__ == "__main__":
    print("🚀 Starting test server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🩺 Health check: http://localhost:8000/health")
    uvicorn.run("test_server:app", host="0.0.0.0", port=8000, reload=True)
