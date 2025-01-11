from email_notification import send_email
import time

# Initialize variables
print("Started")
subject = "Working Email from Reddit Bot"
body = "Hello, this is a Confirmation that email notification setup is working."
recipient_email = "puneet18112006@gmail.com"

# Loop to send emails
i = 0  # Start with 0 for a controlled loop
max_emails = 25

while i < max_emails:
    try:
        # # Send email
        # send_email(subject, body, recipient_email)
        # print(f"Email {i + 1} sent successfully.")
        
        # # Sleep intervals
        time.sleep(180)  # Wait for 3 minutes
        send_email(subject, body, recipient_email)
        print(f"Email {i + 2} sent successfully.")
        
        time.sleep(3600)  # Wait for 1 hour before the next iteration
        i += 2  # Increment email count appropriately
    except Exception as e:
        print(f"An error occurred: {e}")
