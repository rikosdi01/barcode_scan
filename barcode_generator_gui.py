import tkinter as tk
from tkinter import messagebox
import barcode
from barcode.writer import ImageWriter
import os

def generate_barcode():
    text_content = entry_text.get().strip()
    
    if not text_content:
        messagebox.showwarning("Peringatan", "Masukkan teks atau kode terlebih dahulu!")
        return

    try:
        # 1. Tentukan nama folder 'barcode' di root proyek
        folder_name = "barcode"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        # 2. Sanitasi nama file (mengganti spasi dengan underscore)
        sanitized_text = text_content.replace(' ', '_')
        file_name = f"barcode_{sanitized_text}"
        full_path = os.path.join(folder_name, file_name)
        
        # 3. Gunakan 'code128' agar bisa memuat teks dan angka
        # Format ini lebih mudah dibaca oleh library scanner dibanding EAN
        barcode_class = barcode.get_barcode_class('code128')
        
        # Inisialisasi barcode dengan writer untuk menghasilkan gambar (PNG)
        my_barcode = barcode_class(text_content, writer=ImageWriter())
        
        # 4. Simpan ke folder yang ditentukan
        # Library python-barcode otomatis menambahkan ekstensi .png
        save_path = my_barcode.save(full_path)
        
        messagebox.showinfo("Sukses", f"Barcode berhasil dibuat!\n\nSimpan di: {save_path}")
        entry_text.delete(0, tk.END) # Bersihkan input
        
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuat barcode: {e}")

# --- UI SETUP ---
root = tk.Tk()
root.title("RIKO Parts - Barcode Generator")
root.geometry("400x350")
root.configure(padx=20, pady=20)

# Header
tk.Label(root, text="Alat Pembuat Barcode", font=("Arial", 14, "bold")).pack(pady=10)

# Input Field
tk.Label(root, text="Masukkan Nama Barang / Kode:").pack(anchor="w")
entry_text = tk.Entry(root, font=("Arial", 12), width=35)
entry_text.pack(pady=10)
entry_text.focus_set()

# Penjelasan Teknis
info_text = (
    "Tips:\n"
    "- Gunakan nama yang unik.\n"
    "- Barcode akan disimpan otomatis ke folder 'barcode'.\n"
    "- Format: Code128 (Mendukung Huruf & Angka)."
)
tk.Label(root, text=info_text, fg="gray", font=("Arial", 9), justify="left").pack(pady=10, anchor="w")

# Tombol Generate
btn_generate = tk.Button(
    root, 
    text="GENERATE & SIMPAN", 
    command=generate_barcode,
    bg="#28a745", 
    fg="white", 
    font=("Arial", 10, "bold"),
    padx=20, 
    pady=15,
    cursor="hand2"
)
btn_generate.pack(pady=20)

root.mainloop()