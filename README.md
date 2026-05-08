# 📦 Cloud-Integrated Barcode Inventory System

<p align="left">
  <img src="/assets/generator_barcode" />
  <img src="/assets/barcode_saved" />
  <img src="/assets/sheet_header" />
  <img src="/assets/barcode_scan" />
  <img src="/assets/barcode_detected" />
  <img src="/assets/barcode_scanned" />
</p>

## 📝 Project Overview
Sistem manajemen inventaris mandiri yang dikembangkan untuk mendigitalisasi pencatatan stok secara *real-time*. Aplikasi ini mengintegrasikan pengenalan gambar (Computer Vision) dengan database berbasis cloud menggunakan Google Sheets API. Pengguna dapat menghasilkan barcode unik untuk barang baru dan memproses pemindaian stok masuk hanya dengan mengunggah gambar.

Sistem ini dirancang untuk efisiensi operasional dengan logika otomatisasi yang mencegah duplikasi data dan mempercepat proses *input* barang secara digital.

---

## 🛠️ Technical Stack
* **Core Language:** Python 3.12
* **Computer Vision:** `OpenCV` & `ZXing-CPP` (High-stability barcode detection)
* **Cloud Integration:** `GSpread` (Google Sheets API wrapper) & `OAuth2Client`
* **Interface:** `Tkinter` (GUI Framework)
* **Utility:** `Python-Barcode` (Standard Code128 generator)

---

## 🚀 Key Features
* **🏭 Barcode Generator:** Menghasilkan barcode standar Code128 yang siap cetak berdasarkan ID unik barang.
* **🔍 Intelligent Scanning:** Mendeteksi barcode dari file gambar dengan toleransi kejernihan yang baik menggunakan engine ZXing.
* **☁️ Cloud Database Sync:** Menggunakan Google Sheets sebagai database utama, memungkinkan akses data dari mana saja tanpa server tambahan.
* **📊 Smart Inventory Logic:** * **Auto-Recognition:** Jika barcode sudah ada di database, sistem otomatis menampilkan nama barang.
    * **Auto-Increment:** Menambah jumlah stok (+1) secara otomatis pada baris yang sama jika barang di-scan ulang.
    * **New Entry:** Otomatis membuat baris baru jika barcode belum pernah terdaftar.

---

## 📸 App Preview

<table border="0">
  <tr>
    <td align="center">
      <img src="/barcode/barcode_1001.png" width="200" alt="Generated Barcode"/><br/>
      <sub><b>Generated Barcode (ID: 1001)</b></sub>
    </td>
    <td align="center">
      <img src="/barcode/barcode_Laptop_Asus.png" width="200" alt="Scanner Recognition"/><br/>
      <sub><b>Barcode Recognition Test</b></sub>
    </td>
  </tr>
</table>

---

## ⚙️ Implementation Steps

### 1. Google Cloud Configuration
1.  Buka [Google Cloud Console](https://console.cloud.google.com/).
2.  Aktifkan **Google Sheets API** dan **Google Drive API**.
3.  Buka menu **Credentials** > **Create Credentials** > **Service Account**.
4.  Buat Key dalam format **JSON**, unduh, dan simpan sebagai `credentials.json` di folder proyek.
5.  Salin email Service Account tersebut, lalu buka Google Sheets Anda dan klik **Share**, masukkan email tadi sebagai **Editor**.

### 2. Spreadsheet Structure
Pastikan baris pertama (Header) pada Google Sheets Anda diatur manual seperti berikut:
| Barcode Value (A) | Last Update (B) | Item Name (C) | Qty (D) |
| :--- | :--- | :--- | :--- |

### 3. Installation
Instal library yang diperlukan melalui terminal:
```bash
pip install gspread oauth2client opencv-python zxing-cpp python-barcode
