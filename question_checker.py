import re
import time
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'Credentials.json'
SPREADSHEET_ID = 'Your spread id, you will get from link of google sheet'

# Rule checks
def is_open_ended(question):
    return not re.search(r'\b(yes|no|either/or|would you rather|dae|poll)\b', question.lower())

def contains_personal_references(question):
    return bool(re.search(r'\b(my|mine|i|me|myself)\b', question.lower()))

def is_crowdsourcing(question):
    return bool(re.search(r'\b(suggest|recommend|help me choose|name)\b', question.lower()))

def is_requesting_advice(question):
    return bool(re.search(r'\b(medical|legal|financial|mental health|advice|help)\b', question.lower()))

def is_rhetorical_or_loaded(question):
    return bool(re.search(r'\b(always|never|clearly|obviously)\b', question.lower()))

# New checks for question patterns
def starts_with_special_word(question):
    return bool(re.match(r'^(do|is|can|would you rather|should|might|they)\b', question.lower()))

# Main validation function
def validate_question(question):
    errors = []

    if starts_with_special_word(question):
        errors.append("Starts with a restricted word (e.g., do, is, can, etc.).")
    if not is_open_ended(question):
        errors.append("Not open-ended.")
    if contains_personal_references(question):
        errors.append("Contains personal references.")
    if is_crowdsourcing(question):
        errors.append("Suggests crowdsourcing.")
    if is_requesting_advice(question):
        errors.append("Requests professional advice.")
    if is_rhetorical_or_loaded(question):
        errors.append("Rhetorical or loaded question.")

    return errors if errors else ["Valid question!"]

# Google Sheets integration
def get_sheet_service():
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=credentials)

def read_sheet(service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A2:A').execute()
    return result.get('values', [])

def update_sheet(service, updates, color_updates):
    body = {'values': updates}
    sheet = service.spreadsheets()

    # Update values in column B (status column)
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!B2:B',
        valueInputOption='RAW',
        body=body
    ).execute()

    # Apply color formatting only to the updated cells in columns A and B
    requests = []
    for (row, color) in color_updates:
        # Format the cell in column A (for the question)
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": row - 1,  # Adjust for zero-indexing
                    "endRowIndex": row,
                    "startColumnIndex": 0,  # Column A
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": color
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        })
        # Format the cell in column B (for the status)
        requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": row - 1,  # Adjust for zero-indexing
                    "endRowIndex": row,
                    "startColumnIndex": 1,  # Column B
                    "endColumnIndex": 2
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": color
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        })

    # Apply all the requests to update colors for columns A and B
    if requests:
        sheet.batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": requests}
        ).execute()

def process_questions():
    service = get_sheet_service()
    questions = read_sheet(service)

    if not questions:
        print("No questions found.")
        return

    updates = []
    color_updates = []

    for idx, question_row in enumerate(questions, start=2):  # Start from row 2
        if not question_row or not question_row[0].strip().endswith("?"):
            # Skip blank or invalid questions
            updates.append(["Skipped: Not a valid question."])
            color_updates.append((idx, {"red": 1, "green": 1, "blue": 0}))  # Yellow color for skipped
            continue

        question = question_row[0].strip()
        validation = ", ".join(validate_question(question))
        updates.append([validation])

        # Determine cell color based on validation result
        if validation == "Valid question!":
            color_updates.append((idx, {"red": 0.7, "green": 1, "blue": 0.7}))  # Light green for valid
        else:
            color_updates.append((idx, {"red": 1, "green": 0.7, "blue": 0.7}))  # Light red for errors

    update_sheet(service, updates, color_updates)

# Continuous monitoring
if __name__ == "__main__":
    while True:
        print("Checking for updates...")
        process_questions()
        time.sleep(20)  # Run every 20 seconds
