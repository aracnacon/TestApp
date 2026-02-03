# TestApp

## Quick Deployment

Use the automated deployment script:
```bash
./djangoAppdeploy.sh
```

This script will:
- Build and start Docker containers
- Create the database if it doesn't exist
- Run Django migrations
- Collect static files
- Display status and access URLs

## Manual Setup

If you prefer manual setup:

### Start containers
```bash
docker-compose up --build
```

### Create database (if needed)
```bash
docker-compose exec db psql -U postgres -c "CREATE DATABASE testapp;"
```

### Run migrations
```bash
docker-compose exec web python manage.py migrate
```

### Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

## Access

- **Django App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Useful Commands

```bash
# View logs
docker-compose logs -f web

# Stop containers
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# Restart containers
docker-compose restart
```
