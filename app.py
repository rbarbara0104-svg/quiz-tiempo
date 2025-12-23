from flask import Flask, render_template, request
import time
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# =============================
# GOOGLE SHEETS CONFIG
# =============================
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import os

CREDS_FILE = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS",
    "exalted-analogy-474301-m7-7b01604927b9.json"
)
SPREADSHEET_NAME = "Resultados Quiz"

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

# =============================
# CONFIG EXPERIMENTO
# =============================
TOTAL_QUESTIONS = 32
INTRO_TIME = 5
OPTIONS_TIME = 5

# =============================
# BALANCEO FIJO DE LAYOUTS
# =============================
layouts = (
    ["vertical_a"] * 8 +
    ["vertical_b"] * 8 +
    ["horizontal_a"] * 8 +
    ["horizontal_b"] * 8
)
random.shuffle(layouts)

SESSION_LAYOUTS = {
    i + 1: layouts[i] for i in range(TOTAL_QUESTIONS)
}

# =============================
# ROUTES
# =============================
@app.route("/")
def index():
    return render_template("quiz.html")

@app.route("/submit", methods=["POST"])
def submit():
    participant = request.form.get("participant_name")
    age = request.form.get("age_range")
    gender = request.form.get("gender")
    other_gender = request.form.get("other_gender", "")
    second_lang = request.form.get("second_language", "")
    question = int(request.form.get("question_number"))
    option = request.form.get("option") or "no"
    response_time = request.form.get("response_time")
    layout = SESSION_LAYOUTS.get(question)

    sheet.append_row([
        participant,
        age,
        gender,
        other_gender,
        second_lang,
        question,
        layout,
        option,
        response_time,
        time.strftime("%Y-%m-%d %H:%M:%S")
    ])

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
