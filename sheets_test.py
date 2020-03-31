import gspread
from oauth2client.service_account import ServiceAccountCredentials

# http://www.indjango.com/access-google-sheets-in-python-using-gspread/

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
# sheet = client.open("חמל קורונה").worksheet("תגובות לטופס 1")
# sheet = client.open("python_course").worksheet("Form responses 1")
sheet = client.open("python_course").sheet1

# Extract and print all of the values
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

# sheet.update_acell('A10', "I just wrote to a spreadsheet using Python!")

# values_list = sheet.col_values(1)
# print(values_list)
# index = None
# for i in values_list:
#     if i == '4':
#         index = values_list.index(i)
# sheet.update_acell('O'+str(index+1), "טופל")
import time
for i in range(50):
    sheet.update_acell('X'+str(i+1), "טופל")
    time.sleep(1)