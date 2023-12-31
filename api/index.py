import json
from flask import Flask, jsonify, request
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import logging

# Configure logging to output to the console
logging.basicConfig(level=logging.INFO)


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
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credentials_dict, scope)
    gc = gspread.authorize(credentials)

# Now you can use gc to open a spreadsheet, etc.
    spreadsheet = gc.open_by_key(
        "1BrQxNhXigEgf0o8QNkX7iX3ZODw3CjOhRBmHTJKWWOg")

# Select a specific worksheet (by title or index)
    # Replace with your worksheet title or index
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    if current_month == 'December':
        page = 0

    elif current_month == 'Feburary':
        page = 2
    elif current_month == 'January':
        page = 1
    elif current_month == 'March':
        page = 3
    else:
        context = ''
        return

# Filter DataFrame for rows with the current month and year in the 'Date' column
    print(current_month, current_year)
    worksheet = spreadsheet.get_worksheet(page)    
    columns_to_read = ['Date', 'L11', 'L12', 'L2']
    columns_to_read4 = ['Name', 'Email', 'Phone']
    df2 = pd.DataFrame(spreadsheet.get_worksheet(4).get_all_records(
        empty2zero=False), columns=columns_to_read4)
    df = pd.DataFrame(worksheet.get_all_records(
        empty2zero=False), columns=columns_to_read)    
    today = datetime.today()
    target_date = today.strftime('%d-%b')
    index_of_date = df['Date'].index[df['Date'] == target_date].tolist()

    if index_of_date:
        index = index_of_date[0] 
    # Get the value in the 'People' column at the found index
    #adding comments
        people_value1 = df.loc[index, 'L11']
        index_of_people_value1 = df2['Name'].index[df2['Name'] == people_value1].tolist()
        number_people1 = df2.loc[index_of_people_value1[0], 'Phone']
        email_people1 = df2.loc[index_of_people_value1[0], 'Email']        
        people_value3 = df.loc[index, 'L2']
        index_of_people_value3 = df2['Name'].index[df2['Name'] == people_value3].tolist()
        number_people3 = df2.loc[index_of_people_value3[0], 'Phone']
        email_people3 = df2.loc[index_of_people_value3[0], 'Email']
        if df.loc[index, 'L12'] == '':
            context = '<flockml> Oncalls devs for today are: <br>L1: <br><b>' + people_value1 + '</b><br> Email: ' + email_people1 + '<br>Contact No.: ' + str(number_people1) + '<br><br>L2: <br><b>' + people_value3 + '</b><br>Email: ' + email_people3 + '<br>Contact No.: ' + str(number_people3) + '</flockml>'
            print(context)
        else:
            people_value2 = df.loc[index, 'L12']
            index_of_people_value2 = df2['Name'].index[df2['Name'] == people_value2].tolist()
            number_people2 = df2.loc[index_of_people_value2[0], 'Phone']
            email_people2 = df2.loc[index_of_people_value2[0], 'Email']
            context = '<flockml> Oncalls devs for today are: <br>L1: <br><b>' + people_value1 + '</b><br> Email: ' + email_people1 + '<br>Contact No.: ' + str(number_people1) + '<br><b>' + people_value2 + '</b><br>Email: ' + email_people2 + '<br>Contact No.: ' + str(number_people2) + '<br><br>L2: <br><b>' + people_value3 + '</b><br>Email: ' + email_people3 + '<br>Contact No. :' + str(number_people3) + '</flockml>'
    else:
        context = 'Spreadsheet needs  to be updated'
    return context


def hit_curl():
    logging.info("Function execution started")
    context = getcontext()
    url = "https://api.flock.com/hooks/sendMessage/b1520c67-2f57-47e9-bb75-651c632dd78d"
    headers = {'Content-Type': 'application/json'}
    json_payload = {
        "flockml": context
    }
    response = requests.post(url, headers=headers, json=json_payload)
    logging.info("Function execution completed")
    return response.send({"message": "Success"})


app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/cron')
def cron_trigger():
    hit_curl()


@app.route('/run_script', methods=['POST'])
def run_script():
    if request.is_json:
        # Get the JSON data from the payload
        payload_data = request.get_json()

        # Access 'token' and 'text' values from the payload
        text_value = payload_data.get('text', None)
        if text_value == '#oncall/cart':
            context = getcontext()
            url = "https://api.flock.com/hooks/sendMessage/b1520c67-2f57-47e9-bb75-651c632dd78d"
            headers = {'Content-Type': 'application/json'}
            json_payload = {
                "text": context
            }
            response = requests.post(url, headers=headers, json=json_payload)
            return jsonify({'output': "SUCCESS"}), 200
   
    return jsonify({'output': "failure"}), 200


@app.route('/about')
def about():
    return 'About your page'
