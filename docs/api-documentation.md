# 🔌 API Documentation

## Authentication

### Login
```
POST /auth/login
{
  "username": "admin",
  "password": "admin123"
}
```

### Signup
```
POST /auth/signup
{
  "username": "newuser",
  "password": "password123",
  "email": "user@example.com"
}
```

## System Monitoring

### Get Real Metrics
```
GET /api/real-metrics
Authorization: Bearer <token>
```

### Get Status
```
GET /status
Authorization: Bearer <token>
```

## AI Features

### Failure Prediction
```
GET /ai/prediction
Authorization: Bearer <token>
```

### Alert Summary
```
GET /ai/alert-summary
Authorization: Bearer <token>
```

### Healing Stats
```
GET /ai/healing-stats
Authorization: Bearer <token>
```

### Trigger Healing
```
POST /ai/proactive-heal
Authorization: Bearer <token>
```

## URL Monitoring

### Add URL
```
POST /monitor-url
Authorization: Bearer <token>
{
  "url": "https://example.com"
}
```

### Get Monitored URLs
```
GET /monitored-urls
Authorization: Bearer <token>
```

### Check URL
```
POST /check-url
Authorization: Bearer <token>
{
  "url": "https://example.com"
}
```

### Remove URL
```
DELETE /remove-url
Authorization: Bearer <token>
{
  "url": "https://example.com"
}
```

## Self-Healing

### Fix Deployment
```
POST /fix
Authorization: Bearer <token>
```

### Heal URL
```
POST /heal-url
Authorization: Bearer <token>
{
  "url": "https://example.com"
}
```

## Financial

### Get Financial Data
```
GET /financial
Authorization: Bearer <token>
```

## Notifications

### Setup Email
```
POST /setup-email
Authorization: Bearer <token>
{
  "email_user": "user@gmail.com",
  "email_password": "password",
  "admin_email": "admin@company.com"
}
```

### Send Test Notification
```
POST /send-test-notification
Authorization: Bearer <token>
```