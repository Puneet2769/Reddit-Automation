import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Email configuration
EMAIL_ADDRESS = "jackmortan21@gmail.com"  # Your Yahoo email address
EMAIL_PASSWORD = "hxio dabt lufc kmpk"  # App-specific password (not your regular password)

def send_email(subject, body, recipient_email):
    try:
        # Email setup
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
    
        # Connect to Gmail server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())


        logging.info(f"Email sent successfully to {recipient_email}: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email. Error: {e}")

# # Example usage
# send_email(
#     subject="Test Email",
#     body="This is a test email sent using Yahoo SMTP.",
#     recipient_email="recipient@example.com"
# )
