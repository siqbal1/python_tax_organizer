import os
import parser
import sheets_api as sheets

DEFAULT_STATEMENT_DIR = os.getcwd() + "/Bank_Statements"
print(DEFAULT_STATEMENT_DIR)

dir_path = DEFAULT_STATEMENT_DIR

year_summary = parser.parse_pdf_statements_from_directory(dir_path)
service = sheets.get_service()

spreadsheetJSON = year_summary.toSpreadsheetJSON()
spreadsheet = service.spreadsheets().create(
    body=spreadsheetJSON, fields='spreadsheetId').execute()

print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))

