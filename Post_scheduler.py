import time
import threading
import pandas as pd
import random
import logging
from reddit_auth import authenticate
from email_notification import send_email
from datetime import datetime, timezone

# Setup logging
logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def email_scheduler():
    subject = "Working Email from Reddit Bot"
    body = "Hello, this is a Confirmation that email notification setup is working."
    recipient_email = "puneet18112006@gmail.com"

    # Send first email after 3 minutes
    time.sleep(180)  # 3 minutes
    try:
        send_email(subject, body, recipient_email)
        logging.info("First email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending first email: {e}")

    # Send emails every hour
    email_count = 0
    max_emails = 25  # Optional limit for safety
    while email_count < max_emails:
        try:
            time.sleep(3600)  # 1 hour
            send_email(subject, body, recipient_email)
            email_count += 1
            logging.info(f"Email {email_count} sent successfully.")
        except Exception as e:
            logging.error(f"Error sending email {email_count + 1}: {e}")


def post_scheduler():
    reddit = authenticate()
    subreddit_name = "AskReddit"  # Current subreddit
    subreddit = reddit.subreddit(subreddit_name)

    try:
        df = pd.read_excel("questions.xlsx")
        questions = df["Question"].dropna().tolist()
    except FileNotFoundError:
        logging.error("Error: 'questions.xlsx' file not found!")
        return

    posted_questions = set()
    try:
        with open("posted_questions.txt", "r") as file:
            posted_questions.update(file.read().splitlines())
    except FileNotFoundError:
        logging.info("No previous 'posted_questions.txt' found. Starting fresh.")

    for question in questions:
        if question in posted_questions:
            logging.info(f"Skipping already posted question: {question}")
            continue

        try:
            logging.info(f"Posting: {question}")
            submission = subreddit.submit(title=question, selftext="")
            post_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            post_url = f"https://www.reddit.com{submission.permalink}"
            logging.info(f"Posted successfully: {question} at {post_time}")

            subject = "Reddit Automation - Post Update"
            body = (
                f"Hello,\n\n"
                f"A new Reddit post has been processed. Here are the details:\n\n"
                f"Status: Success\n"
                f"Question: {question}\n"
                f"Subreddit: {subreddit_name}\n"
                f"Post Time: {post_time}\n"
                f"Post URL: {post_url}\n\n"
                f"Best regards,\n"
                f"Your Reddit Automation Bot"
            )
            send_email(subject, body, "puneet18112006@gmail.com")

            with open("posted_questions.txt", "a") as file:
                file.write(f"{question}\n")

            wait_time = random.randint(11, 13) * 3600  # Wait 11 to 13 hours
            logging.info(f"Waiting for {wait_time // 3600} hours before the next post...")
            time.sleep(wait_time)

        except Exception as e:
            logging.error(f"Error posting question: {question}. Exception: {e}")
            continue

if __name__ == "__main__":
    # Run both schedulers concurrently
    email_thread = threading.Thread(target=email_scheduler)
    post_thread = threading.Thread(target=post_scheduler)

    email_thread.start()
    post_thread.start()

    email_thread.join()
    post_thread.join()
