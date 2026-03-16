"""
Database configuration and session management for PostgreSQL
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Lấy database URL từ environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://medseg:medseg123@localhost:5432/medseg_db"
)

# Tạo engine để kết nối database
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Kiểm tra connection trước khi sử dụng
    echo=False  # Set True để debug - in ra SQL queries
)

# Tạo session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class cho tất cả ORM models
Base = declarative_base()


def get_db():
    """
    Dependency injection function để lấy database session
    Sử dụng trong FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
