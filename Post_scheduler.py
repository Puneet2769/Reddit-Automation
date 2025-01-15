import time
import pandas as pd
import random
import logging
from reddit_auth import authenticate
from email_notification import send_email
from datetime import datetime, timezone

# Setup logging
logging.basicConfig(
    filename="reddit_posting.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def post_to_reddit():
    reddit = authenticate()
    subreddit_name = "AskReddit"  # Current subreddit (can be expanded later)
    subreddit = reddit.subreddit(subreddit_name)

    # Load questions from Excel
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
            # Post the question
            logging.info(f"Posting: {question}")
            submission = subreddit.submit(title=question, selftext="")
            post_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            post_url = f"https://www.reddit.com{submission.permalink}"
            logging.info(f"Posted successfully: {question} at {post_time}")

            # Send email notification
            subject = "Reddit Automation - Post Update"
            body = (
                f"Hello,\n\n"
                f"A new Reddit post has been processed. Here are the details:\n\n"
                f"Status: Success\n"
                f"Question: {question}\n"
                f"Subreddit: {subreddit_name}\n"
                f"Post Time: {post_time}\n"
                f"Post URL: {post_url}\n\n"
                f"Automation Info:**\n"
                f"- Bot Name: RedditAutomationBot\n"
                f"- Script Version: v1.0\n\n"
                f"Best regards,\n"
                f"Your Reddit Automation Bot"
            )
            send_email(subject, body, "recipient@gmail.com")

            # Save the posted question
            with open("posted_questions.txt", "a") as file:
                file.write(f"{question}\n")

            # Wait before the next post
            wait_time = random.randint(11, 13) * 3600  # Random wait between 11 and 13 hours
            logging.info(f"Waiting for {wait_time // 3600} hours before the next post...")
            time.sleep(wait_time)

        except Exception as e:
            logging.error(f"Error posting question: {question}. Exception type: {type(e).__name__}, Error: {e}")
            subject = "Reddit Automation - Post Error"
            body = (
                f"Hello,\n\n"
                f"The following Reddit post encountered an error:\n\n"
                f"**Status:** Failed\n"
                f"**Question:** {question}\n"
                f"**Subreddit:** {subreddit_name}\n\n"
                f"**Error Details:**\n"
                f"Exception Type: {type(e).__name__}\n"
                f"Error Message: {e}\n\n"
                f"Best regards,\n"
                f"Your Reddit Automation Bot"
            )
            send_email(subject, body, "recipient_email@gmail.com")
            continue

if __name__ == "__main__":
    post_to_reddit()
