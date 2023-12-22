from flask import Flask, jsonify
import schedule
import time
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta


app = Flask(__name__)


def getcontext():
    credentials_dict = {
     "type": "service_account",
     "project_id": "oncalls-dev",
     "private_key_id": "b02f4d031c627ab1f225999a7e3eef972d740437",
     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCURaOKdwWZr0ax\na//zbufRBMy4ub+nL28meN6X05dXeuA6koQ0DZ51L1GPiLUmXooqfzV158JRahqR\n7INKsRMzlqOI7hnPe38gaVbHSXxGaaQUbpdHdItrgHO+p4FOFida5JvIBuA4BTLX\nkNjgySZIlJz8+YROpI+lA2qVwmkjSZgaQFLZ2IBOezrZ3U3hzweZcoXrxur4H8+f\nvA1T7Fheib1lWSnZGsbyBjJjMO9GSqg2XxhTJbXWoc6G4c5TZJ34xWKgYC609N59\nU69LrDlIPs6mnX5xKqCHE/AHHPYzyJrXz9H/LXpscAMU+A4BUmyr7NaNgL2wQBlj\n62nuJUAtAgMBAAECggEAFIcttMJ0xonTVkYXGit9Md2hwGOLKsjw8Rkj7E5Rsj1j\nZQibAB/wk9XYy3AIcIb/RxH0o13Sc/YmNpTRupoYh/hvrMoWTbkR6TlcV9wPNipz\nGpcTH8P9d4VBwSAs0VRU34suHDwDeA4UM28s77Y5tCvLLmUXUdILxzNZYuGXL9jP\nAuAbPwzmKSzsk1KXFFZJrGor3VbZD0Z3aMaCm7Om3+as8veh1dFNmJe04zm4+zQ6\naiTvXCVyb9iWQtlJ931zGm70q7zIvKos/SgfpzH1ptF8LafEoGspaadh6ByIOuJX\nG/V4Pal5ZciAeu6ta+cyVA9A3vqHmko6mFHhdX8KywKBgQDQI9fbRQkbTcZzjBIN\nxPATyRtuKkAvzJkCL++5kPdF7gTbWLyA7btd4MriogWBDBLd/LIy2QPDIqGaKZgO\naAtKopu6uAgQv0rrP79PHpXZWtvfUsg9mIWMxoN81OBYRNBu8p1RXdJd74qoPz91\n1UFeNLZcdMKm/Cd2S08CqyjE0wKBgQC2XasI4Q3wZ/sxlESWb4cUWl4cNqadp5jX\nFD7zMWwIyfEomCucnpkx999yfOqzpm1LZIlnLLgAhQ1Ok7nDvAWyTuyVbAU1+KD5\nSHePd8uDWzSp+TJsFDmHsFjTBn4eyhBAmJDUl26/HtGupX+0d/Hm1POclO3sW/0T\nQneXHbrG/wKBgF+r2hBjzyfJvCpoe/PwThoKGp2stgxCkyI6PoqhY8e0/G6Gfz8U\nB0fDh/5cUwNaNWHsQUy2C9CqHnXqIIaetHH+BG7zIGHyS9GOX7VSbbaW2PHx7zDA\n5sIqjU3X27c3Cke1JTK9WXDsJmPnjpfvCjjvKdOdp8txpAHv48VqPzcZAoGAMwF7\nxt37YhQTI8jObiz/YOftjoKSk2G+09kryiU2jDa/JpV5DTMmsd0cOA9MLbcMtpuF\n+r99L1gHYsTani5GgZqlfR1bT78cdtyX5B6jYzftQOUb/zKg7JycG1mjiMUHSqnh\nSDSamwXpq6lKUJWDqQZCpLba3NLVs79RZ4i/Js0CgYEAx94B3mim3nx36tk4pGvL\nIlBGO3VySY4dGatebhCX1YQ6kK0BCxCxc3oN0oH7UwnpG+hIZ4ztfI1apwVCiGCS\nd0ycWpiOXi+koPpfQlt/QBnE5PG/31Mh4sSvAQGEL+jaDiN9l/KHAIyuKTwW6Qmk\n/3FF5cICrHzgVA6Jd2zwmeI=\n-----END PRIVATE KEY-----\n",
     "client_email": "my-account@oncalls-dev.iam.gserviceaccount.com",
     "client_id": "107012579296443175636",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-account%40oncalls-dev.iam.gserviceaccount.com",
     "universe_domain": "googleapis.com"
    }


# Connect to Google Sheets using service account credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    gc = gspread.authorize(credentials)

# Now you can use gc to open a spreadsheet, etc.
    spreadsheet = gc.open_by_key("1BrQxNhXigEgf0o8QNkX7iX3ZODw3CjOhRBmHTJKWWOg")

# Select a specific worksheet (by title or index)
    worksheet = spreadsheet.get_worksheet(0)  # Replace with your worksheet title or index
    columns_to_read = ['Date', 'T1', 'T2'] 

    df = pd.DataFrame(worksheet.get_all_records(empty2zero=False), columns = columns_to_read)
    today = datetime.today()
    if today.weekday() == 1:
        target_date = today.strftime('%Y-%m-%d')
    else:
        days_since_last_tuesday = (today.weekday() - 1) % 7
    previous_tuesday = today - timedelta(days=days_since_last_tuesday)
    target_date = previous_tuesday.strftime('%Y-%m-%d')
    index_of_date = df['Date'].index[df['Date'] == target_date].tolist()

    if index_of_date:
        index = index_of_date[0]
    # Get the value in the 'People' column at the found index
        people_value1 = df.loc[index, 'T1']
        people_value2 = df.loc[index, 'T2']
        context = 'Oncalls devs for today are ' + people_value1 + '(L1), ' + people_value2 + '(L2)'
    else:
        context = 'Spreadsheet needs  to be updated'
    return context


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/run_script', methods=['POST'])
def run_script():
    context = getcontext()
    url = "https://api.flock.com/hooks/sendMessage/b1520c67-2f57-47e9-bb75-651c632dd78d"
    headers = {'Content-Type': 'application/json'}
    json_payload = {
        "text": context
    }
    response = requests.post(url, headers=headers, json=json_payload)
    return jsonify({'output': "success"}), 200


@app.route('/about')
def about():
    return 'About'