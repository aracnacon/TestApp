# Recommended Extensions & Packages

## 📦 Python/Django Packages (requirements.txt)

### Core (Already Included)
- **Django 5.0.1** - Web framework
- **psycopg2-binary 2.9.9** - PostgreSQL adapter

### Development & Debugging
- **django-debug-toolbar** - Debug panel for development
- **django-extensions** - Useful management commands (shell_plus, graph_models, etc.)

### API Development
- **djangorestframework** - REST API framework
- **django-cors-headers** - Handle CORS for API requests

### Environment Management
- **python-decouple** - Better environment variable management
- **django-environ** - Environment variable handling

### Code Quality
- **black** - Code formatter
- **flake8** - Linter

### Production
- **gunicorn** - Production WSGI server
- **whitenoise** - Static file serving

## 🔌 VS Code / Cursor Extensions

### Essential Extensions
1. **Python** (ms-python.python) - Python language support
2. **Pylance** (ms-python.vscode-pylance) - Fast Python language server
3. **Black Formatter** (ms-python.black-formatter) - Code formatting
4. **Flake8** (ms-python.flake8) - Linting
5. **Docker** (ms-azuretools.vscode-docker) - Docker support

### Recommended Extensions
- **ESLint** (dbaeumer.vscode-eslint) - JavaScript linting
- **Prettier** (esbenp.prettier-vscode) - Code formatter
- **JSON** (ms-vscode.vscode-json) - JSON support

## 🚀 Installation

### Install Python Packages
```bash
docker-compose exec web pip install -r requirements.txt
```

Or rebuild the container:
```bash
docker-compose up --build
```

### Install VS Code Extensions
The `.vscode/extensions.json` file will prompt you to install recommended extensions when you open the project in VS Code/Cursor.

## ⚙️ Configuration

### Django Settings Updates Needed

To use these extensions, update `TestApp/settings.py`:

```python
# Add to INSTALLED_APPS (if using debug toolbar)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

INSTALLED_APPS += [
    'django_extensions',
    'rest_framework',  # If using DRF
    'corsheaders',     # If using CORS
]

# Add to MIDDLEWARE (if using debug toolbar)
if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Add CORS middleware (if using CORS)
MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')

# Debug Toolbar settings
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
```

## 📝 Usage Examples

### Django Extensions Commands
```bash
# Enhanced shell
docker-compose exec web python manage.py shell_plus

# Generate model graph
docker-compose exec web python manage.py graph_models -a -o models.png
```

### Code Formatting
```bash
# Format all Python files
docker-compose exec web black .

# Check code style
docker-compose exec web flake8 .
```

## 🎯 Optional Extensions (Add as needed)

### Database Tools
- **django-dbbackup** - Database backup/restore
- **django-admin-interface** - Better admin UI

### Authentication
- **django-allauth** - Social authentication
- **djangorestframework-simplejwt** - JWT authentication

### Testing
- **pytest-django** - Pytest for Django
- **coverage** - Code coverage

### Monitoring
- **sentry-sdk** - Error tracking
- **django-prometheus** - Metrics
