# Paragraph Analytics - API Documentation

## Overview
This document describes the REST API endpoints available in the Paragraph Analytics application. The API provides programmatic access to user authentication, paragraph management, and word frequency analysis.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Authentication

#### POST /api/auth/register/
Register a new user account.

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-03-01T10:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
    "email": ["A user with that email already exists."],
    "password": ["Password must be at least 8 characters."]
}
```

#### POST /api/auth/login/
Authenticate user and return JWT token.

**Request Body:**
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

**Error Response (401 Unauthorized):**
```json
{
    "detail": "No active account found with the given credentials"
}
```

#### POST /api/auth/refresh/
Refresh JWT access token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### POST /api/auth/logout/
Logout user (blacklist token).

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response (205 Reset Content):**
```json
{
    "detail": "Successfully logged out"
}
```

### Paragraphs

#### GET /api/paragraphs/
Get all paragraphs for the authenticated user.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (int): Page number for pagination (default: 1)
- `page_size` (int): Number of items per page (default: 20)

**Response (200 OK):**
```json
{
    "count": 45,
    "next": "http://127.0.0.1:8000/api/paragraphs/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "content": "This is a sample paragraph for analysis.",
            "word_count": 6,
            "created_at": "2024-03-01T10:00:00Z",
            "updated_at": "2024-03-01T10:00:00Z"
        }
    ]
}
```

#### POST /api/paragraphs/
Create a new paragraph for analysis.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
    "content": "This is a new paragraph to be analyzed for word frequencies."
}
```

**Response (201 Created):**
```json
{
    "id": 2,
    "content": "This is a new paragraph to be analyzed for word frequencies.",
    "word_count": 9,
    "created_at": "2024-03-01T10:05:00Z",
    "updated_at": "2024-03-01T10:05:00Z",
    "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### GET /api/paragraphs/{id}/
Get a specific paragraph by ID.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "content": "This is a sample paragraph for analysis.",
    "word_count": 6,
    "created_at": "2024-03-01T10:00:00Z",
    "updated_at": "2024-03-01T10:00:00Z",
    "word_frequencies": [
        {
            "word": "paragraph",
            "count": 1
        },
        {
            "word": "sample",
            "count": 1
        }
    ]
}
```

**Error Response (404 Not Found):**
```json
{
    "detail": "Paragraph not found"
}
```

#### PUT /api/paragraphs/{id}/
Update a paragraph content.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
    "content": "This is the updated paragraph content."
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "content": "This is the updated paragraph content.",
    "word_count": 5,
    "created_at": "2024-03-01T10:00:00Z",
    "updated_at": "2024-03-01T10:10:00Z"
}
```

#### DELETE /api/paragraphs/{id}/
Delete a paragraph.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response (204 No Content)**

### Word Frequencies

#### GET /api/word-frequencies/
Get word frequency statistics for the authenticated user.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `word` (string): Filter by specific word
- `min_count` (int): Minimum word count (default: 1)
- `limit` (int): Maximum number of results (default: 100)

**Response (200 OK):**
```json
{
    "count": 150,
    "results": [
        {
            "word": "the",
            "count": 45,
            "paragraphs_count": 12
        },
        {
            "word": "and",
            "count": 32,
            "paragraphs_count": 10
        }
    ]
}
```

#### GET /api/word-frequencies/{word}/
Get detailed information about a specific word.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
    "word": "analysis",
    "count": 8,
    "paragraphs_count": 3,
    "first_used": "2024-03-01T10:00:00Z",
    "last_used": "2024-03-01T10:05:00Z",
    "paragraphs": [
        {
            "id": 1,
            "content": "This paragraph contains analysis.",
            "count": 1
        }
    ]
}
```

### Search

#### GET /api/search/
Search for words across paragraphs.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `q` (string, required): Search query
- `exact_match` (boolean): Exact word match (default: false)
- `limit` (int): Maximum results (default: 10)

**Response (200 OK):**
```json
{
    "query": "analysis",
    "exact_match": false,
    "count": 3,
    "results": [
        {
            "paragraph_id": 1,
            "content": "This paragraph contains analysis.",
            "word_count": 1,
            "highlights": "This paragraph contains <mark>analysis</mark>."
        },
        {
            "paragraph_id": 2,
            "content": "Analysis is important for data.",
            "word_count": 1,
            "highlights": "<mark>Analysis</mark> is important for data."
        }
    ]
}
```

### Analytics

#### GET /api/analytics/overview/
Get overview statistics for the authenticated user.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
    "total_paragraphs": 25,
    "total_words": 1250,
    "unique_words": 180,
    "average_paragraph_length": 50,
    "most_common_words": [
        {"word": "the", "count": 45},
        {"word": "and", "count": 32}
    ],
    "recent_activity": [
        {
            "action": "paragraph_created",
            "timestamp": "2024-03-01T10:05:00Z",
            "details": "New paragraph added"
        }
    ]
}
```

#### GET /api/analytics/trends/
Get word usage trends over time.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `period` (string): Time period (day, week, month)
- `words` (string): Comma-separated list of words

**Response (200 OK):**
```json
{
    "period": "week",
    "data": [
        {
            "date": "2024-02-24",
            "analysis": 2,
            "data": 5
        },
        {
            "date": "2024-02-25",
            "analysis": 3,
            "data": 7
        }
    ]
}
```

### Tasks

#### GET /api/tasks/{task_id}/
Get status of background processing tasks.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "result": {
        "paragraph_id": 2,
        "words_processed": 9,
        "unique_words": 8
    },
    "created_at": "2024-03-01T10:05:00Z",
    "completed_at": "2024-03-01T10:05:02Z"
}
```

**Response (202 Accepted) - Task in progress:**
```json
{
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "progress": 75,
    "created_at": "2024-03-01T10:05:00Z"
}
```

## Error Responses

### Standard Error Format
All error responses follow this format:

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {
            "field_name": ["Specific error details"]
        }
    }
}
```

### Common HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `202 Accepted`: Request accepted for processing
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Rate Limiting
API requests are limited to:
- 1000 requests per hour per user
- 100 requests per minute per user

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Pagination
List endpoints support pagination using cursor-based pagination:

**Response Format:**
```json
{
    "count": 150,
    "next": "http://127.0.0.1:8000/api/paragraphs/?cursor=cD02MDIz...",
    "previous": "http://127.0.0.1:8000/api/paragraphs/?cursor=cjoxMA==",
    "results": [...]
}
```

## SDK Examples

### Python (requests)
```python
import requests

# Login
response = requests.post('http://127.0.0.1:8000/api/auth/login/', json={
    'email': 'user@example.com',
    'password': 'password'
})
token = response.json()['access']

# Get paragraphs
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://127.0.0.1:8000/api/paragraphs/', headers=headers)
paragraphs = response.json()['results']
```

### JavaScript (fetch)
```javascript
// Login
const loginResponse = await fetch('http://127.0.0.1:8000/api/auth/login/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'user@example.com',
        password: 'password'
    })
});
const {access} = await loginResponse.json();

// Get paragraphs
const paragraphsResponse = await fetch('http://127.0.0.1:8000/api/paragraphs/', {
    headers: {'Authorization': `Bearer ${access}`}
});
const paragraphs = await paragraphsResponse.json();
```

## Testing

### Running API Tests
```bash
# Run all API tests
python manage.py test api

# Run specific test
python manage.py test api.test_paragraphs
```

### Test Coverage
```bash
# Generate coverage report
coverage run --source='.' manage.py test
coverage report
```

## Changelog

### v1.0.0 (Current)
- User authentication with JWT
- Paragraph CRUD operations
- Word frequency analysis
- Search functionality
- Background task processing
- Analytics endpoints

### Upcoming Features
- Export functionality (CSV, JSON)
- Advanced search filters
- Real-time updates with WebSockets
- File upload support
- Collaborative features
