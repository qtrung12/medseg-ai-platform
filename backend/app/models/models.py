"""
SQLAlchemy ORM Models tương ứng với các bảng trong PostgreSQL database
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    """
    Model đại diện cho bảng users
    Lưu thông tin người dùng của hệ thống
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    cases = relationship("Case", back_populates="owner")


class Case(Base):
    """
    Model đại diện cho bảng cases
    Lưu thông tin ca bệnh hoặc ảnh được upload
    """
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_name = Column(String(255), nullable=False)
    image_path = Column(String(500), nullable=False)  # S3/MinIO path
    image_url = Column(String(500), nullable=True)  # Public URL
    modality = Column(String(50), nullable=True)  # CT, MRI, X-ray, etc.
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="cases")
    inference_logs = relationship("InferenceLog", back_populates="case")
    corrections = relationship("Correction", back_populates="case")


class InferenceLog(Base):
    """
    Model đại diện cho bảng inference_logs
    Lưu lịch sử chạy mô hình AI và kết quả dự đoán
    """
    __tablename__ = "inference_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    model_version = Column(String(50), nullable=True)
    segmentation_mask_path = Column(String(500), nullable=False)  # S3/MinIO path
    confidence_score = Column(Float, nullable=True)  # 0.0 - 1.0
    inference_time = Column(Float, nullable=True)  # milliseconds
    status = Column(String(50), nullable=False)  # pending, completed, failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case = relationship("Case", back_populates="inference_logs")


class Correction(Base):
    """
    Model đại diện cho bảng corrections
    Lưu các chỉnh sửa của người dùng đối với kết quả segmentation
    """
    __tablename__ = "corrections"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    inference_log_id = Column(Integer, ForeignKey("inference_logs.id"), nullable=True)
    corrected_mask_path = Column(String(500), nullable=False)  # S3/MinIO path
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case = relationship("Case", back_populates="corrections")
