# 🚀 Universal Website Monitor - Quick Start

## ⚡ Instant Setup (Recommended)

```bash
# Run the complete application with all features
python3 START_MONITOR.py
```

## 🌐 Access the Application

- **URL**: http://localhost:5000
- **Username**: `admin`
- **Password**: `admin123`

## ✨ Features Available

### 🤖 AI-Powered Features
- **Failure Prediction**: AI predicts potential failures before they happen
- **Root Cause Analysis**: Automated analysis of system issues
- **Intelligent Alerting**: Smart alert filtering to prevent spam
- **Enhanced Self-Healing**: Multiple healing strategies for different issues

### 📊 Real-Time Monitoring
- **System Metrics**: Live CPU, Memory, Disk, Network monitoring
- **URL Monitoring**: Monitor multiple websites with healing capabilities
- **WebSocket Updates**: Real-time dashboard updates every 3 seconds
- **Health Scoring**: Overall system health score calculation

### 🔧 Self-Healing Capabilities
- **Automatic Recovery**: Auto-heal memory pressure, CPU overload, network issues
- **URL Healing**: Automatic protocol switching and www prefix addition
- **Proactive Actions**: Preventive measures based on AI predictions
- **Resource Optimization**: Memory cleanup and process optimization

### 💰 Financial Monitoring
- **Balance Tracking**: Monitor deployment costs (demo mode)
- **Transaction History**: Complete audit trail of expenses
- **Low Fund Alerts**: Automatic notifications when balance is low
- **Runway Estimation**: Predict how long current balance will last

### 📧 Notifications
- **Email Alerts**: Server down/recovery notifications
- **Telegram Integration**: Instant mobile notifications
- **Weekly Reports**: Automated performance summaries
- **Smart Filtering**: Prevent alert storms and duplicates

### 🔍 Advanced Monitoring
- **SSL Certificate Checking**: Monitor certificate expiration
- **DNS Resolution**: Check domain name resolution
- **Port Status**: Verify service port availability
- **Security Events**: Track security-related incidents

### 📋 Production Features
- **Audit Logging**: Complete audit trail for compliance
- **Log Search**: Search through application logs
- **Performance Metrics**: Track API response times
- **Security Monitoring**: Monitor failed login attempts

## 🛠️ Alternative Startup Methods

### Method 1: Direct Python
```bash
cd backend
python3 app.py
```

### Method 2: Using the run script
```bash
python3 run_app.py
```

### Method 3: Manual setup
```bash
cd backend
pip install -r requirements.txt
export DEPLOYMENT_URL="https://your-website.com"
python3 app.py
```

## 🔧 Configuration (Optional)

### MongoDB Database
```bash
export MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
```

### Email Notifications
```bash
export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export ADMIN_EMAIL="admin@yourcompany.com"
```

### Telegram Notifications
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

### Custom Monitoring URL
```bash
export DEPLOYMENT_URL="https://your-website.com"
```

## 🎯 Dashboard Sections

1. **Overview**: System status and health score
2. **Metrics**: Real-time CPU, Memory, Disk usage
3. **AI Features**: Failure prediction and healing stats
4. **URL Monitor**: Add and monitor multiple websites
5. **Financial**: Balance and transaction tracking
6. **Alerts**: Recent alerts and notifications
7. **Reports**: Daily and weekly summaries
8. **Logs**: Search and view application logs

## 🧪 Testing Features

The application includes a built-in test suite that runs automatically. You can also run tests manually:

```bash
python3 test_features.py
```

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Missing Dependencies
```bash
pip3 install Flask Flask-CORS Flask-JWT-Extended Flask-SocketIO requests psutil
```

### Permission Issues
```bash
chmod +x START_MONITOR.py
```

## 📱 Mobile Access

The dashboard is fully responsive and works on mobile devices. Access the same URL from your phone for mobile monitoring.

## 🔒 Security

- JWT-based authentication
- Secure password hashing
- Rate limiting on sensitive endpoints
- Audit logging for all actions
- Security event monitoring

---

**🎉 Enjoy monitoring your deployments with AI-powered insights!**