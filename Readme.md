# Reddit Question Poster Bot

A Python-based automation bot designed to streamline the process of posting dynamic, open-ended questions to the [r/AskReddit](https://www.reddit.com/r/AskReddit/) subreddit. This bot integrates seamlessly with Google Sheets for managing and updating questions, supports question validation, logging, email notifications, and error handling.

## Features

### 🔄 **Dynamic Question Management**
- Fetches questions directly from Google Sheets for easy updates.
- No need to rely on static local files, making it highly adaptable and up-to-date.

### ✅ **Question Validation**
- Automatically validates that only open-ended questions are posted.
- Invalid questions are skipped and marked in Google Sheets with an appropriate status and highlighted color for quick identification.

### 📬 **Posting to Reddit**
- Posts validated questions to the r/AskReddit subreddit.
- Tracks posted questions to prevent duplicates, ensuring each question is posted once.

### 📧 **Email Notifications**
- Receive email updates after every posting attempt, whether successful or failed.
- Includes essential post details such as timestamp, status, and direct URL to the post.

### 📊 **Logging**
- Logs every activity for troubleshooting, performance monitoring, and auditing purposes.

### 🗂 **Google Sheets Integration**
- Fetches questions directly from a Google Sheet.
- Updates Google Sheets with status and color-coded highlights (success, error, or duplicate).

### ⚠️ **Error Handling**
- Catches errors during the posting process and sends email notifications for each failure, ensuring no issues go unnoticed.

## Prerequisites

Before using this bot, ensure you have the following:

- Python 3.8 or higher
- Reddit API Credentials
- Google Cloud Service Account JSON file for Google Sheets integration
- SMTP server setup for email notifications

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<YourGitHubUsername>/reddit-question-poster.git
cd reddit-question-poster
2. Install Dependencies
Ensure all necessary libraries are installed by running the following command:

bash
Copy code
pip install -r requirements.txt
3. Set Up Credentials
Reddit API Credentials
Create a Reddit app at Reddit Apps and obtain your client_id, client_secret, username, password, and user_agent.
Add your Reddit credentials to config_2.py:
python
Copy code
REDDIT_CLIENT_ID = "<Your Client ID>"
REDDIT_SECRET = "<Your Secret>"
REDDIT_USERNAME = "<Your Username>"
REDDIT_PASSWORD = "<Your Password>"
USER_AGENT = "<Your User Agent>"
Google Sheets Credentials
Create a Google Cloud Service Account and download the JSON file for Google Sheets API access.
Place the Credentials.json file in the project root directory.
Ensure the Google Sheet is accessible by the service account.
4. Configure Google Sheets Integration
Create a Google Sheet with questions in the first column.
Update the SPREADSHEET_ID variable in question_checker.py with your Google Sheet ID.
5. Run the Script
Execute the script to start posting questions:

bash
Copy code
python Test-post.py
Usage
Populate the Google Sheet: Add questions to the first column of your Google Sheet.
Run the bot script: Execute the core script to begin posting questions to r/AskReddit.
Monitor the log file: Track activity and errors via the reddit_posting.log file.
Check your email: Receive notifications about the status of each post attempt.
File Structure
plaintext
Copy code
.
├── config_2.py              # Reddit API credentials and configuration
├── posted_questions.txt     # Records previously posted questions
├── question_checker.py      # Validates and processes questions
├── Test.py                  # Handles email notifications
├── Test-post.py             # Core automation script for posting to Reddit
├── Credentials.json         # Google Service Account credentials for Google Sheets
├── reddit_posting.log       # Log file for bot activity and errors
└── requirements.txt         # List of required Python dependencies
Future Enhancements
We are continuously improving this project. Upcoming features include:

Support for multiple subreddits: Easily expand the bot to post to multiple subreddits.
Advanced question validation: Implement NLP-based validation to ensure the best quality of questions.
Rate-limiting support: Incorporate features to comply with Reddit's rate-limiting rules.
GUI for management: A graphical interface for managing questions, viewing post status, and interacting with the bot.
Contributing
We welcome contributions to improve the Reddit Question Poster Bot. Feel free to fork the repository and submit pull requests with your changes. Please ensure your code adheres to the project's coding standards and includes relevant tests.

Steps to Contribute:
Fork this repository.
Create a new branch for your feature or fix.
Implement your changes.
Write tests (if applicable).
Submit a pull request with a clear description of your changes.
License
This project is licensed under the MIT License. See the LICENSE file for more details.