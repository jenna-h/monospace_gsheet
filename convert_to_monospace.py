import argparse
import json
import os.path
import pickle
from googleapiclient.discovery import build

# s.join with empty string ensures that there's a trailing slash
BASE_DIR = os.path.join(os.path.dirname(__file__), '')
SHEETS_TOKEN_PATH = BASE_DIR + 'sheets-token.pickle'
STYLE_PATH = BASE_DIR + 'sheet_style.json'

ID_PREFIX = '/spreadsheets/d/'

# set up the 'service'
if os.path.exists(SHEETS_TOKEN_PATH):
    with open(SHEETS_TOKEN_PATH, 'rb') as token:
        SHEETS_CREDS = pickle.load(token)
else:
    print('token not found--do setup again')

SERVICE = build('sheets', 'v4', credentials=SHEETS_CREDS)

def get_id_from_url(spreadsheet_url):
    url_suffix = spreadsheet_url.split(ID_PREFIX)[1] # chars after id prefix
    spreadsheet_id = url_suffix.split('/')[0] # chars before next /
    return spreadsheet_id

def convert(spreadsheet_id):
    # populate the spreadsheet style
    with open(STYLE_PATH) as style_file:
        style = json.load(style_file)
        
    # specify that we are updating the spreadsheet theme
    style['fields'] = 'spreadsheetTheme'
    
    requests = []

    requests.append({
        'updateSpreadsheetProperties': style,
    })

    body = {
        'requests': requests
    }
    
    response = SERVICE.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body).execute()

def convert_all(spreadsheet_urls):
    for url in spreadsheet_urls:
        convert(get_id_from_url(url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Make Consolas the default font for the supplied Google sheets')
    parser.add_argument('spreadsheet_urls', type=str, nargs='+',
                        help='the urls of the spreadsheets')
    args = parser.parse_args()
    convert_all(args.spreadsheet_urls)
