import tkinter as tk
from tkinter import filedialog, messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import cv2
import os
import zxingcpp 

# --- KONFIGURASI GOOGLE SHEETS ---
def setup_gspread():
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    json_file = 'gen-lang-client-0529165208-75bf2bc4b4d7.json'
    
    if not os.path.exists(json_file):
        messagebox.showerror("Error", f"File kredensial {json_file} tidak ditemukan!")
        return None

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open('Scan Barcode')
        return spreadsheet.sheet1
    except Exception as e:
        messagebox.showerror("Error Koneksi", f"Gagal terhubung ke Google Sheets: {e}")
        return None

sheet = setup_gspread()

# --- LOGIKA PEMROSESAN BARCODE ---
def scan_barcode_from_file(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    try:
        results = zxingcpp.read_barcodes(image)
        if results:
            return results[0].text
    except Exception as e:
        print(f"Error ZXing: {e}")
    return None

def update_inventory(barcode_data, nama_barang_input):
    try:
        # Mengambil semua data untuk menentukan posisi
        all_data = sheet.get_all_values()
        
        # Jika sheet kosong, col_barcode akan jadi list kosong
        if not all_data:
            col_barcode = []
        else:
            col_barcode = [row[0] for row in all_data] 
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if barcode_data in col_barcode:
            row_index = col_barcode.index(barcode_data) + 1
            
            # Ambil nilai Qty di Kolom D (Indeks ke-3 di list)
            # Gunakan penanganan error jika baris tersebut lebih pendek dari 4 kolom
            try:
                current_qty_val = all_data[row_index-1][3]
                current_qty = int(current_qty_val) if current_qty_val else 0
            except IndexError:
                current_qty = 0
            
            new_qty = current_qty + 1
            
            # Update spesifik ke kolomnya:
            sheet.update_cell(row_index, 2, timestamp) # Kolom B (Waktu)
            sheet.update_cell(row_index, 4, new_qty)  # Kolom D (Qty)
            
            return f"Stok Berhasil Ditambah: {new_qty}"
        else:
            # MEMBUAT BARIS BARU: [A, B, C, D]
            # Pastikan ini adalah sebuah list dengan 4 elemen
            new_row = [barcode_data, timestamp, nama_barang_input, 1]
            sheet.append_row(new_row) 
            return f"Barang Baru Berhasil Didaftarkan"
            
    except Exception as e:
        raise e

def process_upload():
    # 1. Pilih Gambar
    file_path = filedialog.askopenfilename(
        title="Pilih Gambar Barcode",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    if file_path:
        lbl_status.config(text="Memindai Barcode...", fg="blue")
        root.update()
        
        barcode_data = scan_barcode_from_file(file_path)
        
        if barcode_data:
            lbl_status.config(text="Mengecek Database...", fg="blue")
            root.update()
            
            try:
                all_data = sheet.get_all_values()
                col_barcode = [row[0] for row in all_data]
                
                # FITUR AUTO-FILL NAMA
                if barcode_data in col_barcode:
                    row_index = col_barcode.index(barcode_data)
                    existing_name = all_data[row_index][2]
                    
                    # Update input box secara otomatis
                    entry_nama.delete(0, tk.END)
                    entry_nama.insert(0, existing_name)
                    lbl_status.config(text=f"Barcode Terdeteksi: {barcode_data}\nNama otomatis terisi.", fg="black")
                else:
                    lbl_status.config(text=f"Barcode Baru: {barcode_data}\nSilakan isi Nama Barang.", fg="orange")
                    entry_nama.delete(0, tk.END)
                    entry_nama.insert(0, "Laptop Asus")
                
                # 2. Konfirmasi apakah ingin langsung update stok
                if messagebox.askyesno("Konfirmasi", f"Barcode: {barcode_data}\nUpdate stok sekarang?"):
                    nama_barang = entry_nama.get().strip()
                    pesan_sukses = update_inventory(barcode_data, nama_barang)
                    lbl_status.config(text=f"BERHASIL!\n{pesan_sukses}", fg="green")
            
            except Exception as e:
                lbl_status.config(text=f"Error Database: {e}", fg="red")
        else:
            lbl_status.config(text="TIDAK TERDETEKSI.\nGunakan gambar yang lebih jelas.", fg="red")

# --- UI SETUP ---
root = tk.Tk()
root.title("RIKO Parts - Smart Inventory")
root.geometry("450x450")
root.configure(padx=20, pady=20)

tk.Label(root, text="Sistem Stok Barcode Cloud", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Nama Barang (Otomatis jika data ada):").pack(anchor="w")
entry_nama = tk.Entry(root, font=("Arial", 12), width=40)
entry_nama.pack(pady=5)

tk.Label(root, text="Klik untuk Pilih & Scan:", pady=10).pack(anchor="w")
btn_scan = tk.Button(root, text="PILIH GAMBAR BARCODE", command=process_upload, 
                     bg="#0078d4", fg="white", font=("Arial", 10, "bold"), 
                     padx=20, pady=15, cursor="hand2")
btn_scan.pack(pady=10)

lbl_status = tk.Label(root, text="Siap melakukan sinkronisasi stok...", font=("Arial", 10), wraplength=380, pady=10)
lbl_status.pack(pady=20)

if sheet:
    root.mainloop()