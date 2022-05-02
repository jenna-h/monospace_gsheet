These are scripts that you can use in order to make Google Sheets with the monospace font of your choice as the default font.

Choose the monospace font that you would like to use by entering its name in "primaryFontFamily" in sheet_style.json.

In order for these to work, you will have to download your credentials for the Google Sheets (and optionally the Google Drive) API. Please follow the **first two steps** of the [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) and, optionally, the [Google Drive API](https://developers.google.com/drive/api/v3/quickstart/python). You'll need the Google Drive API only if you want to be able make spreadsheets in specific folders--otherwise, the spreadsheets will just appear in the "root" of your Drive. Make sure that you move your credentials into the this folder.

After that, you will need to run sheets_quickstart.py (and optionally drive_quickstart.py).

I use these scripts through my terminal; I have shell functions in my ~/.zshrc as follows:
```
gsheet() {
  python3 /path/to/create_monospace.py "$@"
}

convert() {
  python3 /path/to/convert_to_monospace.py "$@"
}
```

I can then create new sheets in the following way:
```
gsheet "name of 1st sheet" "sheet 2" ... "sheet n" [-p https://link-to-google-drive-folder]
```
(The `-p` flag and the link to the parent Google Drive folder are optional.)

Converting sheets to Consolas styling works like this:
```
convert https://link-to-sheet-1 https://link-to-sheet-2 ...
```
