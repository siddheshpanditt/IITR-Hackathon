# 🚀 Installation Guide

## Quick Start

```bash
python3 RUN.py
```

## Requirements

- Python 3.7+
- Internet connection (for dependency installation)

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/siddheshpanditt/universal-website-monitor.git
cd universal-website-monitor
```

### 2. Run Application
```bash
python3 RUN.py
```

### 3. Access Dashboard
- Open: http://localhost:5000
- Login: admin / admin123
- Or create new account

## Manual Installation

```bash
cd backend
pip install Flask Flask-CORS Flask-JWT-Extended Flask-SocketIO requests psutil
python3 app.py
```

## Environment Variables (Optional)

```bash
export DEPLOYMENT_URL="https://your-website.com"
export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export TELEGRAM_BOT_TOKEN="your-bot-token"
export MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
```