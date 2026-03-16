"""
MedSeg AI Platform - Backend API Server
FastAPI application initialization and configuration
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables từ .env file
load_dotenv()

# Import routers
from app.routers import health

# Tạo FastAPI app instance
app = FastAPI(
    title="MedSeg AI Platform API",
    description="Medical Image Segmentation Platform Backend API",
    version="0.1.0"
)

# ========== CORS Configuration ==========
# Cho phép frontend có thể gọi API từ localhost:3000
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

if os.getenv("ENV") == "development":
    ALLOWED_ORIGINS.append("*")  # Allow all origins in development

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Include Routers ==========
app.include_router(health.router)

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint - thông tin về API
    """
    return {
        "name": "MedSeg AI Platform API",
        "version": "0.1.0",
        "status": "running"
    }

if __name__ == "__main__":
    # Nếu run file trực tiếp
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
