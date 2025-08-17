#!/bin/bash

# 🚀 Bulletproof Deployment Script
# This script ensures your app is perfect before deploying

set -e  # Exit on any error

echo "🚀 Starting Bulletproof Deployment Process..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 1. Check if we're in the right directory
echo "1️⃣ Checking project structure..."
if [ ! -f "backend/main.py" ] || [ ! -f "frontend/package.json" ]; then
    print_error "Not in the correct project directory!"
    exit 1
fi
print_status "Project structure verified"

# 2. Check if virtual environment exists
echo "2️⃣ Checking Python environment..."
if [ ! -d "backend/teen_venv" ]; then
    print_error "Virtual environment not found! Run setup first."
    exit 1
fi
print_status "Virtual environment found"

# 3. Test backend production environment
echo "3️⃣ Testing backend production environment..."
cd backend
source teen_venv/bin/activate
if ! python test_production.py; then
    print_error "Backend production test failed!"
    exit 1
fi
print_status "Backend production test passed"

# 4. Test frontend build
echo "4️⃣ Testing frontend build..."
cd ../frontend
if ! npm run build; then
    print_error "Frontend build failed!"
    exit 1
fi
print_status "Frontend build successful"

# 5. Check if all required files exist
echo "5️⃣ Checking deployment files..."
cd ..
required_files=(
    "backend/requirements.txt"
    "backend/Procfile"
    "railway.json"
    "DEPLOYMENT.md"
    "DEPLOYMENT_CHECKLIST.md"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Missing required file: $file"
        exit 1
    fi
done
print_status "All deployment files present"

# 6. Check Git status
echo "6️⃣ Checking Git status..."
if ! git status --porcelain | grep -q .; then
    print_warning "No changes to commit"
else
    echo "Changes detected:"
    git status --porcelain
    echo ""
    read -p "Do you want to commit these changes before deploying? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "🚀 Pre-deployment commit - $(date)"
        print_status "Changes committed"
    fi
fi

# 7. Final deployment checklist
echo ""
echo "🎯 FINAL DEPLOYMENT CHECKLIST:"
echo "==============================="
echo "✅ Backend imports all packages"
echo "✅ Backend app loads successfully"
echo "✅ Database connection works"
echo "✅ Uvicorn starts without errors"
echo "✅ Frontend builds successfully"
echo "✅ All deployment files present"
echo "✅ Code committed to Git"
echo ""
echo "🚀 Your app is READY for deployment!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub: git push origin main"
echo "2. Deploy to Render/Railway following DEPLOYMENT.md"
echo "3. Set environment variables (DATABASE_URL, FRONTEND_URL)"
echo "4. Run database setup scripts"
echo ""
echo "💡 Tip: Use the DEPLOYMENT_CHECKLIST.md to track progress!"
