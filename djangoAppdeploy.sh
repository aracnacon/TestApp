#!/bin/bash

# Django App Deployment Script
# This script automates the deployment of Django + PostgreSQL Docker setup

set -e  # Exit on any error

echo "🚀 Starting Django App Deployment..."
echo ""

# Interactive Questions
echo "📝 Please provide the following information:"
echo ""

# Project Name
read -p "Project Name (e.g., TestApp): " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-TestApp}
echo "✅ Using project name: $PROJECT_NAME"
echo ""

# Database Configuration
read -p "Database Name (default: testapp): " DB_NAME
DB_NAME=${DB_NAME:-testapp}
echo "✅ Using database name: $DB_NAME"
echo ""

read -p "Database User (default: postgres): " DB_USER
DB_USER=${DB_USER:-postgres}
echo "✅ Using database user: $DB_USER"
echo ""

read -sp "Database Password (default: postgres): " DB_PASSWORD
DB_PASSWORD=${DB_PASSWORD:-postgres}
echo ""
echo "✅ Password set"
echo ""

# Port Configuration
read -p "Web Server Port (default: 8000): " WEB_PORT
WEB_PORT=${WEB_PORT:-8000}
echo "✅ Using web port: $WEB_PORT"
echo ""

read -p "Database Port (default: 5432): " DB_PORT
DB_PORT=${DB_PORT:-5432}
echo "✅ Using database port: $DB_PORT"
echo ""

# Confirmation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Deployment Configuration Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Project Name:     $PROJECT_NAME"
echo "  Database Name:   $DB_NAME"
echo "  Database User:   $DB_USER"
echo "  Database Port:   $DB_PORT"
echo "  Web Server Port: $WEB_PORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "Continue with deployment? (y/n): " CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled."
    exit 1
fi

echo ""
echo "🚀 Starting deployment..."
echo ""

# Update .env file with user inputs
echo "📝 Updating .env file..."
cat > .env << EOF
POSTGRES_DB=$DB_NAME
POSTGRES_USER=$DB_USER
POSTGRES_PASSWORD=$DB_PASSWORD
EOF
echo "✅ .env file updated"
echo ""

# Check if docker-compose.yml exists, if not create a template
if [ ! -f docker-compose.yml ]; then
    echo "⚠️  docker-compose.yml not found. Creating template..."
    cat > docker-compose.yml << EOF
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: \${POSTGRES_DB}
      POSTGRES_USER: \${POSTGRES_USER}
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "$DB_PORT:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:$WEB_PORT
    volumes:
      - .:/app
    ports:
      - "$WEB_PORT:$WEB_PORT"
    depends_on:
      - db
    environment:
      - POSTGRES_DB=\${POSTGRES_DB}
      - POSTGRES_USER=\${POSTGRES_USER}
      - POSTGRES_PASSWORD=\${POSTGRES_PASSWORD}
      - POSTGRES_HOST=db

volumes:
  postgres_data:
EOF
    echo "✅ docker-compose.yml created"
    echo ""
fi

# Step 1: Build and start containers
echo "📦 Building and starting Docker containers..."
docker-compose up -d --build

# Step 2: Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 5

# Step 3: Check if database exists, create if not
echo "🔍 Checking database..."
DB_EXISTS=$(docker-compose exec -T db psql -U $DB_USER -lqt 2>/dev/null | cut -d \| -f 1 | grep -w $DB_NAME | wc -l || echo "0")

if [ $DB_EXISTS -eq 0 ]; then
    echo "📊 Creating database: $DB_NAME..."
    docker-compose exec -T db psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "⚠️  Database might already exist or connection issue"
else
    echo "✅ Database already exists"
fi

# Step 4: Run migrations
echo "🔄 Running Django migrations..."
docker-compose exec -T web python manage.py migrate --noinput

# Step 5: Collect static files (if needed)
echo "📁 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput || true

# Step 6: Check container status
echo "🔍 Checking container status..."
docker-compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Deployment complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Django app is running at: http://localhost:$WEB_PORT"
echo "🔐 Admin panel: http://localhost:$WEB_PORT/admin"
echo ""
echo "📝 Next steps:"
echo "  • Create a superuser: docker-compose exec web python manage.py createsuperuser"
echo "  • View logs: docker-compose logs -f web"
echo "  • Stop containers: docker-compose down"
echo ""
