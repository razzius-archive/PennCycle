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

  client = gdata.spreadsheet.service.SpreadsheetsService()
  client.email = email
  client.password = password
  client.source = 'app.penncycle.org'
  client.ProgrammaticLogin()

  # Prepare the dictionary to write
  d = {}
  d['timestamp'] = time.strftime('%m/%d/%Y %H:%M:%S')
  d['name'] = name
  d['penncard'] = penncard
  d['two'] = last_two
  d['type'] = type
  d['paid'] = '---'
  print d

  entry = client.InsertRow(d, spreadsheet_key, worksheet_id)
  if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    print "Insert row succeeded."
    return "Insert row succeeded."
  else:
    print "Insert row failed."
    return "Insert row failed."
    
    
def recordRide(ride):
  email = 'messenger@penncycle.org'
  password = 'penncycle'

  # Find this value in the url with 'key=XXX' and copy XXX below
  spreadsheet_key = '0AkVzE4zNIXVEdHJSUXN2ZGhrd3IyMmhVcndEc21femc'
  # All spreadsheets have worksheets. I think worksheet #1 by default always
  # has a value of 'od6'
  worksheet_id = 'od6'

  client = gdata.spreadsheet.service.SpreadsheetsService()
  client.email = email
  client.password = password
  client.source = 'app.penncycle.org'
  client.ProgrammaticLogin()

  # Prepare the dictionary to write
  d = {}
  d['outs'] = str(ride.checkout_time)
  d['ins'] = str(ride.checkin_time)
  d['users'] = str(ride.num_users)
  print d

  entry = client.InsertRow(d, spreadsheet_key, worksheet_id)
  if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    print "Insert row succeeded."
    return "Insert row succeeded."
  else:
    print "Insert row failed."
    return "Insert row failed."