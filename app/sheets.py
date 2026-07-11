import gspread
from google.oauth2.service_account import Credentials
from app.config import GOOGLE_CREDENTIALS, SHEET_NAME

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS,
    scopes=SCOPES,
)

gc = gspread.authorize(creds)

def get_random_product():
    sheet = gc.open(SHEET_NAME).sheet1
    values = sheet.get_all_records()

    if not values:
        return None

    return values[0]