
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'telegram-est-388a5ebb5583.json'
# Escribe aquí el ID de tu documento:
SPREADSHEET_ID = '1vL1qhwx-nqVW_yBxfWFnIvHkSqagWVBHD8JN9ulUs5w'

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Llamada a la api
# Función para imprimir datos desde la hoja de cálculo
async def imprimir_datos(update):
  result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!E1:E29').execute()
  # Extraemos valores del resultado
  values = result.get('values',[])
  print("ejecutado")

  if update.callback_query:
      await update.callback_query.answer()  # Responder al callback query

      if values:
         for row in values:
             for value in row:
                 # Eliminar corchetes, comas y comillas
                 cleaned_value = value.replace('[', '').replace(']', '').replace(',', '').replace("'", "")
                 await update.callback_query.message.reply_text(cleaned_value)
      else: 
         await update.callback_query.message.reply_text("No se encontraron datos en la hoja de cálculo.")
  else:
    if values:
      for row in values:
        for value in row:
                 # Eliminar corchetes, comas y comillas
                 cleaned_value = value.replace('[', '').replace(']', '').replace(',', '').replace("'", "")
        await update.message.reply_text(cleaned_value)

    else:
        await update.message.reply_text("No se encontraron datos en la hoja de cálculo.")

async def imprimir_datos1234(update):
  result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!F3:F13').execute()
  # Extraemos valores del resultado
  values = result.get('values',[])
  print(values)

  if update.callback_query:
      await update.callback_query.answer()  # Responder al callback query

      if values:
         for row in values:
             for value in row:
                 # Eliminar corchetes, comas y comillas
                 cleaned_value = value.replace('[', '').replace(']', '').replace(',', '').replace("'", "")
                 await update.callback_query.message.reply_text(cleaned_value)
      else:
         await update.callback_query.message.reply_text("No se encontraron datos en la hoja de cálculo.")
  else:
    if values:
      for row in values:
        for value in row:
                 # Eliminar corchetes, comas y comillas
                 cleaned_value = value.replace('[', '').replace(']', '').replace(',', '').replace("'", "")
        await update.message.reply_text(cleaned_value)

    else:
        await update.message.reply_text("No se encontraron datos en la hoja de cálculo.")