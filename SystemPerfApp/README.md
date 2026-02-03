# System Performance Monitoring Application

A full-stack application for monitoring system performance metrics (CPU, Memory, Disk, Network) with a Django REST API backend, React frontend, and PostgreSQL database. Fully containerized with Docker and cross-platform compatible (Windows, macOS, Linux).

## Features

- **Real-time System Metrics Collection**: CPU, Memory, Disk, and Network usage
- **Cross-platform Support**: Works on Windows, macOS, and Linux
- **Historical Data**: Store and visualize performance metrics over time
- **Interactive Dashboard**: React-based UI with charts and real-time updates
- **RESTful API**: Django REST Framework for metric collection and retrieval
- **Dockerized**: Complete containerization with Docker Compose

## Architecture

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: React 18 with Recharts for visualization
- **Database**: PostgreSQL 15
- **Containerization**: Docker Compose with separate containers for each service

## Prerequisites

- Docker Desktop (for Windows/macOS) or Docker Engine (for Linux)
- Docker Compose (included with Docker Desktop)

### Windows Setup

1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Ensure WSL2 backend is enabled (recommended)
3. Make sure Docker Desktop is running before proceeding

### macOS Setup

1. Install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Make sure Docker Desktop is running

### Linux Setup

1. Install Docker Engine and Docker Compose
2. Ensure Docker daemon is running

## Quick Start

1. **Clone or navigate to the project directory**:
   ```bash
   cd SystemPerfApp
   ```

2. **Start all services with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

   This will:
   - Build the backend and frontend containers
   - Start PostgreSQL database
   - Run Django migrations
   - Start the Django development server
   - Serve the React frontend

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Django Admin: http://localhost:8000/admin/ (create superuser first)

4. **Create a Django superuser** (optional, for admin access):
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

## API Endpoints

- `POST /api/metrics/collect/` - Collect and store current system metrics
- `GET /api/metrics/` - Retrieve metrics (optional query param: `?hours=24`)
- `GET /api/metrics/latest/` - Get most recent metrics
- `GET /api/metrics/stats/` - Get aggregated statistics (optional query param: `?hours=24`)

## Environment Variables

You can customize the configuration using environment variables. Create a `.env` file in the root directory:

```env
POSTGRES_DB=perfapp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## Development

### Backend Development

To work on the backend:

```bash
# Access backend container
docker-compose exec backend bash

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests (if any)
python manage.py test
```

### Frontend Development

The frontend is built and served via nginx in production mode. For development with hot-reload:

1. Modify `docker-compose.yml` to use a development server
2. Or run locally:
   ```bash
   cd frontend
   npm install
   npm start
   ```

## Windows Compatibility Notes

- **Docker Desktop**: Requires Docker Desktop for Windows with WSL2 backend (recommended)
- **Volume Mounts**: The docker-compose.yml uses named volumes for PostgreSQL data, which works seamlessly on Windows
- **System Metrics**: The `psutil` library automatically handles Windows drive letters (C:, D:, etc.)
- **Line Endings**: `.gitattributes` file ensures consistent line endings across platforms

## Important Note: Host vs Container Metrics

By default, when running in Docker containers, the application collects metrics from **within the container**, not the host system. 

To collect **host system metrics**:

### Option 1: Run Backend on Host (Recommended for Production)
Run the Django backend directly on your host machine (outside Docker) while keeping the database and frontend containerized.

### Option 2: Linux Host Metrics Access
On Linux, you can mount host filesystems in `docker-compose.yml`:
```yaml
volumes:
  - /proc:/host/proc:ro
  - /sys:/host/sys:ro
  - /:/rootfs:ro
```
Then modify the collector to read from `/host/proc`, `/host/sys`, etc.

### Option 3: Docker Desktop Metrics (Windows/macOS)
Docker Desktop provides limited host metrics access. For full host metrics on Windows/macOS, consider running the backend directly on the host.

## Project Structure

```
SystemPerfApp/
├── backend/              # Django application
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── perfapp/         # Django project settings
│   └── metrics/         # Metrics app (models, views, collectors)
├── frontend/            # React application
│   ├── package.json
│   ├── Dockerfile
│   ├── nginx.conf
│   └── src/
│       ├── components/  # React components
│       └── services/    # API client
├── docker-compose.yml   # Multi-container orchestration
└── README.md
```

## Troubleshooting

### Database Connection Issues

If the backend can't connect to the database:
1. Ensure the `db` service is healthy (check with `docker-compose ps`)
2. Wait for the database to be ready (healthcheck should pass)
3. Check environment variables match in docker-compose.yml

### Port Conflicts

If ports 3000, 8000, or 5432 are already in use:
- Modify the port mappings in `docker-compose.yml`
- Or stop the conflicting services

### Windows-Specific Issues

- **WSL2**: Ensure Docker Desktop is using WSL2 backend
- **Permissions**: If you encounter permission issues, run Docker Desktop as administrator
- **Volume Access**: Named volumes work better than bind mounts on Windows

## Stopping the Application

```bash
docker-compose down
```

To also remove volumes (deletes database data):
```bash
docker-compose down -v
```

## License

This project is open source and available for use.
