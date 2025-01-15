# Reddit Question Poster Bot with Email Notifications

A Python-based automation bot designed to simplify the process of posting dynamic, open-ended questions to the r/AskReddit subreddit. This bot features email notifications, logging, and scheduling to enhance automation efficiency.

## Features

### 🔄 Dynamic Question Management
- Fetches questions directly from an Excel file (`questions.xlsx`) for easy updates.
- Avoids reliance on static local files, ensuring adaptability and freshness.

### ✅ Automatic Question Posting
- Posts open-ended questions to r/AskReddit.
- Prevents duplicate submissions by tracking previously posted questions.

### 📧 Email Notifications
- Sends email updates after every posting attempt, successful or failed.
- Provides essential details, including the timestamp, status, and post URL.

### 📊 Detailed Logging
- Logs all activities for troubleshooting, performance monitoring, and auditing.
- Logs are stored in a file named `automation.log`.

### ⏳ Scheduled Posting and Notifications
- Automates question posting at set intervals, with random delays for variability.
- Sends email notifications immediately after posting and then hourly updates.

### ⚠️ Robust Error Handling
- Captures errors during posting and sends email notifications to highlight failures.

## Prerequisites

Before using the bot, ensure you have the following:
- Python 3.8 or higher
- Reddit API credentials
- SMTP email server for notifications
- An Excel file (`questions.xlsx`) containing your questions

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Puneet2769/Reddit-Automation.git
   cd Reddit-Automation
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Credentials**
   - **Reddit API**: Create a Reddit app at [Reddit Apps](https://www.reddit.com/prefs/apps) and add the credentials to `config.py`:
     ```python
     REDDIT_CLIENT_ID = "<Your Client ID>"
     REDDIT_SECRET = "<Your Secret>"
     REDDIT_USERNAME = "<Your Username>"
     REDDIT_PASSWORD = "<Your Password>"
     USER_AGENT = "<Your User Agent>"
     ```
   - **Email Server**: Configure your SMTP details in the `send_email` function within `email_notification.py`.

4. **Prepare the Questions File**
   - Create an Excel file named `questions.xlsx` and add open-ended questions in the first column.

5. **Run the Script**
   ```bash
   python main.py
   ```

## Usage

1. **Populate the Excel File**
   - Add questions to the first column of `questions.xlsx`.

2. **Execute the Script**
   - Run the bot to start posting questions to r/AskReddit.

3. **Monitor Activity**
   - Check `automation.log` for detailed activity and error logs.

4. **Review Notifications**
   - Verify the status of each posting attempt via email updates.

## File Structure

```
.
├── config.py                # Reddit API credentials and configuration
├── posted_questions.txt     # Tracks previously posted questions
├── email_notification.py    # Handles email notifications
├── main.py                  # Core script for posting to Reddit and scheduling
├── automation.log           # Log file for activity and errors
├── questions.xlsx           # Excel file with questions for posting
└── requirements.txt         # List of dependencies
```

## Future Enhancements

- **Multi-Subreddit Support**: Expand the bot to post to multiple subreddits.
- **Enhanced Question Validation**: Implement NLP to ensure high-quality questions.
- **Rate-Limiting Compliance**: Add support for Reddit's rate-limiting rules.
- **GUI Management**: Introduce a graphical interface for easier interaction.

## Contributing

We welcome contributions to enhance this project. Follow these steps to contribute:
1. Fork this repository.
2. Create a new branch for your feature or fix.
3. Implement and test your changes.
4. Submit a pull request with a clear description.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

**Author**: Puneet Poddar

---

This revised version improves the structure and formatting of the README while maintaining its content. Let me know if there are specific areas you'd like adjusted further!