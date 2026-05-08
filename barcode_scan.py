import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
# HAPUS BARIS INI: from pyzbar.pyzbar import decode 
import cv2

# Google Sheets credentials and setup
# Tambahkan scope Google Drive agar gspread bisa mencari file berdasarkan nama
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Pastikan nama file JSON ini sesuai dengan yang ada di folder Anda
creds = ServiceAccountCredentials.from_json_keyfile_name('gen-lang-client-0529165208-75bf2bc4b4d7.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Scan Barcode')
sheet = spreadsheet.sheet1

# Barcode scanning function menggunakan OpenCV (Lebih stabil di Windows)
def scan_barcode():
    # Coba indeks 0, jika tetap error 'index out of range', ganti angka 0 menjadi 1
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    
    if not cap.isOpened():
        print("Error: Kamera tidak ditemukan atau sedang digunakan aplikasi lain.")
        return None

    # QRCodeDetector lebih stabil di banyak versi OpenCV
    detector = cv2.QRCodeDetector()
    
    print("Kamera terbuka. Arahkan kode ke kamera. Tekan 'q' untuk keluar.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal mengambil gambar dari kamera.")
            break

        # Deteksi sederhana
        data, bbox, _ = detector.detectAndDecode(frame)
        
        if data:
            cap.release()
            cv2.destroyAllWindows()
            return data
            
        cv2.imshow("Barcode Scanner - Tekan 'q' untuk batal", frame)
        if cv2.waitKey(1) == ord("q"):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return None

# Main function to update spreadsheet
def update_spreadsheet():
    barcode_value = scan_barcode()
    
    if barcode_value:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item_name = "Your Item Name"  
        
        # Update Google Spreadsheet
        sheet.append_row([barcode_value, timestamp, item_name])
        print(f"Berhasil! Barcode: {barcode_value} ditambahkan ke spreadsheet.")
    else:
        print("Scan dibatalkan.")

if __name__ == "__main__":
    update_spreadsheet()