#!/bin/bash

# Test Runner Script for Django App
# Runs comprehensive tests to verify the application is working correctly

set -e

echo "🧪 Running Django App Test Suite"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if containers are running
echo "1️⃣  Checking container status..."
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Containers are not running. Start them with: docker-compose up -d"
    exit 1
fi
echo "✅ Containers are running"
echo ""

# Test 1: Django system check
echo "2️⃣  Running Django system check..."
docker-compose exec -T web python manage.py check
echo "✅ System check passed"
echo ""

# Test 2: Database connection
echo "3️⃣  Testing database connection..."
docker-compose exec -T db psql -U postgres -d testapp -c "SELECT 1;" > /dev/null
echo "✅ Database connection successful"
echo ""

# Test 3: HTTP endpoint test
echo "4️⃣  Testing HTTP endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Web server responding (HTTP $HTTP_CODE)"
else
    echo "⚠️  Web server returned HTTP $HTTP_CODE"
fi
echo ""

# Test 4: Run Django test suite
echo "5️⃣  Running Django test suite..."
docker-compose exec -T web python manage.py test TestApp.tests --verbosity=1
echo ""

# Test 5: Check migrations
echo "6️⃣  Checking migrations..."
docker-compose exec -T web python manage.py showmigrations | tail -5
echo ""

# Test 6: Database tables
echo "7️⃣  Verifying database tables..."
TABLE_COUNT=$(docker-compose exec -T db psql -U postgres -d testapp -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
echo "✅ Found $TABLE_COUNT tables in database"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Test suite completed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
