<<<<<<< Updated upstream
=======
Here is a README for the main branch of your repository, without the "Test Feature," but incorporating the core functionality as seen in your code:

```markdown
# Reddit Question Poster Bot with Email Notifications

A Python-based automation bot designed to streamline the process of posting dynamic, open-ended questions to the r/AskReddit subreddit. This bot integrates email notifications, logging, and scheduling features. It automatically fetches questions from an Excel file, posts them to Reddit, and sends email updates on successful and failed attempts.

## Features

- **🔄 Dynamic Question Management**
  - Fetches questions directly from an Excel file (`questions.xlsx`) for easy updates.
  - No need to rely on static local files, making it highly adaptable and up-to-date.

- **✅ Question Posting to Reddit**
  - Automatically posts open-ended questions to the r/AskReddit subreddit.
  - Tracks previously posted questions to prevent duplicates.

- **📧 Email Notifications**
  - Sends email updates after every posting attempt, whether successful or failed.
  - Includes essential post details such as timestamp, status, and direct URL to the post.

- **📊 Logging**
  - Logs every activity for troubleshooting, performance monitoring, and auditing purposes.
  - All activities are logged to a file (`automation.log`).

- **⏳ Posting and Email Scheduling**
  - Posts questions on Reddit at scheduled intervals, with a random wait time between posts.
  - Email notifications are sent initially and then every hour thereafter.

- **⚠️ Error Handling**
  - Catches errors during the posting process and sends email notifications for each failure, ensuring no issues go unnoticed.

## Prerequisites

Before using this bot, ensure you have the following:

- Python 3.8 or higher
- Reddit API Credentials
- Email server setup for email notifications
- Excel file (`questions.xlsx`) containing open-ended questions

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Puneet2769/Reddit-Automation.git
   cd Reddit-Automation
   ```

2. **Install Dependencies:**
   Ensure all necessary libraries are installed by running the following command:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Credentials:**

   - **Reddit API Credentials:**
     - Create a Reddit app at [Reddit Apps](https://www.reddit.com/prefs/apps) and obtain your client_id, client_secret, username, password, and user_agent.
     - Add your Reddit credentials to `config.py`:
     ```python
     REDDIT_CLIENT_ID = "<Your Client ID>"
     REDDIT_SECRET = "<Your Secret>"
     REDDIT_USERNAME = "<Your Username>"
     REDDIT_PASSWORD = "<Your Password>"
     USER_AGENT = "<Your User Agent>"
     ```

   - **Email Setup:**
     - Ensure you have an SMTP server configured for sending emails. The `email_notification.py` module uses this to send the emails.
     - Update the `send_email` function with your SMTP server details.

4. **Prepare the Questions File:**
   - Create an Excel file named `questions.xlsx` and add open-ended questions to the first column.

5. **Run the Script:**
   Execute the script to start posting questions and sending email notifications:
   ```bash
   python main.py
   ```

## Usage

1. **Populate the Excel File:**
   - Add open-ended questions to the first column of `questions.xlsx`.

2. **Run the bot script:**
   - Execute the core script to begin posting questions to r/AskReddit.

3. **Monitor the log file:**
   - Track activity and errors via the `automation.log` file.

4. **Check your email:**
   - Receive notifications about the status of each post attempt.

## File Structure

```
.
├── config.py                # Reddit API credentials and configuration
├── posted_questions.txt     # Records previously posted questions
├── email_notification.py    # Handles email notifications
├── main.py                  # Core script for posting to Reddit and scheduling
├── automation.log           # Log file for bot activity and errors
├── questions.xlsx           # Excel file containing questions to be posted
└── requirements.txt         # List of required Python dependencies
```

## Future Enhancements

We are continuously improving this project. Upcoming features include:

- **Support for multiple subreddits:** Easily expand the bot to post to multiple subreddits.
- **Advanced question validation:** Implement NLP-based validation to ensure the best quality of questions.
- **Rate-limiting support:** Incorporate features to comply with Reddit's rate-limiting rules.
- **GUI for management:** A graphical interface for managing questions, viewing post status, and interacting with the bot.

## Contributing

We welcome contributions to improve the Reddit Question Poster Bot. Feel free to fork the repository and submit pull requests with your changes. Please ensure your code adheres to the project's coding standards and includes relevant tests.

### Steps to Contribute:
1. Fork this repository.
2. Create a new branch for your feature or fix.
3. Implement your changes.
4. Write tests (if applicable).
5. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

**Author:** Puneet Poddar
```

### Summary:
- This README reflects the main features of your code that automate posting on Reddit, email notifications, logging, and scheduling.
- It does not reference any test features, focusing on the core functionality of the Reddit automation bot.
  
Let me know if you'd like any further changes or clarifications!
>>>>>>> Stashed changes
