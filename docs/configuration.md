# ⚙️ Configuration Guide

## Environment Variables

### Required (Auto-set)
```bash
DEPLOYMENT_URL="https://google.com"    # Default monitoring URL
JWT_SECRET_KEY="monitor-key-2024"      # JWT secret
PORT="5000"                            # Server port
```

### Optional - Database
```bash
MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
MONGODB_DATABASE="deployment_monitor"
```

### Optional - Email Notifications
```bash
EMAIL_USER="your-email@gmail.com"
EMAIL_PASSWORD="your-app-password"
ADMIN_EMAIL="admin@company.com"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"
```

### Optional - Telegram Notifications
```bash
TELEGRAM_BOT_TOKEN="your-bot-token"
TELEGRAM_CHAT_ID="your-chat-id"
```

### Optional - Financial Monitoring
```bash
SPHERON_API_KEY="your-spheron-api-key"
LOW_BALANCE_THRESHOLD="10.0"
```

## Configuration Files

### users.json (Auto-created)
```json
{
  "admin": {
    "username": "admin",
    "password_hash": "hashed_password",
    "email": "admin@monitor.com",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### monitored_urls.json (Auto-created)
```json
{
  "https://example.com": {
    "url": "https://example.com",
    "status": "active",
    "last_check": "2024-01-01T00:00:00",
    "is_online": true,
    "response_time": 150
  }
}
```

## Runtime Configuration

### Monitoring Intervals
- System metrics: 3 seconds
- URL checks: On-demand
- Balance checks: 30 seconds
- Daily reports: Midnight
- Weekly reports: Monday 9 AM

### Alert Thresholds
- CPU: 80%
- Memory: 85%
- Disk: 90%
- Latency: 5000ms

### Self-Healing Cooldowns
- Fix deployment: 5 minutes
- Memory cleanup: 1 minute
- CPU optimization: 2 minutes