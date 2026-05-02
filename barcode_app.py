import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pyzbar.pyzbar import decode
import cv2

# Google Sheets credentials and setup
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('rikoparts-3daa342d1f57.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Scan Barcode')
sheet = spreadsheet.sheet1

# Barcode scanning function
def scan_barcode():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')
            cap.release()
            return barcode_data
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cv2.destroyAllWindows()

# Main function to update spreadsheet
def update_spreadsheet():
    barcode_value = scan_barcode()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = "Your Item Name"  # Replace with actual item name logic if needed
    
    # Update Google Spreadsheet
    sheet.append_row([barcode_value, timestamp, item_name])
    print(f"Barcode: {barcode_value} | Timestamp: {timestamp} | Item Name: {item_name} added to spreadsheet.")

if __name__ == "__main__":
    update_spreadsheet()
