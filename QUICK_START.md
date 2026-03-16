# Quick Start - For Your Friend (Bạn Bạng)

**Đọc file này trước tiên! (5 minute guide)**

## 🚀 Cài Đặt Lần Đầu (First Time Setup)

### 1️⃣ Clone Project
```bash
git clone https://github.com/YOUR_USERNAME/medseg-ai-platform.git
cd medseg-ai-platform
```

### 2️⃣ Setup Backend (Everyone cần làm, dù frontend hay backend)
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# OR (macOS/Linux)
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
```

### 3️⃣ Start Docker Services
```bash
# From project root directory
cd infra
docker-compose up -d

# Verify running
docker-compose ps
# Should show 3 containers: postgres, redis, minio
```

### 4️⃣ Start Development Server
```bash
# From backend folder
cd ../backend
uvicorn app.main:app --reload --port 8000

# Open browser: http://localhost:8000
# Should see: {"name": "MedSeg AI Platform API", ...}
```

✅ **Setup complete! Enjoy coding!**

---

## 📅 Daily Workflow (Every Day)

### Morning (When you start)
```bash
# 1. Activate environment
cd medseg-ai-platform/backend
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate             # Windows

# 2. Update from develop branch
git checkout develop
git pull origin develop

# 3. Create or switch to your feature branch
git checkout feature/your-feature
git merge develop                  # Sync with latest

# 4. Start servers
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Verify Docker
cd infra
docker-compose ps
```

### During Day (Coding)
```bash
# Make changes, test locally
# Commit frequently with clear messages
git add .
git commit -m "feat: add login endpoint"
git commit -m "feat: add password validation"

# Push at least once every day
git push origin feature/your-feature
```

### Evening (Before leaving)
```bash
# Push final code
git push origin feature/your-feature

# Send message to friend:
# "Pushed feature/user-auth, ready for review"
```

---

## 📊 Project Structure You'll Use

```
medseg-ai-platform/
├── backend/
│   ├── app/
│   │   ├── main.py              ← FastAPI server
│   │   ├── models/              ← Database models
│   │   ├── schemas/             ← Request/Response validation
│   │   ├── routers/             ← API endpoints
│   │   ├── services/            ← Business logic
│   │   └── db/                  ← Database config
│   ├── .env                     ← Your config (git ignored)
│   ├── .env.example             ← Template for config
│   └── requirements.txt         ← Python packages
│
├── frontend/                    ← Will be created Week 2
├── model_server/                ← Will be created Week 2
├── airflow/                     ← Will be created Week 3
│
├── infra/
│   ├── docker-compose.yml       ← Services config
│   └── init-db.sql              ← Database init
│
├── README.md                    ← Full documentation
├── ERD.md                       ← Database schema
├── COLLABORATION_GUIDE.md       ← How to work together
└── .git/                        ← Git repository
```

---

## 🔧 If You're Person B (Backend Developer)

### Your Main Job (Week 2+)
- Create API endpoints: POST /users, GET /cases, etc.
- Database queries and migrations
- Authentication system
- Error handling

### You'll Work With
```
├── app/routers/       ← Create new files here for endpoints
├── app/models/        ← Define new database tables
├── app/schemas/       ← Define request/response formats
└── app/services/      ← Business logic (password hashing, etc.)
```

### Example: Create New Endpoint
```bash
# 1. Add to app/routers/cases.py
@router.post("/api/v1/cases")
def create_case(case: CaseCreate, db: Session = Depends(get_db)):
    # Your code here
    return {"message": "Case created"}

# 2. Test locally
curl -X POST http://localhost:8000/api/v1/cases \
  -H "Content-Type: application/json" \
  -d '{"case_name": "Patient123", ...}'

# 3. Commit
git add app/routers/cases.py
git commit -m "feat: add create case endpoint"
git push origin feature/cases-api

# 4. Create Pull Request for review
```

---

## 🎨 If You're Person A (Frontend Developer)

### Your Main Job (Week 2+)
- React/Vue pages: Home, Login, Dashboard
- Connect to backend APIs
- Handle errors and loading states
- Styling and UI/UX

### You'll Work With (When created Week 2)
```
frontend/
├── src/pages/        ← Create pages here
├── src/components/   ← Reusable UI components
├── src/services/     ← API calling functions
└── public/           ← Static files
```

### Example: Use Person B's API
```javascript
// frontend/src/services/api.js
import axios from 'axios';

export const createCase = async (caseData) => {
  const response = await axios.post(
    'http://localhost:8000/api/v1/cases',
    caseData
  );
  return response.data;
};

// In your component:
import { createCase } from '../services/api';

const handleUpload = async () => {
  try {
    const result = await createCase(formData);
    console.log('Case created:', result);
  } catch (error) {
    console.error('Failed:', error.message);
  }
};
```

---

## 🐳 Docker Commands You'll Use

```bash
# Check if services running
cd infra
docker-compose ps

# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker logs medseg_postgres

# Reset everything (WARNING: deletes data!)
docker-compose down -v
docker-compose up -d
```

---

## 🔄 Common Git Commands

```bash
# See what changed
git status

# Update from team
git pull origin develop

# Save your changes
git add .
git commit -m "clear message about your change"

# Share with team
git push origin feature/your-branch

# See history
git log --oneline

# Undo last commit (if not pushed yet)
git reset --soft HEAD~1
```

---

## 📞 Where to Find Help

### If Something's Broken
1. **Check logs** → `docker logs medseg_postgres`
2. **Restart services** → `docker-compose restart`
3. **Check README.md** → Troubleshooting section
4. **Ask your friend** → Message on Slack/Discord

### Code Questions
- **README.md** - Full documentation
- **ERD.md** - Database structure
- **COLLABORATION_GUIDE.md** - How to work together properly

---

## ✅ How to Know Setup is Correct

```bash
# 1. Check virtual environment
venv\Scripts\activate
pip list | grep fastapi
# Should show fastapi 0.135.1

# 2. Check Docker services
docker-compose ps
# Should show 3 containers (Up 2 minutes)

# 3. Test backend
curl http://localhost:8000
# Should return: "name": "MedSeg AI Platform API"

# 4. Test database
curl http://localhost:8000/api/v1/health/db
# Should return: "status": "ok"
```

---

## 🚫 Common Mistakes to Avoid

```bash
# ❌ Don't commit .env file
git add .env              # WRONG!
git add backend/          # This adds .env too!

# ✅ Do this instead
git add backend/app/      # Add specific folder
git add README.md         # Add specific files

# ❌ Don't forget to activate venv
python -m pip install    # Uses system Python!

# ✅ Do this
source venv/bin/activate  # Activate first
pip install package       # Uses venv Python

# ❌ Don't commit node_modules (if frontend exists)
git add frontend/node_modules/  # HUGE! Don't do this

# ✅ node_modules should be in .gitignore
```

---

## 🎯 This Week Tasks

**Person B (Backend):**
- [ ] Setup complete
- [ ] Can run `uvicorn app.main:app --reload`
- [ ] Know where to add new endpoints (app/routers/)
- [ ] Understand what ERD.md means

**Person A (Frontend):**
- [ ] Setup complete
- [ ] Can run backend + understand what it does
- [ ] Know where to create pages and components (Week 2)
- [ ] Understand how to call APIs from Person B

**Both:**
- [ ] Understand Git workflow
- [ ] Know how to push/pull code
- [ ] Can run Docker services
- [ ] Read README.md thoroughly

---

## 📚 Next Week (Week 2)

Person B will create:
- User registration API
- User login API  
- JWT token system

Person A will create:
- Frontend project setup
- Login page
- Connect login page to API

Then you'll test together! 🎉

---

**Questions? Read COLLABORATION_GUIDE.md or ask your friend!**

Version: 1.0 | Date: Week 1
