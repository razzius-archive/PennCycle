import time
import gdata.spreadsheet.service

def addPerson(name, penncard, last_two, type):
  email = 'messenger@penncycle.org'
  password = 'penncycle'

  # Find this value in the url with 'key=XXX' and copy XXX below
  spreadsheet_key = '0AgV6RMJ1U0h6dEdma3ZCdzEtc0N0cXAtT2NNTi16bFE'
  # All spreadsheets have worksheets. I think worksheet #1 by default always
  # has a value of 'od6'
  worksheet_id = 'od6'

  spr_client = gdata.spreadsheet.service.SpreadsheetsService()
  spr_client.email = email
  spr_client.password = password
  spr_client.source = 'app.penncycle.org'
  spr_client.ProgrammaticLogin()

  # Prepare the dictionary to write
  d = {}
  d['timestamp'] = time.strftime('%m/%d/%Y %H:%M:%S')
  d['name'] = name
  d['penncard'] = penncard
  d['two'] = last_two
  d['type'] = type
  d['paid'] = '---'
  print d

  entry = spr_client.InsertRow(d, spreadsheet_key, worksheet_id)
  if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    print "Insert row succeeded."
    return "Insert row succeeded."
  else:
    print "Insert row failed."
    return "Insert row failed."
