# 🔧 Troubleshooting Guide

## Common Issues

### Installation Issues

#### "No module named 'Flask'"
```bash
pip install Flask Flask-CORS Flask-JWT-Extended Flask-SocketIO requests psutil
```

#### "Port 5000 already in use"
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
# Or change port
export PORT=8080
```

#### "Permission denied"
```bash
chmod +x RUN.py
python3 RUN.py
```

### Login Issues

#### "Invalid credentials"
- Default: admin / admin123
- Create new account via signup
- Check users.json file exists

#### "JWT token expired"
- Refresh page and login again
- Token expires after 24 hours

### Monitoring Issues

#### "Failed to get metrics"
- Check psutil installation
- Restart application
- Check system permissions

#### "URL monitoring not working"
- Check internet connection
- Verify URL format (include https://)
- Check firewall settings

### Database Issues

#### "MongoDB connection failed"
- Application uses local JSON fallback
- Check MONGODB_URI environment variable
- Verify MongoDB Atlas credentials

#### "Data not persisting"
- Check file permissions in project directory
- Verify users.json and monitored_urls.json creation

### Performance Issues

#### "High CPU usage"
- Reduce monitoring frequency
- Check for infinite loops in logs
- Restart application

#### "Memory leaks"
- Application includes automatic garbage collection
- Restart if memory usage exceeds 1GB

### Notification Issues

#### "Email not sending"
- Check EMAIL_USER, EMAIL_PASSWORD, ADMIN_EMAIL
- Use app-specific password for Gmail
- Test with /setup-email endpoint

#### "Telegram not working"
- Verify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
- Check bot permissions
- Test bot with direct message

## Debug Mode

Enable debug logging:
```bash
export DEBUG=true
python3 RUN.py
```

## Log Files

Check logs in:
- `logs/app.log` - Application logs
- `logs/security.log` - Security events
- `logs/audit.log` - Audit trail
- `actions.log` - Action history

## Getting Help

1. Check this troubleshooting guide
2. Review log files for errors
3. Test with `python3 test_features.py`
4. Create GitHub issue with:
   - Error message
   - Steps to reproduce
   - System information
   - Log excerpts