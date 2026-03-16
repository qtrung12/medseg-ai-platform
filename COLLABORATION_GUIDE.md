# MedSeg AI Platform - Collaboration Guide

**Hướng dẫn làm chuyên nghiệp khi 2 người làm chung dự án**

## 📑 Mục Lục
- [Team Structure & Communication](#team-structure--communication)
- [Initial Setup for Both Developers](#initial-setup-for-both-developers)
- [Daily Workflow](#daily-workflow)
- [Git Workflow - Branching & Merging](#git-workflow---branching--merging)
- [Docker & Service Management](#docker--service-management)
- [Code Review Process](#code-review-process)
- [Testing Strategy](#testing-strategy)
- [Deployment Checklist](#deployment-checklist)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## Team Structure & Communication

### Team Roles (Week 1-4)
```
Developer 1 (Person A)
├── Frontend Development (React/Vue - Week 2)
├── UI/UX Implementation
└── Client-side features

Developer 2 (Person B)
├── Backend Development (Current focus)
├── Database & API endpoints
└── Infrastructure & DevOps

Shared Responsibilities:
├── Testing
├── Documentation
├── Git maintenance
└── Code reviews
```

### Communication Checklist
**Daily (每日)**
- ☐ Morning standup (15 min) - What we did yesterday, what we're doing today, blockers?
- ☐ Slack/Email updates before pushing code changes
- ☐ Share commits with clear messages

**Weekly**
- ☐ Code review session (Friday, 1-2 hours)
- ☐ Merge develop → main (if everything passes tests)
- ☐ Update project tracking (who did what, progress %)

**Before Major Changes**
- ☐ Discuss design/architecture approach
- ☐ Agree on implementation strategy
- ☐ Assign tasks clearly

### Project Tracking
```
Use simple checklist in README.md or Google Sheets:

Week 2 Tasks:
├── Frontend (Person A)
│   ├── [ ] Setup React/Vue project
│   ├── [ ] Home page layout
│   └── [ ] Login form
└── Backend (Person B)
    ├── [ ] User authentication API
    ├── [ ] Case upload endpoint
    └── [ ] Integration tests

Update status: Not Started → In Progress → Code Review → Merged → Deployed
```

---

## Initial Setup for Both Developers

### Person A (Frontend Developer)
```bash
# Step 1: Clone repository
git clone https://github.com/YOUR_USERNAME/medseg-ai-platform.git
cd medseg-ai-platform

# Step 2: Understand the project structure
cat README.md              # Read full docs
cat ERD.md                 # Understand database

# Step 3: Setup backend locally (even if you're doing frontend)
# WHY? You need to test API integration
cd backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

# Step 4: Start Docker services
cd ../infra
docker-compose up -d

# Verify services
docker-compose ps
# Should show 3 running: postgres, redis, minio

# Step 5: Test backend API
cd ../backend
uvicorn app.main:app --reload --port 8000

# In another terminal:
curl http://localhost:8000
# Should return: {"name": "MedSeg AI Platform API", ...}

# Step 6: Create your feature branch
git checkout develop
git pull origin develop
git checkout -b feature/frontend-setup
```

### Person B (Backend Developer)
```bash
# Step 1: Clone repository
git clone https://github.com/YOUR_USERNAME/medseg-ai-platform.git
cd medseg-ai-platform

# Step 2: Understand the database
cat ERD.md                 # Know what tables we have

# Step 3: Setup backend environment
cd backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
pip freeze                 # Verify all packages installed

# Step 4: Create .env file
cp .env.example .env
# Check .env values match what Docker will use

# Step 5: Start Docker services
cd ../infra
docker-compose up -d

# Verify all services are ready
docker-compose ps | grep -E "running|healthy"

# Verify PostgreSQL is accessible
docker exec medseg_postgres psql -U medseg -d medseg_db -c "\dt"
# If error about role, Docker is still initializing - wait 10 seconds and retry

# Step 6: Test backend endpoints
cd ../backend
uvicorn app.main:app --reload --port 8000

# In another terminal, test
curl http://localhost:8000/api/v1/health
# Should return: {"status": "ok", "message": "..."}

# Step 7: Create your feature branch
git checkout develop
git pull origin develop
git checkout -b feature/auth-endpoints
```

### Both Developers
```bash
# Create Git aliases (optional but recommended)
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm "commit -m"
git config --global alias.up pull --rebase

# Test alias
git st                     # Should show status
```

---

## Daily Workflow

### Start of Day (每天早上)

**Person A (Frontend):**
```bash
# 1. Activate environment
cd medseg-ai-platform/frontend      # or wherever you're working
source venv/bin/activate            # macOS/Linux
# OR
venv\Scripts\activate               # Windows

# 2. Update code from main branch
git checkout develop
git pull origin develop             # Get latest changes from Person B

# 3. Continue your feature
git checkout feature/your-feature
git merge develop                   # If Person B merged something

# 4. Start dev server
npm start                           # or yarn serve (depends on framework)
```

**Person B (Backend):**
```bash
# 1. Activate environment
cd medseg-ai-platform/backend
source venv/bin/activate

# 2. Update code
git checkout develop
git pull origin develop

# 3. Continue your feature
git checkout feature/your-feature
git merge develop                   # If you diverged

# 4. Start API server
uvicorn app.main:app --reload --port 8000
```

**Both:**
```bash
# 5. Make sure Docker is running
cd infra
docker-compose ps                   # Should show 3 containers running

# If not running:
docker-compose up -d
```

### During Day (編碼時)

**Code Organization:**
```
Week 2 Split:

Backend (Person B):
- routers/users.py          → POST /api/v1/users (register)
- routers/auth.py           → POST /api/v1/auth/login
- services/user_service.py  → Business logic for users

Frontend (Person A):
- pages/Home.jsx
- pages/Login.jsx
- components/NavigationBar.jsx
- services/api.js           → API call functions
```

**Commit Strategy:**
```bash
# Before each commit, ensure:
# ✓ Code is tested locally
# ✓ No console.log/print statements
# ✓ Docstrings added for new functions
# ✓ No .env secrets in code

# Small commits are better than large ones
git add backend/routers/users.py
git commit -m "feat: add user registration endpoint"

git add backend/routers/auth.py
git commit -m "feat: add JWT token generation"

git add backend/services/user_service.py
git commit -m "feat: implement password hashing with bcrypt"

# NOT this (too big, hard to review):
git commit -m "feat: complete user authentication system"
```

### End of Day (下班前)

**Push Your Work:**
```bash
# Person A (Frontend):
git push origin feature/your-feature

# Person B (Backend):
git push origin feature/your-feature

# IMPORTANT: Push daily, don't keep code only locally!
```

**Update Team:**
```bash
# Write brief summary:
# Example in Slack/Email:
"""
Frontend (Person A):
- ✓ Completed: Login form UI
- 🔄 In Progress: Form validation
- 🚫 Blocked: Waiting for login API endpoint from Person B

Backend (Person B):
- ✓ Completed: User registration API
- 🔄 In Progress: JWT authentication
- 📋 Next: Password reset endpoint
"""
```

---

## Git Workflow - Branching & Merging

### Branch Naming Convention
```
feature/description          → New feature (Person A/B)
bugfix/description           → Bug fix
hotfix/description           → Urgent production fix
docs/description             → Documentation only

Examples:
- feature/user-authentication
- feature/image-upload
- bugfix/cors-error
- docs/api-endpoints
```

### Workflow: Person A wants to merge code

```bash
# Step 1: Make sure your code is complete
git add .
git status
# Should show your changes

# Step 2: Test everything works
cd frontend
npm test                            # If you have tests
npm run build                       # Build before merge

# Step 3: Push feature branch
git push origin feature/your-feature

# Step 4: Create Pull Request on GitHub
# → Go to: https://github.com/YOUR_USERNAME/medseg-ai-platform
# → Click: "Pull Requests" tab
# → Click: "New Pull Request"
# → Base: develop, Compare: feature/your-feature
# → Write description:
"""
## What changes?
- Implemented login form
- Added form validation
- Integrated with login API

## Testing
- Tested on Chrome, Firefox
- Verified error messages display correctly
- Confirmed redirect after login

## Screenshots/Links
[Add screenshot if UI change]

## Checklist
- [x] Code follows style guide
- [x] Self-reviewed my own code
- [x] No new warnings generated
- [x] Comments added for complex logic
"""

# Step 5: Wait for Person B to review
# Person B will:
# - Read your code
# - Add comments if needed
# - Approve or request changes

# Step 6: If approved, merge on GitHub
# → Click "Merge pull request"
# → Select "Squash and merge" (cleaner history)
# → Delete feature branch

# Step 7: Back in your terminal
git checkout develop
git pull origin develop             # Get merged code
git branch -d feature/your-feature  # Delete local branch
```

### Workflow: Person B wants to merge code

```bash
# Same as above, but for backend

# Before PR, ensure:
# ✓ All tests pass
# ✓ No syntax errors
pip install -r requirements.txt    # Verify dependencies

# Run tests (if you wrote them)
pytest tests/                      # When you have tests

# Check Python code quality
python -m py_compile app/main.py app/models/models.py

# Then follow same PR process
```

### Reviewing Person A's Frontend Code (Person B perspective)

**When you see PR notification:**
```bash
# Step 1: Create a review branch to test
git fetch origin
git checkout origin/feature/frontend-feature

# Step 2: Run locally to see if it works
cd frontend
npm install
npm start
# Test the changes

# Step 3: Review code on GitHub
# - Check coding style
# - Look for edge cases
# - Verify it integrates with your API

# Step 4: Add comment
# Good examples:
"""
✅ Good work! Code is clean and well-documented.

Minor suggestions:
1. Line 45: Consider using optional chaining (?.) for safety
2. Add error handling for failed API calls on line 67

Ready to merge after these fixes!
"""

# Step 5: Approve the PR
# → Click "Review changes" → "Approve" → Submit
```

### Resolving Merge Conflicts

**Scenario:** You both edited the same file
```bash
# This happens when:
# - Person A edited frontend/src/App.jsx
# - Person B edited frontend/src/App.jsx
# - Both try to merge into develop

# Solution:
# 1. Get conflicts
git fetch origin
git merge origin/develop

# Output:
# CONFLICT (content): Merge conflict in frontend/src/App.jsx
# Auto-merging frontend/src/App.jsx
# CONFLICT (add/add): Merge conflict in backend/requirements.txt

# 2. Open conflicted file, find markers:
"""
<<<<<<< HEAD
  return <Home user={currentUser} />        # Your code
=======
  return <Dashboard user={currentUser} />   # Person B's code
>>>>>>>
"""

# 3. Decide which code to keep
# Option A: Keep your code, delete <<<<<<
# Option B: Keep Person B's code
# Option C: Combine both

# After deciding:
git add frontend/src/App.jsx
git commit -m "Merge: resolve App.jsx conflict"
git push

# Then create/update PR - it should show "conflict resolved"
```

---

## Docker & Service Management

### Understanding Current Services

```bash
# What we have running:
docker-compose ps

# Output:
NAME                STATUS          PORTS
medseg_postgres     Up 2 minutes    5432/tcp
medseg_redis       Up 2 minutes    6379/tcp
medseg_minio       Up 2 minutes    9000/tcp, 9001/tcp
```

### Service Details

**PostgreSQL (Database)**
```bash
# Access database
docker exec -it medseg_postgres psql -U medseg -d medseg_db

# Common commands:
\dt                                     # List all tables
\d users                               # Show users table structure
SELECT count(*) FROM users;            # Count users
\q                                     # Quit

# Backup database
docker exec medseg_postgres pg_dump -U medseg medseg_db > backup.sql

# Restore database
docker exec -i medseg_postgres psql -U medseg medseg_db < backup.sql
```

**Redis (Cache)**
```bash
# Access Redis CLI
docker exec -it medseg_redis redis-cli

# Common commands:
PING                                   # Test connection (should return PONG)
KEYS *                                 # List all keys
SET mykey "myvalue"
GET mykey
DEL mykey
FLUSHALL                              # Clear all (use in development only!)
exit                                   # Quit
```

**MinIO (Object Storage)**
```bash
# Access MinIO console
# URL: http://localhost:9001
# Username: minioadmin
# Password: minioadmin

# Or use MinIO CLI:
docker exec -it medseg_minio mc ls minio
docker exec -it medseg_minio mc mb minio/medseg-ai
```

### Docker Workflow for Both Developers

**At Start of Project (Week 2+):**
```bash
# Both run same commands
cd infra
docker-compose up -d                   # Start all services
docker-compose ps                      # Verify running

# Both should see:
# ✓ 3 containers running
# ✓ Ports open: 5432, 6379, 9000, 9001
```

**If Services Get Corrupted:**
```bash
# Example: Database stopped responding
# Solution: Restart just that service

docker-compose restart postgres         # Restart PostgreSQL only
docker-compose logs postgres           # Check logs

# Or reset entire stack
docker-compose down -v                 # Stop and remove volumes
docker-compose up -d                   # Recreate fresh

# ⚠️ WARNING: This deletes all data in development database
# Use only when you want clean slate
```

**Database Synchronization:**
```
IMPORTANT: When Person B creates new tables/schemas
→ Build migration script
→ Run on both machines
→ Commit migration to Git

Example (Week 2):
File: infra/migrations/001_create_users_table.sql

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    ...
);

How both developers apply migration:
docker exec medseg_postgres psql -U medseg -d medseg_db < infra/migrations/001_create_users_table.sql
```

---

## Code Review Process

### Before You Request Review

**Person A/B Checklist:**
```
Code Quality:
  [ ] Code is readable and well-commented
  [ ] No hardcoded values (use config/environment)
  [ ] Follows naming convention (snake_case for functions)
  [ ] No console.log or print() statements
  [ ] Error messages are descriptive

Testing:
  [ ] Tested locally before pushing
  [ ] Tested with invalid inputs
  [ ] Tested with multiple browsers (for frontend)
  [ ] Verified no CSS conflicts (for frontend)
  [ ] Verified API response format (for backend)

Documentation:
  [ ] Docstring added to functions
  [ ] README updated if new feature
  [ ] API endpoint documented

Security:
  [ ] No secrets hardcoded (.env only)
  [ ] Input validation added
  [ ] SQL injection prevention (using ORM)
  [ ] CORS properly configured

Performance:
  [ ] Database queries optimized
  [ ] No N+1 queries
  [ ] API response time acceptable
```

### Review Template

**Person A reviewing Person B's backend code:**
```
✅ What I liked:
- Clear commit messages
- Good error handling
- Type hints on functions
- Database indexes properly set

⚠️ Questions/Suggestions:
1. Line 45-50: Why using raw SQL instead of ORM?
   → Can we use User.query.filter() instead?

2. Line 120: What happens if case_id doesn't exist?
   → Should we return 404 or 500?

3. Performance: InferenceLog query might be slow with large datasets
   → Consider adding pagination

🔧 Required Changes:
1. Add error handling for database connection
2. Move magic strings to constants
3. Update tests to cover edge cases (if you have them)

📋 Nice-to-have:
- Add docstring to inference_log_service.py
- Update README with new API endpoint docs

Approved after requested changes ✅
```

### Feedback Guidelines

**Good Review Comment:**
```
✅ "This function clearly handles permission checking. 
   Consider also validating the file format here for 
   early error detection. See similar example in upload_service.py L23."
```

**Bad Review Comment:**
```
❌ "This is bad. Change it."
   → No context, no alternative suggested
```

---

## Testing Strategy

### Backend Testing (Person B)

**What to test:**
```
✓ API Endpoints
  - POST /api/v1/users (create user)
  - GET /api/v1/users/{id} (get user)
  - PUT /api/v1/users/{id} (update user)
  - DELETE /api/v1/users/{id} (delete user)

✓ Database Operations
  - Insert/update/delete data
  - Relationship constraints
  - Unique constraints

✓ Business Logic
  - Password hashing
  - Token generation
  - Image validation
```

**Example test (Week 2+):**
```python
# tests/test_user_endpoints.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/api/v1/users", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_get_nonexistent_user():
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

# Run tests:
# pytest tests/test_user_endpoints.py -v
```

### Frontend Testing (Person A)

```javascript
// tests/Login.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Login from '../pages/Login';

test('shows error on invalid credentials', () => {
    render(<Login />);
    
    const inputEmail = screen.getByPlaceholderText('Email');
    fireEvent.change(inputEmail, { target: { value: 'invalid' } });
    
    const submitButton = screen.getByText('Login');
    fireEvent.click(submitButton);
    
    expect(screen.getByText('Invalid email format')).toBeInTheDocument();
});

// Run tests:
// npm test
```

### Manual API Testing

```bash
# Person A testing Person B's new endpoint
# Without writing code, just test manually

# Test 1: Create user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "pass123"
  }'

# Should return 201 with user data

# Test 2: Get user
curl http://localhost:8000/api/v1/users/1

# Should return 200 with user data

# Test 3: Invalid input
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane",
    "email": "invalid-email"
  }'

# Should return 422 with validation error
```

---

## Deployment Checklist

### Before Week 2+ Deployment

```
Pre-Deployment Review:
  [ ] All PRs merged to main branch
  [ ] Latest code pulled locally
  [ ] All Docker services working
  [ ] Database migrations applied
  [ ] No console.log/print statements in code
  [ ] Environment variables documented
  [ ] README updated with latest info
  [ ] No breaking changes to API

Testing (Run before deploy):
  [ ] Backend server starts without errors
  [ ] All health check endpoints pass
  [ ] Database connection works
  [ ] Manual API testing completed
  [ ] Frontend loads without errors
  [ ] Frontend can call API successfully
  [ ] No JavaScript/Python syntax errors

Final Check:
  [ ] Git log is clean (good commit messages)
  [ ] .env file NOT committed (only .env.example)
  [ ] No dependencies missing (requirements.txt updated)
  [ ] Docker images build successfully
  [ ] Performance acceptable (page loads < 3s)

Tag Release (recommended):
git tag -a v0.2.0 -m "Week 2: User authentication and file upload"
git push origin v0.2.0
```

---

## Troubleshooting Common Issues

### Issue 1: Merge Conflicts in requirements.txt

**Cause:** Both Person A and B added different packages
```bash
# Solution:
git fetch origin
git merge origin/develop

# You'll see conflict
# Edit requirements.txt:
# Keep/add packages from both versions
# Example:
fastapi==0.135.1          # Everyone needs this
react==18.2.0             # Person A added
pytest==7.4.0             # Person B added

# Resolve:
git add requirements.txt
git commit -m "Merge: combine requirements from both branches"
```

### Issue 2: Docker Container Won't Start

```bash
# Symptom:
docker-compose up
# Error: Container fails to start

# Solution:
docker-compose logs postgres        # Check logs
# If error about corrupted database:
docker-compose down -v
docker-compose up -d
# This resets database but you lose data
```

### Issue 3: Port Already in Use

```bash
# Symptom:
# Error: Port 8000 already in use

# Solution 1: Find what's using it
netstat -ano | findstr :8000       # Windows
lsof -i :8000                      # macOS/Linux

# Solution 2: Kill the process
taskkill /PID <PID> /F             # Windows

# Solution 3: Use different port
uvicorn app.main:app --port 8001
```

### Issue 4: Git Merge Conflicts with .env

**Cause:** .env is NOT committed (good!), but .env.example is
```bash
# If you see conflict on .env:
# You accidentally committed .env (bad!)

# Solution:
git rm --cached .env                # Remove from Git
git add .gitignore                  # Should already ignore .env
git commit -m "Remove .env from Git"

# Tell Person B to do same:
rm .env
git pull origin develop
cp .env.example .env
# Manually set values in .env
```

### Issue 5: Virtual Environment Not Activated

```bash
# Symptom:
# pip install fails, or wrong Python used

# Solution:
# Make sure you see (venv) at start of terminal prompt

# Windows:
cd backend
venv\Scripts\activate
# Should show: (venv) C:\...\backend>

# macOS/Linux:
cd backend
source venv/bin/activate
# Should show: (venv) user@computer:...$
```

---

## Best Practices Summary

### Git
- ✅ Pull before you start coding
- ✅ Commit small changes frequently
- ✅ Write clear commit messages
- ✅ Push at end of day
- ✅ Never force push to shared branches
- ❌ Never commit .env files
- ❌ Never commit node_modules or venv

### Code
- ✅ Comment complex logic
- ✅ Use meaningful variable names
- ✅ Add docstrings to functions
- ✅ Test before pushing
- ✅ Handle errors gracefully
- ❌ No console.log/print in final code
- ❌ No hardcoded secrets

### Docker
- ✅ Keep docker-compose.yml in repo
- ✅ Document environment variables
- ✅ Backup important data before docker-compose down -v
- ✅ Restart services if they become unresponsive
- ❌ Don't use production database on local machine

### Communication
- ✅ Share PR links and status daily
- ✅ Ask for help when blocked
- ✅ Review PRs promptly (within 24 hours)
- ✅ Be specific in feedback ("line 45" not "this")
- ❌ Don't merge your own code without review
- ❌ Don't wait until end of week to merge

---

## Weekly Sync Checklist

**Every Friday afternoon:**
```
[ ] Code Review Session (1-2 hours)
    - Person A reviews all Person B's PRs
    - Person B reviews all Person A's PRs
    - Merge to develop when approved
    - Delete feature branches

[ ] Update Project Status
    - What's completed this week?
    - What's planned for next week?
    - Any blockers or delays?

[ ] Database & Infrastructure Check
    - Are Docker services stable?
    - Any performance issues?
    - Backup database if important data
    - Update documentation if any changes

[ ] Plan Next Week
    - Divide tasks clearly
    - Set realistic goals
    - Identify dependencies between tasks

[ ] Document Changes
    - Update README.md if architecture changed
    - Update COLLABORATION_GUIDE.md if workflow changed
    - Add migration scripts if DB schema changed
```

---

## Next Steps

### Week 2 Planning

```
Person A (Frontend):
  1. Setup React/Vue project
  2. Create basic page layout
  3. Implement login form
  4. Setup API client (axios/fetch)

Person B (Backend):
  1. Create user authentication API
  2. Implement password hashing (bcrypt)
  3. Generate JWT tokens
  4. Create user CRUD endpoints

Shared:
  1. Test integration (Frontend → Backend API)
  2. Fix any CORS issues
  3. Document API endpoints
  4. Code review everything
```

---

**Last Updated:** Week 1  
**Status:** Ready for multi-developer collaboration  
**Document Version:** 1.0
