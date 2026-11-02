@echo off
REM ============================================
REM AUTO-P / AutoIntel - Production Deployment Script (Windows)
REM ============================================
REM This script automates the deployment to Railway (backend) and Vercel (frontend)

echo 🚀 Starting AutoIntel Production Deployment...
echo ==============================================

REM ============================================
REM STEP 1: Clean the project
REM ============================================
echo 📦 Step 1: Cleaning project...
del /Q *.log *.pid 2>nul
del /Q backend\*.log backend\*.pid 2>nul
del /Q backend\default_*.sqlite3 2>nul
rmdir /S /Q backend\__pycache__ 2>nul
rmdir /S /Q frontend\.vite frontend\dist 2>nul
echo ✅ Cleanup complete

REM ============================================
REM STEP 2: Verify environment files
REM ============================================
echo 🔐 Step 2: Checking environment files...
if not exist .env.production (
    echo ⚠️  .env.production not found. Creating from example...
    copy .env.production.example .env.production
    echo ❗ Please edit .env.production with your actual values before deploying!
    echo ❗ Press Enter to continue or Ctrl+C to abort...
    pause
)

if not exist backend\.env (
    echo ⚠️  backend\.env not found. Creating from example...
    copy backend\.env.example backend\.env
    echo ❗ Please edit backend\.env with your actual values!
)

if not exist frontend\.env.production (
    echo ⚠️  frontend\.env.production not found. Creating from example...
    if exist frontend\.env.production.example (
        copy frontend\.env.production.example frontend\.env.production
    ) else (
        echo VITE_API_URL=https://your-backend-url.railway.app > frontend\.env.production
    )
    echo ❗ Please edit frontend\.env.production with your actual values!
)

echo ✅ Environment files checked

REM ============================================
REM STEP 3: Git preparation
REM ============================================
echo 📝 Step 3: Preparing Git...
git add .
git commit -m "chore: prepare for production deployment" 2>nul || echo No changes to commit
echo ✅ Git prepared

REM ============================================
REM STEP 4: Deploy Backend to Railway
REM ============================================
echo ☁️  Step 4: Deploying Backend to Railway...
where railway >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    railway login
    railway init
    railway up
    
    echo 📊 Adding PostgreSQL database...
    railway add postgresql
    
    echo 🔧 Setting environment variables...
    echo ❗ Please set these variables in Railway dashboard:
    echo    - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_hex(32))")
    echo    - DEBUG=False
    echo    - ALLOWED_HOSTS=your-backend-url.railway.app
    echo    - CORS_ORIGINS=https://your-frontend.vercel.app
    echo    - FRONTEND_URL=https://your-frontend.vercel.app
    echo    - STRIPE_SECRET_KEY
    echo    - STRIPE_PUBLIC_KEY
    echo    - STRIPE_WEBHOOK_SECRET
    
    echo ✅ Backend deployed to Railway
) else (
    echo ⚠️  Railway CLI not found. Skipping backend deployment.
    echo    Install with: npm install -g @railway/cli
)

REM ============================================
REM STEP 5: Deploy Frontend to Vercel
REM ============================================
echo ⚡ Step 5: Deploying Frontend to Vercel...
where vercel >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    cd frontend
    vercel --prod
    cd ..
    
    echo ✅ Frontend deployed to Vercel
) else (
    echo ⚠️  Vercel CLI not found. Skipping frontend deployment.
    echo    Install with: npm install -g vercel
)

REM ============================================
REM STEP 6: Configure Stripe Webhooks
REM ============================================
echo 💳 Step 6: Stripe Webhook Configuration
echo ❗ Manual step required:
echo    1. Go to Stripe Dashboard ^> Developers ^> Webhooks
echo    2. Add endpoint: https://your-backend-url.railway.app/api/subscriptions/webhook/
echo    3. Select events: checkout.session.completed, customer.subscription.deleted, etc.
echo    4. Copy webhook secret and add to Railway environment variables
echo.

REM ============================================
REM STEP 7: Final verification
REM ============================================
echo ✅ Step 7: Deployment Summary
echo ==============================================
echo Backend URL: Check Railway dashboard
echo Frontend URL: Check Vercel dashboard
echo.
echo 🔧 Post-deployment checklist:
echo   [ ] Update CORS_ORIGINS in Railway with actual frontend URL
echo   [ ] Set STRIPE_SECRET_KEY and STRIPE_PUBLIC_KEY in Railway
echo   [ ] Set STRIPE_WEBHOOK_SECRET in Railway
echo   [ ] Set VITE_API_URL in Vercel to backend URL
echo   [ ] Test authentication flow
echo   [ ] Test payment flow
echo   [ ] Configure custom domains (optional)
echo.
echo 🎉 Deployment complete!
pause
