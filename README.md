# MedSeg AI Platform

Medical Image Segmentation Platform - Nền tảng phân tích và phân đoạn ảnh y tế sử dụng AI.

## Mục Lục

- [Tổng Quan](#tổng-quan)
- [Những Tính Năng Chính](#những-tính-năng-chính)
- [Công Nghệ Sử Dụng](#công-nghệ-sử-dụng)
- [Kiến Trúc Hệ Thống](#kiến-trúc-hệ-thống)
- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
- [Hướng Dẫn Cài Đặt](#hướng-dẫn-cài-đặt)
- [Chạy Ứng Dụng Locally](#chạy-ứng-dụng-locally)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Hướng Dẫn Contribute](#hướng-dẫn-contribute)
- [Tìm Hiểu Thêm](#tìm-hiểu-thêm)

---

## Tổng Quan

**MedSeg AI Platform** là một nền tảng tích hợp đầy đủ để:

1. **Upload ảnh y tế** (CT, MRI, X-ray, ...)
2. **Chạy AI model** để tự động phân đoạn (segmentation) các vùng quan tâm
3. **Hiệu chỉnh kết quả** bằng tay nếu cần thiết
4. **Lưu trữ và quản lý** lịch sử phân tích

Hệ thống sử dụng **kiến trúc microservices** với:
- **Backend API**: FastAPI (Python), xử lý logic chính
- **Frontend**: React/Vue, giao diện người dùng
- **Model Server**: Inference server để chạy AI models
- **Airflow**: Orchestration và scheduling cho các tác vụ nền
- **Database**: PostgreSQL để lưu metadata
- **Cache**: Redis để lưu trữ tạm thời
- **Storage**: MinIO cho lưu ảnh y tế

---

## Những Tính Năng Chính

- ✅ **API RESTful** - Quản lý ca bệnh, ảnh, kết quả phân tích
- ✅ **Xác thực người dùng** - Login/Register (JWT - sẽ implement tuần sau)
- ✅ **Lưu trữ phân tán** - MinIO object storage cho ảnh y tế
- ✅ **Caching thông minh** - Redis cache để tối ưu performance
- ✅ **Health Check** - Endpoint để kiểm tra trạng thái server và DB
- ✅ **Database** - PostgreSQL với relationships mạnh mẽ
- ✅ **CORS** - Cấu hình cho frontend development (localhost:3000, 5173)
- ✅ **Environment Config** - Support multiple environments (dev, staging, production)

---

## Công Nghệ Sử Dụng

### Backend Stack
| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|----------|---------|
| **FastAPI** | 0.135.1 | Web framework, auto API docs |
| **Uvicorn** | 0.41.0 | ASGI server |
| **SQLAlchemy** | 2.0.48 | ORM cho database |
| **Pydantic** | (via FastAPI) | Data validation |
| **psycopg2** | 2.9.11 | PostgreSQL driver |
| **python-dotenv** | 1.0.1 | Environment variables |
| **python-multipart** | 0.0.22 | File uploads |
| **MinIO** | 7.2.20 | Object storage SDK |
| **email-validator** | 2.2.0 | Email validation |

### Infrastructure Stack
| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|----------|---------|
| **PostgreSQL** | 14 | Database chính |
| **Redis** | 7 | Caching & message broker |
| **MinIO** | Latest | Object storage (S3-compatible) |
| **Docker** | Latest | Containerization |
| **Docker Compose** | Latest | Multi-container orchestration |

### Python & Environment
- **Python**: 3.13
- **Virtual Environment**: `.venv` (isolated environment)
- **Package Manager**: `pip` (24.3.1)

---

## Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React/Vue)                      │
│             http://localhost:3000 or 5173                    │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────────┐
│                  FastAPI Backend API                         │
│           http://localhost:8000 (Port 8000)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Health Check Endpoints                           │   │
│  │  • User Management (Login, Register - Future)       │   │
│  │  • Case Management (Upload, List, Details)          │   │
│  │  • Inference Logs (Model predictions)               │   │
│  │  • Corrections (Manual refinements)                 │   │
│  └──────────────────────────────────────────────────────┘   │
└────┬──────────────────────┬──────────────────────────┬──────┘
     │                      │                          │
     │ SQL                  │ Cache/Message Broker     │ Object Storage
     │                      │                          │
┌────▼──────┐        ┌────▼──────┐          ┌────────▼────────┐
│ PostgreSQL│        │  Redis    │          │     MinIO       │
│ Database  │        │   Cache   │          │  Image Storage  │
│ (Port     │        │ (Port     │          │  (Port 9000)    │
│  5432)    │        │  6379)    │          │                 │
└───────────┘        └───────────┘          └─────────────────┘

┌─────────────────────────────────────────────────────────────┐
│           Model Server (Future - Tuần 2)                     │
│              AI Inference Engine                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│           Airflow (Future - Tuần 3)                          │
│            Task Orchestration & Scheduling                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Cấu Trúc Dự Án

```
medseg-ai-platform/
│
├── backend/                      # FastAPI Backend Application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Entry point - FastAPI app initialization
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── database.py      # SQLAlchemy setup, DB connection, session management
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── models.py        # SQLAlchemy ORM models (User, Case, InferenceLog, Correction)
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py       # Pydantic request/response schemas
│   │   │
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── health.py        # Health check endpoints
│   │   │
│   │   └── services/
│   │       └── __init__.py      # Business logic & utilities (placeholder)
│   │
│   ├── .env                      # Environment variables (LOCAL only, don't commit)
│   ├── .env.example              # Template untuk environment variables
│   ├── requirements.txt          # Python dependencies
│   └── (venv/)                   # Virtual environment (ignored by Git)
│
├── frontend/                     # React/Vue Frontend Application (TBD - Tuần 2)
│   └── (will be created)
│
├── model_server/                 # AI Model Inference Server (TBD - Tuần 2)
│   └── (will be created)
│
├── airflow/                      # Airflow Task Orchestration (TBD - Tuần 3)
│   └── (will be created)
│
├── infra/                        # Infrastructure & Deployment
│   ├── docker-compose.yml       # Docker Compose configuration
│   │   ├── PostgreSQL 14 database
│   │   ├── Redis 7 cache
│   │   └── MinIO object storage
│   │
│   └── init-db.sql              # Database initialization script
│
├── ERD.md                        # Entity Relationship Diagram & Schema Documentation
├── README.md                     # This file
├── .gitignore                    # Git ignore patterns
└── .git/                         # Git repository
```

### Giải Thích Chi Tiết Cấu Trúc Backend

#### `main.py` - Entry Point
- Khởi tạo FastAPI application
- Cấu hình CORS middleware (cho phép frontend gọi API)
- Import và đăng ký routers
- Root endpoint trả về thông tin API

#### `db/database.py` - Database Configuration
- Thiết lập SQLAlchemy engine
- Cấu hình connection pool với `pool_pre_ping`
- Tạo SessionLocal factory
- Implement `get_db()` dependency injection function

#### `models/models.py` - Database Models
4 mô hình chính:

1. **User** - Người dùng hệ thống
   - Columns: id, username, email, hashed_password, full_name, is_active, created_at
   - Relationship: many cases

2. **Case** - Ca bệnh / Ảnh y tế
   - Columns: id, user_id (FK), case_name, image_path, image_url, modality, description, created_at, updated_at
   - Relationships: owner (User), many inference_logs, many corrections

3. **InferenceLog** - Kết quả phân tích
   - Columns: id, case_id (FK), model_version, segmentation_mask_path, confidence_score, inference_time, status, error_message, created_at
   - Relationship: case

4. **Correction** - Hiệu chỉnh thủ công
   - Columns: id, case_id (FK), inference_log_id (FK), corrected_mask_path, notes, created_at
   - Relationships: case, inference_log

#### `schemas/schemas.py` - Pydantic Schemas
- Validate input data từ client
- Define response format
- Separate Base, Create, Update, Response classes cho mỗi model
- Hỗ trợ ORM mode: `from_attributes = True`

#### `routers/health.py` - API Endpoints
- `GET /api/v1/health` - Server status check
- `GET /api/v1/health/db` - Database connection check

---

## Hướng Dẫn Cài Đặt

### Prerequisites

Trước khi bắt đầu, bạn cần cài đặt:

1. **Python 3.13+**
   ```bash
   # Check version
   python --version
   ```

2. **Docker & Docker Compose**
   ```bash
   # Check versions
   docker --version
   docker-compose --version
   ```

3. **Git**
   ```bash
   git --version
   ```

### Step 1: Clone Repository

```bash
# Navigate to your projects folder
cd your-workspace

# Clone the repository
git clone https://github.com/phunuquoctrung/medseg-ai-platform.git
cd medseg-ai-platform
```

### Step 2: Setup Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Python Dependencies

```bash
# Navigate to backend folder
cd backend

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 4: Setup Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env file with your configuration
# Default values are already set for local development:
# DATABASE_URL=postgresql://medseg:medseg123@localhost:5432/medseg_db
# REDIS_URL=redis://localhost:6379/0
# MINIO_ENDPOINT=localhost:9000
# etc.
```

### Step 5: Start Docker Services

```bash
# Navigate to infra folder (from project root)
cd infra

# Start all services (PostgreSQL, Redis, MinIO)
docker-compose up -d

# Verify services are running
docker-compose ps

# Output should show 3 services running:
# - medseg_postgres (port 5432)
# - medseg_redis    (port 6379)
# - medseg_minio    (port 9000, 9001)
```

### Step 6: Verify Setup

```bash
# Check Docker services
docker ps --filter "status=running"

# Verify PostgreSQL
docker-compose logs postgres | head -20

# Verify MinIO endpoint
curl http://localhost:9000/minio/health/live
```

---

## Chạy Ứng Dụng Locally

### Running the FastAPI Server

```bash
# From backend folder (đảm bảo venv được activate)
cd backend

# Run development server
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Output:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started server process [1234]
```

### Accessing the Application

1. **API Root**: http://localhost:8000/
   - Returns: `{"name": "MedSeg AI Platform API", "version": "0.1.0", "status": "running"}`

2. **Health Check**: http://localhost:8000/api/v1/health
   - Returns: `{"status": "ok", "message": "MedSeg AI Platform Backend is running"}`

3. **Database Check**: http://localhost:8000/api/v1/health/db
   - Returns: `{"status": "ok", "database": "connected", "message": "Database connection successful"}`

4. **Auto API Documentation**: http://localhost:8000/docs
   - Swagger UI - interactive API documentation
   - Test endpoints directly from browser

5. **Alternative API Docs**: http://localhost:8000/redoc
   - ReDoc - beautiful API documentation

### Stopping Services

```bash
# Stop FastAPI server
# Press CTRL+C

# Stop Docker services
cd infra
docker-compose down

# Stop and remove volumes (to reset database)
docker-compose down -v
```

### Troubleshooting

#### Port Already in Use
```bash
# If port 8000 is already in use:
uvicorn app.main:app --reload --port 8001

# Check which process is using port 8000:
# Windows:
netstat -ano | findstr :8000
# macOS/Linux:
lsof -i :8000
```

#### Virtual Environment Not Activated
```bash
# You should see (venv) at the beginning of your terminal prompt
# If not, activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Database Connection Error
```bash
# Ensure Docker services are running:
docker-compose -f infra/docker-compose.yml up -d

# Verify PostgreSQL is ready:
docker logs medseg_postgres | tail -20

# Check DATABASE_URL in .env matches docker-compose config
```

---

## API Documentation

### Available Endpoints (Week 1)

#### Health Check Endpoints
```
GET /                       → Server info & status
GET /api/v1/health          → Basic health check
GET /api/v1/health/db       → Database connection check
```

### Response Examples

**1. GET `http://localhost:8000/`**
```json
{
  "name": "MedSeg AI Platform API",
  "version": "0.1.0",
  "status": "running"
}
```

**2. GET `http://localhost:8000/api/v1/health`**
```json
{
  "status": "ok",
  "message": "MedSeg AI Platform Backend is running"
}
```

**3. GET `http://localhost:8000/api/v1/health/db`**
```json
{
  "status": "ok",
  "database": "connected",
  "message": "Database connection successful"
}
```

### Full API Documentation

Complete API documentation (including future endpoints) will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

More endpoints coming in Week 2:
- User authentication (Login, Register, Profile)
- Case management (Create, Read, Update, Delete)
- Inference logs (List, Details, Filter)
- Corrections (Create, Update)

---

## Database Schema

### Overview
The project uses PostgreSQL 14 with 4 main tables as defined in [ERD.md](ERD.md):

```
USERS (1) ──────────┬──────── (M) CASES
                    │              │
                    │              ├──── (M) INFERENCE_LOGS
                    │              │
                    │              └──── (M) CORRECTIONS
                    │
             └──────(FK)
```

### Table Descriptions

#### 1. USERS
Stores system user information.

| Column | Type | Constraint | Purpose |
|--------|------|-----------|---------|
| id | INTEGER | PRIMARY KEY | Unique user identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(100) | UNIQUE, NOT NULL | User email |
| hashed_password | VARCHAR(255) | NOT NULL | Encrypted password |
| full_name | VARCHAR(100) | NULL | User's full name |
| is_active | BOOLEAN | DEFAULT: TRUE | Account status |
| created_at | TIMESTAMP | DEFAULT: NOW | Account creation time |

**Relationships:**
- One-to-Many: USERS → CASES (owner)

---

#### 2. CASES
Stores medical cases/images.

| Column | Type | Constraint | Purpose |
|--------|------|-----------|---------|
| id | INTEGER | PRIMARY KEY | Unique case identifier |
| user_id | INTEGER | FOREIGN KEY → users.id | Case owner |
| case_name | VARCHAR(255) | NOT NULL | Case/patient identifier |
| image_path | VARCHAR(500) | NOT NULL | MinIO/S3 path to image |
| image_url | VARCHAR(500) | NULL | Public URL for image |
| modality | VARCHAR(50) | NULL | Image type (CT, MRI, X-ray) |
| description | TEXT | NULL | Case notes/comments |
| created_at | TIMESTAMP | DEFAULT: NOW | Case creation time |
| updated_at | TIMESTAMP | DEFAULT: NOW | Last update time |

**Relationships:**
- Many-to-One: CASES → USERS (owner)
- One-to-Many: CASES → INFERENCE_LOGS
- One-to-Many: CASES → CORRECTIONS

---

#### 3. INFERENCE_LOGS
Stores AI model segmentation results.

| Column | Type | Constraint | Purpose |
|--------|------|-----------|---------|
| id | INTEGER | PRIMARY KEY | Unique log identifier |
| case_id | INTEGER | FOREIGN KEY → cases.id | Associated case |
| model_version | VARCHAR(50) | NULL | Model version used |
| segmentation_mask_path | VARCHAR(500) | NULL | MinIO path to result mask |
| confidence_score | FLOAT | NULL | Model confidence (0-1) |
| inference_time | FLOAT | NULL | Processing time (seconds) |
| status | VARCHAR(50) | NULL | PENDING, SUCCESS, FAILED |
| error_message | TEXT | NULL | Error details if failed |
| created_at | TIMESTAMP | DEFAULT: NOW | Log creation time |

**Relationships:**
- Many-to-One: INFERENCE_LOGS → CASES
- One-to-Many: INFERENCE_LOGS ← CORRECTIONS (corrected_mask_path ref)

---

#### 4. CORRECTIONS
Stores manual corrections to inference results.

| Column | Type | Constraint | Purpose |
|--------|------|-----------|---------|
| id | INTEGER | PRIMARY KEY | Unique correction identifier |
| case_id | INTEGER | FOREIGN KEY → cases.id | Associated case |
| inference_log_id | INTEGER | FOREIGN KEY (optional) → inference_logs.id | Original inference (optional) |
| corrected_mask_path | VARCHAR(500) | NULL | MinIO path to corrected mask |
| notes | TEXT | NULL | Correction notes/rationale |
| created_at | TIMESTAMP | DEFAULT: NOW | Correction creation time |

**Relationships:**
- Many-to-One: CORRECTIONS → CASES
- Many-to-One: CORRECTIONS → INFERENCE_LOGS (optional)

---

### Database Initialization

The database is automatically initialized when Docker services start:

```bash
# init-db.sql is executed automatically by docker-compose
# It grants necessary privileges to the medseg user
```

If you need to reset the database:

```bash
# From infra folder
docker-compose down -v  # Remove volumes
docker-compose up -d    # Recreate with init-db.sql
```

For detailed schema information, see [ERD.md](ERD.md).

---

## Hướng Dẫn Contribute

### Branch Strategy

We follow GitHub Flow with two main branches:

- **`main`** - Production-ready code (stable)
- **`develop`** - Development branch (latest features)

### Workflow

1. **Update develop branch**
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create feature branch**
   ```bash
   # Format: feature/description or bugfix/description
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**
   ```bash
   # Edit files, test locally
   git status                          # Check changes
   git add .                           # Stage changes
   git commit -m "Descriptive message" # Commit
   ```

4. **Push to remote**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Set base: `develop`, compare: `feature/your-feature-name`
   - Add description
   - Request review from teammates
   - Merge after approval

6. **Update local develop**
   ```bash
   git checkout develop
   git pull origin develop
   git branch -d feature/your-feature-name  # Delete local branch
   ```

### Commit Message Conventions

Follow conventional commits format:

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (no logic change)
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `test:` - Test addition/modification
- `chore:` - Build/tooling/dependency

**Examples:**
```bash
git commit -m "feat: add user authentication endpoints"
git commit -m "fix: resolve database connection timeout issue"
git commit -m "docs: update README with setup instructions"
```

### Code Style Guidelines

- **Python**: Follow PEP 8
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Comments**: Write clear comments in Vietnamese or English
- **Type Hints**: Add type annotations for function parameters and returns
- **Docstrings**: Use triple quotes for module/function/class documentation

### Testing Before Push

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows

# Check Python syntax
python -m py_compile app/main.py

# Verify imports
python -c "from app.main import app; print('✓ Imports OK')"

# Run local tests (if available)
pytest

# Check if server starts
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Press CTRL+C to stop
```

### Pull Request Review Checklist

Before submitting PR, ensure:
- ✅ Code follows style guidelines
- ✅ New functions have docstrings
- ✅ Changes are tested locally
- ✅ Commit messages are clear and descriptive
- ✅ No console.log/print statements left (except logging)
- ✅ Dependencies are added to requirements.txt (if new packages)
- ✅ Tests pass

### Common Issues & Solutions

**Issue**: Merge conflicts
```bash
# Update your feature branch with latest develop
git fetch origin
git merge origin/develop
# Resolve conflicts in editor, then:
git add .
git commit -m "Merge develop into feature branch"
```

**Issue**: Need to add new Python package
```bash
# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Commit both
git add requirements.txt
git commit -m "chore: add package-name dependency"
```

---

## Tìm Hiểu Thêm

### Project Documentation
- [**ERD.md**](ERD.md) - Entity Relationship Diagram and detailed database schema

### External Resources
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [MinIO Documentation](https://docs.min.io/)
- [Redis Documentation](https://redis.io/documentation)

### Development Roadmap

#### Week 1 ✅ (Current - Completed)
- [x] Backend structure setup (FastAPI)
- [x] Database schema design and models
- [x] Docker infrastructure (PostgreSQL, Redis, MinIO)
- [x] Git repository and branch strategy
- [x] Health check endpoints
- [x] Documentation (ERD, README)

#### Week 2 (Next)
- [ ] Frontend setup (React/Vue.js)
- [ ] User authentication (JWT)
- [ ] File upload and image management
- [ ] Model server basic setup
- [ ] CRUD endpoints for all entities
- [ ] Integration tests

#### Week 3 (Following)
- [ ] Airflow orchestration setup
- [ ] Scheduled tasks configuration
- [ ] Advanced filtering and search
- [ ] Performance optimization
- [ ] Error handling and logging improvements

#### Week 4+
- [ ] Production deployment
- [ ] Monitoring and alerts
- [ ] API versioning
- [ ] Advanced features (batch processing, etc.)

### Contact & Support

For questions or issues:
- Email: phunuquoctrung@gmail.com
- GitHub Issues: Report bugs and suggest features
- Project Wiki: Additional documentation and guides

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Last Updated**: March 2026  
**Version**: 0.1.0 (Week 1 - Backend Setup)  
**Status**: 🟢 In Development
