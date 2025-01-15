import time
import random
import logging
from reddit_auth import authenticate
from email_notification import send_email
from datetime import datetime, timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.utils import rowcol_to_a1
import re


# Setup logging
logging.basicConfig(
    filename="reddit_posting.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Authenticate with Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('Credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Function to check for valid open-ended questions
def is_open_ended(question):
    return not re.search(r'\b(yes|no|either/or|would you rather|dae|poll)\b', question.lower())

# Validate question based on certain criteria
def validate_question(question):
    if not question.strip().endswith("?"):
        return False, "Not a valid question (missing '?')."
    if not is_open_ended(question):
        return False, "Not an open-ended question."
    return True, ""

def post_to_reddit():
    reddit = authenticate()
    subreddit_name = "AskReddit"
    subreddit = reddit.subreddit(subreddit_name)

    # Authenticate Google Sheets and get the data
    try:
        client = authenticate_google_sheets()
        sheet = client.open("Questions").sheet1  # Open the first sheet of the document
        questions = sheet.col_values(1)[1:]  # Skip the first row (header)
        questions = [q for q in questions if q]  # Remove any empty values
    except Exception as e:
        logging.error(f"Error: {e}")
        return

    posted_questions = set()
    try:
        with open("posted_questions.txt", "r") as file:
            posted_questions.update(file.read().splitlines())
    except FileNotFoundError:
        logging.info("No previous 'posted_questions.txt' found. Starting fresh.")

    for idx, question in enumerate(questions, start=2):  # Start from row 2
        if question in posted_questions:
            logging.info(f"Skipping already posted question: {question}")
            
            # Update Google Sheets with 'Already Posted' status in 3rd column and yellow color
            sheet.update_acell(rowcol_to_a1(idx, 3), 'Already Posted')  # Update the 3rd column (C)
            sheet.format(rowcol_to_a1(idx, 3), {"backgroundColor": {"red": 1, "green": 1, "blue": 0}})  # Yellow color
            continue
        
        valid, error_msg = validate_question(question)
        if not valid:
            logging.info(f"Skipping invalid question: {question}. Reason: {error_msg}")
            # Update Google Sheets with error status in 3rd column and red color
            sheet.update_acell(rowcol_to_a1(idx, 3), error_msg)  # Update with error reason
            sheet.format(rowcol_to_a1(idx, 3), {"backgroundColor": {"red": 1, "green": 0, "blue": 0}})  # Red color
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
                f"Best regards,\n"
                f"Your Reddit Automation Bot"
            )
            send_email(subject, body, "reciptent@gmail.com")

            # Save the posted question
            with open("posted_questions.txt", "a") as file:
                file.write(f"{question}\n")

            # Update Google Sheets with success status in 3rd column and green color
            sheet.update_acell(rowcol_to_a1(idx, 3), 'Success')  # Set status in 3rd column (C)
            sheet.format(rowcol_to_a1(idx, 3), {"backgroundColor": {"red": 0, "green": 1, "blue": 0}})  # Green color
            logging.info(f"Google Sheets updated with success for question: {question}")

            # Wait before the next post
            wait_time = random.randint(11, 13) * 3600  # Random wait between 11 and 13 hours
            logging.info(f"Waiting for {wait_time} seconds before the next post...")
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

            # Update Google Sheets with error status in 3rd column and red color
            sheet.update_acell(rowcol_to_a1(idx, 3), 'Error')  # Set status in 3rd column (C)
            sheet.format(rowcol_to_a1(idx, 3), {"backgroundColor": {"red": 1, "green": 0, "blue": 0}})  # Red color
            logging.info(f"Google Sheets updated with error for question: {question}")

            continue

# Infinite loop for continuous checking
if __name__ == "__main__":
    while True:
        logging.info("Checking for new questions...")
        post_to_reddit()
        time.sleep(120)  # Wait for 2 minutes before checking again
