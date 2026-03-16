# MedSeg AI Platform - Entity Relationship Diagram (ERD)

## Overview
Medical Image Segmentation Platform database schema showing relationships between users, medical cases, AI inference logs, and user corrections.

---

## Database Design

### Entity Relationship

```
USERS (1) → (Many) CASES
CASES (1) → (Many) INFERENCE_LOGS
CASES (1) → (Many) CORRECTIONS
```

---

## Tables Description

### 1. USERS Table
**Purpose:** Store user information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique user identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Username for login |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Email address |
| hashed_password | VARCHAR(255) | NOT NULL | Encrypted password |
| full_name | VARCHAR(100) | NULLABLE | User's full name |
| is_active | BOOLEAN | DEFAULT TRUE | User status (active/inactive) |
| created_at | DATETIME | DEFAULT NOW() | Account creation timestamp |

**Relationships:**
- One User → Many Cases (owns medical cases)

---

### 2. CASES Table
**Purpose:** Store medical case/image information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique case identifier |
| user_id | INTEGER | FOREIGN KEY → Users.id | Case owner |
| case_name | VARCHAR(255) | NOT NULL | Medical case name |
| image_path | VARCHAR(500) | NOT NULL | S3/MinIO storage path |
| image_url | VARCHAR(500) | NULLABLE | Public URL for display |
| modality | VARCHAR(50) | NULLABLE | Image type (CT, MRI, X-ray, etc.) |
| description | TEXT | NULLABLE | Case notes/description |
| created_at | DATETIME | DEFAULT NOW() | Upload timestamp |
| updated_at | DATETIME | DEFAULT NOW() ON UPDATE | Last modification timestamp |

**Relationships:**
- Many Cases → One User (belongs to user)
- One Case → Many InferenceLogs (has multiple AI inference runs)
- One Case → Many Corrections (has multiple user corrections)

---

### 3. INFERENCE_LOGS Table
**Purpose:** Store AI model inference results and history

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique inference log identifier |
| case_id | INTEGER | FOREIGN KEY → Cases.id | Associated medical case |
| model_version | VARCHAR(50) | NULLABLE | AI model version used |
| segmentation_mask_path | VARCHAR(500) | NOT NULL | S3/MinIO path to result mask |
| confidence_score | FLOAT | NULLABLE | Model confidence (0.0-1.0) |
| inference_time | FLOAT | NULLABLE | Execution time in milliseconds |
| status | VARCHAR(50) | NOT NULL | Status (pending, completed, failed) |
| error_message | TEXT | NULLABLE | Error details if failed |
| created_at | DATETIME | DEFAULT NOW() | Inference timestamp |

**Relationships:**
- Many InferenceLogs → One Case (belongs to case)

---

### 4. CORRECTIONS Table
**Purpose:** Store user corrections to AI segmentation results

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique correction identifier |
| case_id | INTEGER | FOREIGN KEY → Cases.id | Associated medical case |
| inference_log_id | INTEGER | FOREIGN KEY → InferenceLogs.id | Reference to inference result (optional) |
| corrected_mask_path | VARCHAR(500) | NOT NULL | S3/MinIO path to corrected mask |
| notes | TEXT | NULLABLE | User notes about correction |
| created_at | DATETIME | DEFAULT NOW() | Correction timestamp |

**Relationships:**
- Many Corrections → One Case (belongs to case)
- Optional link to InferenceLogs (references specific inference)

---

## Data Flow Example

```
Timeline: Medical Image Analysis Workflow

1. User Registration
   └─> Create record in USERS table
   
2. Image Upload
   └─> Create record in CASES table
   └─> Store image file in MinIO

3. AI Inference
   └─> Model processes image
   └─> Create record in INFERENCE_LOGS table
   └─> Store segmentation mask in MinIO

4. User Review
   └─> User reviews segmentation result
   └─> If satisfied: workflow ends
   └─> If needs correction: go to step 5

5. User Correction
   └─> User manually corrects segmentation
   └─> Create record in CORRECTIONS table
   └─> Store corrected mask in MinIO

6. Data Archive
   └─> All records kept for audit trail
   └─> Can retrieve historical versions
```

---

## Key Design Decisions

### Foreign Keys (Relationships)
- **CASES.user_id** → USERS.id
  - Establishes ownership: each case belongs to one user
  - Enables user-specific case filtering

- **INFERENCE_LOGS.case_id** → CASES.id
  - Links inference results to source case
  - Allows retrieval of all inference runs for a case

- **CORRECTIONS.case_id** → CASES.id
  - Links user corrections to source case
  - Enables version history tracking

- **CORRECTIONS.inference_log_id** → INFERENCE_LOGS.id (OPTIONAL)
  - Optional reference to specific inference result
  - Allows tracking which inference was corrected

### Storage Strategy
- **Image files**: S3/MinIO object storage (not database)
- **Paths & URLs**: Store in database pointing to object storage
- **Metadata**: All case/result info in database

### Temporal Data
- **created_at**: Immutable creation timestamp
- **updated_at**: Updated on modification (CASES only)
- Enables audit trail and version history

---

## Indexes (for Performance)

**Recommended indexes:**
```sql
-- User lookups
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Case lookups
CREATE INDEX idx_cases_user_id ON cases(user_id);
CREATE INDEX idx_cases_created_at ON cases(created_at);

-- Inference log lookups
CREATE INDEX idx_inference_logs_case_id ON inference_logs(case_id);
CREATE INDEX idx_inference_logs_status ON inference_logs(status);

-- Correction lookups
CREATE INDEX idx_corrections_case_id ON corrections(case_id);
```

---

## Database Integrity Constraints

✅ **Primary Keys**: Ensure unique records
✅ **Foreign Keys**: Maintain referential integrity
✅ **Unique Constraints**: Prevent duplicate usernames/emails
✅ **Not Null**: Required fields always present
✅ **Default Values**: Automatic timestamps

---

## Future Extensions

Potential tables for Phase 2:
- **AUDIT_LOGS**: Track all system actions
- **ANNOTATIONS**: Detailed pixel-level annotations
- **MODEL_METRICS**: Performance metrics per model
- **USER_FEEDBACK**: Quality feedback on results
- **EXPORT_HISTORY**: Track data exports/shares

