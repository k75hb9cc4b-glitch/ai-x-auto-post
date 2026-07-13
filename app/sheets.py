import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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


def get_sheet():
    return gc.open(SHEET_NAME).sheet1


def get_random_product():

    sheet = get_sheet()

    values = sheet.get_all_records()

    for i, row in enumerate(values, start=2):

        if str(row.get("投稿済み", "")).strip():
            continue

        row["_row"] = i

        return row

    return None


def mark_posted(row):

    sheet = get_sheet()

    sheet.update(f"I{row}", [["TRUE"]])

    sheet.update(
        f"J{row}",
        [[datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
    )
