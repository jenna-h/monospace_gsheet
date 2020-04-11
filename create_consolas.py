import argparse
import json
import os.path
import pickle
from googleapiclient.discovery import build

# s.join with empty string ensures that there's a trailing slash
BASE_DIR = os.path.join(os.path.dirname(__file__), '')
DRIVE_TOKEN_PATH = BASE_DIR + 'drive-token.pickle'
SHEETS_TOKEN_PATH = BASE_DIR + 'sheets-token.pickle'
STYLE_PATH = BASE_DIR + 'sheet_style.json'

SPREADSHEET_LINK_FORMAT = 'https://docs.google.com/spreadsheets/d/{}/edit#gid=0'
DRIVE_ID_PREFIX = 'drive/folders/'

def set_up_sheets_service():
    global SHEETS_SERVICE
    if os.path.exists(SHEETS_TOKEN_PATH):
        with open(SHEETS_TOKEN_PATH, 'rb') as token:
            sheets_creds = pickle.load(token)
    else:
        print('sheets token not found--do setup again')

    SHEETS_SERVICE = build('sheets', 'v4', credentials=sheets_creds)

def set_up_drive_service():
    global DRIVE_SERVICE
    if os.path.exists('drive-token.pickle'):
        with open('drive-token.pickle', 'rb') as token:
            drive_creds = pickle.load(token)
    else:
        print('drive token not found--do setup again')

    DRIVE_SERVICE = build('drive', 'v3', credentials=drive_creds)


def move(file_id, folder_id):
    # Retrieve the existing parents to remove
    file = DRIVE_SERVICE.files().get(fileId=file_id,
                                     fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    # Move the file to the new folder
    file = DRIVE_SERVICE.files().update(fileId=file_id,
                                        addParents=folder_id,
                                        removeParents=previous_parents,
                                        fields='id, parents').execute()

def get_folder_id_from_url(folder_url):
    url_suffix = folder_url.split(DRIVE_ID_PREFIX)[1] # chars after drive_id prefix
    return url_suffix.split('/')[0] # chars before next slash


def create(title):
    with open(STYLE_PATH) as style_file:
        spreadsheet = json.load(style_file) # populate style information
    spreadsheet['properties']['title'] = title # add the title
    spreadsheet = SHEETS_SERVICE.spreadsheets().create(body=spreadsheet,
                                    fields='spreadsheetId').execute()
    return spreadsheet.get('spreadsheetId')

def create_multiple(titles, parent):
    # set up sheets service, and drive service if necessary
    set_up_sheets_service()
    if parent:
        set_up_drive_service()

    for title in titles:
        spreadsheet_id = create(title)
        print('{}: {}'.format(title, SPREADSHEET_LINK_FORMAT.format(spreadsheet_id)), end='\n\n')
        if parent:
            move(spreadsheet_id, get_folder_id_from_url(parent))

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Make Google sheets with Consolas as their default font')
    parser.add_argument('titles', type=str, nargs='+',
                        help='the titles of the new spreadsheets')
    parser.add_argument('-p', '--parent',
                        help='the url of the parent folder',
                        nargs='?', default=None)
    args = parser.parse_args()
    create_multiple(args.titles, args.parent)
