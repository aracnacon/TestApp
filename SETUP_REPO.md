# Setting Up Git Repository

## Quick Setup

### 1. Initialize Git Repository
```bash
cd /Users/brandon/TestApp
git init
```

### 2. Add All Files
```bash
git add .
```

### 3. Create Initial Commit
```bash
git commit -m "Initial commit: Django + PostgreSQL Docker setup"
```

### 4. Create GitHub Repository

**Option A: Using GitHub CLI (if installed)**
```bash
gh repo create TestApp --public --source=. --remote=origin --push
```

**Option B: Manual Setup**
1. Go to https://github.com/new
2. Create a new repository (don't initialize with README)
3. Copy the repository URL
4. Run these commands:

```bash
git remote add origin https://github.com/YOUR_USERNAME/TestApp.git
git branch -M main
git push -u origin main
```

### 5. Verify
```bash
git remote -v
git status
```

## Important Notes

- **`.env` file is ignored** - Contains sensitive credentials
- **Docker volumes** are ignored - `postgres_data/` won't be committed
- **Python cache files** are ignored - `__pycache__/` won't be committed

## Recommended Repository Settings

1. Add a **README.md** (already exists)
2. Add a **LICENSE** file
3. Enable **Issues** and **Pull Requests**
4. Add repository topics: `django`, `postgresql`, `docker`, `python`

## Files Included in Repository

✅ All source code
✅ Docker configuration
✅ Deployment scripts
✅ Documentation
✅ Test files
✅ VS Code settings

## Files Excluded (via .gitignore)

❌ `.env` - Environment variables
❌ `__pycache__/` - Python cache
❌ `postgres_data/` - Database volumes
❌ `.DS_Store` - OS files
❌ Virtual environments
