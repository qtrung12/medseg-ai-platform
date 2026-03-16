"""
Pydantic schemas định nghĩa cấu trúc dữ liệu request/response của API
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ========== User Schemas ==========
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Case Schemas ==========
class CaseBase(BaseModel):
    case_name: str
    modality: Optional[str] = None
    description: Optional[str] = None


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    case_name: Optional[str] = None
    description: Optional[str] = None


class CaseResponse(CaseBase):
    id: int
    user_id: int
    image_path: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ========== InferenceLog Schemas ==========
class InferenceLogBase(BaseModel):
    model_version: Optional[str] = None
    confidence_score: Optional[float] = None
    inference_time: Optional[float] = None
    status: str


class InferenceLogCreate(InferenceLogBase):
    case_id: int
    segmentation_mask_path: str


class InferenceLogResponse(InferenceLogBase):
    id: int
    case_id: int
    segmentation_mask_path: str
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Correction Schemas ==========
class CorrectionBase(BaseModel):
    notes: Optional[str] = None


class CorrectionCreate(CorrectionBase):
    case_id: int
    corrected_mask_path: str
    inference_log_id: Optional[int] = None


class CorrectionResponse(CorrectionBase):
    id: int
    case_id: int
    corrected_mask_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True
