"""
Health check router untuk kiểm tra server hoạt động
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/api/v1/health",
    tags=["health"],
)


@router.get("")
def health_check():
    """
    Health check endpoint - kiểm tra server đang chạy
    Trả về status: ok nếu server hoạt động
    """
    return {
        "status": "ok",
        "message": "MedSeg AI Platform Backend is running"
    }


@router.get("/db")
def health_check_db(db: Session = Depends(get_db)):
    """
    Health check database - kiểm tra kết nối database
    Thực hiện query đơn giản để xác nhận kết nối PostgreSQL hoạt động
    """
    try:
        # Kiểm tra kết nối database bằng simple query
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }
