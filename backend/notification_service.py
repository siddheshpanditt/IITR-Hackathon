import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        # Email configuration
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.email_user = os.environ.get('EMAIL_USER')
        self.email_password = os.environ.get('EMAIL_PASSWORD')
        self.admin_email = os.environ.get('ADMIN_EMAIL')
        
        # Telegram configuration
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        self.email_enabled = bool(self.email_user and self.email_password and self.admin_email)
        self.telegram_enabled = bool(self.telegram_token and self.telegram_chat_id)
        
        if not (self.email_enabled or self.telegram_enabled):
            logger.warning("No notification methods configured")

    def send_email(self, subject, body, is_html=False):
        if not self.email_enabled:
            logger.warning("Email not configured")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.admin_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Email sent: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def send_telegram(self, message):
        if not self.telegram_enabled:
            logger.warning("Telegram not configured")
            return False
            
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            logger.info("Telegram message sent")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send telegram: {e}")
            return False

    def notify_server_down(self, deployment_url, downtime_duration=None):
        subject = "🚨 Server Down Alert"
        
        duration_text = f" (Down for {downtime_duration})" if downtime_duration else ""
        
        email_body = f"""
        <h2>🚨 Deployment Monitor Alert</h2>
        <p><strong>Status:</strong> Server is DOWN{duration_text}</p>
        <p><strong>URL:</strong> {deployment_url}</p>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>The monitoring system will attempt automatic recovery.</p>
        """
        
        telegram_msg = f"🚨 <b>Server Down</b>\n\nURL: {deployment_url}{duration_text}\nTime: {datetime.now().strftime('%H:%M:%S')}"
        
        self.send_email(subject, email_body, is_html=True)
        self.send_telegram(telegram_msg)

    def notify_server_recovered(self, deployment_url):
        subject = "✅ Server Recovered"
        
        email_body = f"""
        <h2>✅ Server Recovery Notification</h2>
        <p><strong>Status:</strong> Server is back ONLINE</p>
        <p><strong>URL:</strong> {deployment_url}</p>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        telegram_msg = f"✅ <b>Server Recovered</b>\n\nURL: {deployment_url}\nTime: {datetime.now().strftime('%H:%M:%S')}"
        
        self.send_email(subject, email_body, is_html=True)
        self.send_telegram(telegram_msg)

    def notify_low_funds(self, current_balance, threshold):
        subject = "💰 Low Funds Alert"
        
        email_body = f"""
        <h2>💰 Low Funds Warning</h2>
        <p><strong>Current Balance:</strong> ${current_balance:.2f}</p>
        <p><strong>Threshold:</strong> ${threshold:.2f}</p>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Please add funds to prevent service interruption.</p>
        """
        
        telegram_msg = f"💰 <b>Low Funds Alert</b>\n\nBalance: ${current_balance:.2f}\nThreshold: ${threshold:.2f}"
        
        self.send_email(subject, email_body, is_html=True)
        self.send_telegram(telegram_msg)

    def send_weekly_report(self, report_data):
        subject = f"📊 Weekly Report - {report_data['week_start']} to {report_data['week_end']}"
        
        email_body = f"""
        <h2>📊 Weekly Deployment Report</h2>
        <h3>Summary</h3>
        <ul>
            <li><strong>Uptime:</strong> {report_data['uptime_percentage']:.1f}%</li>
            <li><strong>Average Latency:</strong> {report_data['avg_latency']:.1f}ms</li>
            <li><strong>Total Incidents:</strong> {report_data['total_incidents']}</li>
            <li><strong>Auto-fixes:</strong> {report_data['auto_fixes']}</li>
        </ul>
        
        <h3>System Metrics</h3>
        <ul>
            <li><strong>Average CPU:</strong> {report_data['avg_cpu']:.1f}%</li>
            <li><strong>Average Memory:</strong> {report_data['avg_memory']:.1f}%</li>
            <li><strong>Average Disk:</strong> {report_data['avg_disk']:.1f}%</li>
        </ul>
        
        <h3>Financial</h3>
        <ul>
            <li><strong>Current Balance:</strong> ${report_data['current_balance']:.2f}</li>
            <li><strong>Weekly Spend:</strong> ${report_data['weekly_spend']:.2f}</li>
        </ul>
        """
        
        self.send_email(subject, email_body, is_html=True)
    
    def send_test_email(self):
        """Send test email to verify configuration"""
        if not self.email_enabled:
            raise Exception("Email not configured")
        
        subject = "🚀 Website Monitor - Email Test"
        body = f"""
        <h2>🚀 Universal Website Monitor</h2>
        <p>This is a test email from your monitoring system!</p>
        
        <h3>✅ Email notifications are working correctly.</h3>
        
        <p>You will now receive alerts for:</p>
        <ul>
            <li>Server downtime</li>
            <li>Server recovery</li>
            <li>High resource usage</li>
            <li>SSL certificate issues</li>
            <li>Weekly performance reports</li>
        </ul>
        
        <p><strong>Generated at:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        self.send_email(subject, body, is_html=True)
        logger.info("Test email sent successfully")

# Global instance
notification_service = NotificationService()

# Reinitialize function for dynamic updates
def reinitialize_notifications():
    global notification_service
    notification_service = NotificationService()
    return notification_service