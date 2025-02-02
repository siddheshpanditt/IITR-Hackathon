import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from app import check_availability, validate_resources

def send_email(subject, body):
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    password = "your_password"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def daily_status_report():
    url = "http://example.com"  # Replace with your deployment URL
    is_available = check_availability(url)
    is_resources_valid, resource_message = validate_resources()
    
    status = "Online" if is_available else "Offline"
    resource_status = "Healthy" if is_resources_valid else "Unhealthy"
    
    subject = "Daily Deployment Status Report"
    body = f"Deployment Status: {status}\nResource Status: {resource_status}\n{resource_message}"
    
    send_email(subject, body)

# Schedule the daily status report
schedule.every().day.at("08:00").do(daily_status_report)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)