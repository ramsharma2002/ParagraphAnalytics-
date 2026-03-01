# Paragraph Analytics - Project Setup Guide

## Overview
Paragraph Analytics is a Django web application that allows users to analyze text content, track word frequencies, and search for specific words across paragraphs. This application features a modern UI with Bootstrap 5, user authentication, and background text processing.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation Steps

### 1. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
The application uses hardcoded settings for development. For production, update `config/settings.py`:
```python
SECRET_KEY = 'your-production-secret-key'
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

### 4. Database Setup
```bash
# Apply database migrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure
```
paragraph_analytics/
├── config/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main configuration file
│   ├── urls.py            # Main URL patterns
│   └── wsgi.py            # WSGI configuration
├── users/                 # User authentication app
│   ├── models.py          # Custom User model (email-based auth)
│   ├── views.py           # Login, register, logout views
│   └── urls.py            # User-related URLs
├── paragraphs/            # Main functionality app
│   ├── models.py          # Paragraph and WordFrequency models
│   ├── views.py           # Dashboard and search views
│   ├── tasks.py           # Celery tasks for background processing
│   └── urls.py            # Paragraph-related URLs
├── templates/             # Global templates
│   ├── base.html          # Base template with Bootstrap 5
│   ├── login.html         # Modern login page with validation
│   ├── register.html      # Registration page with password confirmation
│   ├── dashboard.html     # Main dashboard interface
│   └── search.html        # Search results page
├── venv/                  # Virtual environment
├── db.sqlite3            # SQLite database (default)
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── API_DOCUMENTATION.md  # API reference documentation
```

## Features

### User Authentication
- **Modern Registration**: Email-based registration with password confirmation
- **Secure Login**: JWT-ready authentication with Django sessions
- **Custom User Model**: Email as username field with custom User model
- **Password Validation**: Client-side validation with visual feedback

### Text Analysis
- **Paragraph Submission**: Submit multiple paragraphs at once
- **Word Frequency Tracking**: Automatic counting and storage of word frequencies
- **Background Processing**: Celery integration with synchronous fallback
- **Real-time Updates**: Immediate feedback on processing status

### Search Functionality
- **Word Search**: Search for specific words across all user paragraphs
- **Ranked Results**: Results sorted by word count and relevance
- **Context Display**: Shows paragraph content with word counts

### Modern UI/UX
- **Bootstrap 5**: Responsive, modern design framework
- **Interactive Forms**: Real-time validation and user feedback
- **Password Toggle**: Show/hide password functionality
- **Error Handling**: User-friendly error messages and alerts
- **Responsive Design**: Works on desktop, tablet, and mobile

### Admin Interface
- **Django Admin**: Full admin panel for data management
- **User Management**: Manage users and their content
- **Content Oversight**: Monitor paragraphs and word frequencies

## URL Structure

### Authentication URLs
- `/login/` - User login page
- `/register/` - User registration page  
- `/logout/` - User logout

### Application URLs
- `/dashboard/` - Main dashboard and paragraph submission
- `/search/` - Word search functionality
- `/admin/` - Django admin panel

## Configuration Options

### Current Settings
The application uses these default settings in `config/settings.py`:
- **Database**: SQLite (development)
- **Authentication**: Custom User model with email field
- **Debug Mode**: Enabled for development
- **Static Files**: Django static files handling
- **Templates**: Jinja2/Django templates with Bootstrap 5

### Database Settings (Optional)
To use PostgreSQL instead of SQLite:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'paragraph_analytics',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Celery Configuration (Optional)
For background task processing with Redis:
1. Install and start Redis
2. Add to `settings.py`:
```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```
3. Start Celery worker:
```bash
celery -A paragraph_analytics worker -l info
```

## Common Issues & Solutions

### 1. Migration Issues
```bash
# Reset database (caution: deletes all data)
python manage.py flush
python manage.py migrate
```

### 2. Celery Connection Errors
The application automatically falls back to synchronous processing if Redis/Celery is not available.

### 3. Static Files Not Loading
Ensure `DEBUG=True` in development or run:
```bash
python manage.py collectstatic
```

### 4. Template Not Found
Check that templates are in the correct directories and that `TEMPLATES` setting includes `BASE_DIR / "templates"`.

## Development Workflow

### Adding New Features
1. Create models in the appropriate app
2. Add views and URL patterns
3. Create or update templates
4. Run migrations if models changed
5. Test the functionality

### Database Operations
```python
# Get user's paragraphs
from paragraphs.models import Paragraph, WordFrequency
paragraphs = Paragraph.objects.filter(user=request.user)

# Get word frequencies for user
words = WordFrequency.objects.filter(user=request.user).order_by('-count')

# Create new paragraph
paragraph = Paragraph.objects.create(
    user=request.user,
    content="Your paragraph text here"
)
```

### Frontend Development
- **Bootstrap 5**: Use Bootstrap classes for styling
- **JavaScript**: Form validation and interactive elements
- **Icons**: Bootstrap Icons or inline SVGs
- **Responsive**: Mobile-first design approach

## Production Deployment

### Security Settings
Update `config/settings.py` for production:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'your-production-secret-key'

# Use environment variables
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
```

### Web Server Setup
- **WSGI Server**: Gunicorn recommended
- **Reverse Proxy**: Nginx or Apache
- **SSL**: Configure HTTPS certificates
- **Static Files**: Serve via Nginx or collectstatic

### Environment Variables
```bash
export DEBUG=False
export SECRET_KEY='your-production-secret'
export DATABASE_URL='postgresql://user:pass@localhost/dbname'
```

## API Integration
The application is API-ready with Django REST Framework. See `API_DOCUMENTATION.md` for complete API reference.

## Support & Troubleshooting

### Common Debugging Steps
1. Check Django logs: `python manage.py runserver --verbosity=2`
2. Verify database: `python manage.py dbshell`
3. Test models: `python manage.py shell`
4. Check URLs: `python manage.py show_urls`

### Performance Tips
- Use `select_related()` and `prefetch_related()` for database queries
- Implement pagination for large datasets
- Consider database indexing for frequent queries
- Use Celery for long-running tasks

## License
[Add your license information here]
