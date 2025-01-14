import re
import time
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'P:\Coding\Google sheets api try/speedy-solstice-447806-j6-abfc08a86e04.json'
SPREADSHEET_ID = '1Q8gi__xytEM9EjUjB1hI5AN86YoOSbwBCIVC3ZBOWbo'

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

# Main validation function
def validate_question(question):
    errors = []

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

def update_sheet(service, updates):
    body = {'values': updates}
    sheet = service.spreadsheets()
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!B2:B',
        valueInputOption='RAW',
        body=body
    ).execute()

def process_questions():
    service = get_sheet_service()
    questions = read_sheet(service)

    if not questions:
        print("No questions found.")
        return

    updates = []
    for question_row in questions:
        question = question_row[0]
        validation = ", ".join(validate_question(question))
        updates.append([validation])

    update_sheet(service, updates)

# Continuous monitoring
if __name__ == "__main__":
    while True:
        print("Checking for updates...")
        process_questions()
        time.sleep(60)  # Run every 60 seconds
