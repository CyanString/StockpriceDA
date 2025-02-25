import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


NAME = "stock_data"

# Set up credentials and access the Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_service_account.json", scope)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("Your Google Sheet Name").sheet1

# Fetch data into a Pandas DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Save the data as a CSV/XLS file
df.to_csv(f"{NAME}.csv", index=False)
df.to_excel(f"{NAME}.xlsx", index=False)

print("Data successfully saved!")
