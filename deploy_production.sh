#!/bin/bash

# ============================================
# AUTO-P / AutoIntel - Production Deployment Script
# ============================================
# This script automates the deployment to Railway (backend) and Vercel (frontend)
# Prerequisites: 
# - Railway CLI installed
# - Vercel CLI installed
# - Git configured

set -e  # Exit on error

echo "🚀 Starting AutoIntel Production Deployment..."
echo "=============================================="

# ============================================
# STEP 1: Clean the project
# ============================================
echo "📦 Step 1: Cleaning project..."
rm -f *.log *.pid
rm -f backend/*.log backend/*.pid
rm -f frontend/*.log frontend/*.pid
rm -f backend/default_*.sqlite3
rm -rf backend/__pycache__
rm -rf frontend/.vite frontend/dist
echo "✅ Cleanup complete"

# ============================================
# STEP 2: Verify environment files
# ============================================
echo "🔐 Step 2: Checking environment files..."
if [ ! -f .env.production ]; then
    echo "⚠️  .env.production not found. Creating from example..."
    cp .env.production.example .env.production
    echo "❗ Please edit .env.production with your actual values before deploying!"
    echo "❗ Press Enter to continue or Ctrl+C to abort..."
    read
fi

if [ ! -f backend/.env ]; then
    echo "⚠️  backend/.env not found. Creating from example..."
    cp backend/.env.example backend/.env
    echo "❗ Please edit backend/.env with your actual values!"
fi

if [ ! -f frontend/.env.production ]; then
    echo "⚠️  frontend/.env.production not found. Creating from example..."
    cp frontend/.env.production.example frontend/.env.production
    echo "❗ Please edit frontend/.env.production with your actual values!"
fi

echo "✅ Environment files checked"

# ============================================
# STEP 3: Git preparation
# ============================================
echo "📝 Step 3: Preparing Git..."
git add .
git commit -m "chore: prepare for production deployment" || echo "No changes to commit"
echo "✅ Git prepared"

# ============================================
# STEP 4: Deploy Backend to Railway
# ============================================
echo "☁️  Step 4: Deploying Backend to Railway..."
if command -v railway &> /dev/null; then
    railway login
    railway init
    railway up
    
    # Get the backend URL
    BACKEND_URL=$(railway domain)
    echo "🔗 Backend URL: $BACKEND_URL"
    
    # Add PostgreSQL database
    echo "📊 Adding PostgreSQL database..."
    railway add postgresql
    
    # Set environment variables
    echo "🔧 Setting environment variables..."
    railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
    railway variables set DEBUG=False
    railway variables set ALLOWED_HOSTS=$BACKEND_URL
    railway variables set CORS_ORIGINS=https://your-frontend.vercel.app
    railway variables set FRONTEND_URL=https://your-frontend.vercel.app
    
    echo "✅ Backend deployed to Railway"
    echo "❗ Don't forget to set STRIPE keys in Railway dashboard!"
else
    echo "⚠️  Railway CLI not found. Skipping backend deployment."
    echo "   Install with: npm install -g @railway/cli"
fi

# ============================================
# STEP 5: Deploy Frontend to Vercel
# ============================================
echo "⚡ Step 5: Deploying Frontend to Vercel..."
if command -v vercel &> /dev/null; then
    cd frontend
    vercel --prod
    
    # Get the frontend URL
    FRONTEND_URL=$(vercel ls --prod | head -n 1 | awk '{print $2}')
    echo "🔗 Frontend URL: $FRONTEND_URL"
    
    cd ..
    
    echo "✅ Frontend deployed to Vercel"
else
    echo "⚠️  Vercel CLI not found. Skipping frontend deployment."
    echo "   Install with: npm install -g vercel"
fi

# ============================================
# STEP 6: Configure Stripe Webhooks
# ============================================
echo "💳 Step 6: Stripe Webhook Configuration"
echo "❗ Manual step required:"
echo "   1. Go to Stripe Dashboard > Developers > Webhooks"
echo "   2. Add endpoint: $BACKEND_URL/api/subscriptions/webhook/"
echo "   3. Select events: checkout.session.completed, customer.subscription.deleted, etc."
echo "   4. Copy webhook secret and add to Railway environment variables"
echo ""

# ============================================
# STEP 7: Final verification
# ============================================
echo "✅ Step 7: Deployment Summary"
echo "=============================================="
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: $FRONTEND_URL"
echo ""
echo "🔧 Post-deployment checklist:"
echo "  [ ] Update CORS_ORIGINS in Railway with actual frontend URL"
echo "  [ ] Set STRIPE_SECRET_KEY and STRIPE_PUBLIC_KEY in Railway"
echo "  [ ] Set STRIPE_WEBHOOK_SECRET in Railway"
echo "  [ ] Set VITE_API_URL in Vercel to backend URL"
echo "  [ ] Test authentication flow"
echo "  [ ] Test payment flow"
echo "  [ ] Configure custom domains (optional)"
echo ""
echo "🎉 Deployment complete!"
