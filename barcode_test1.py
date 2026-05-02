import tkinter as tk
from tkinter import filedialog
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import openpyxl
from datetime import datetime
import cv2

# Function to scan the barcode
def scan_barcode(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    if decoded_objects:
        for obj in decoded_objects:
            return obj.data.decode('utf-8')
    return None

# Function to save data to Excel
def save_to_excel(data):
    try:
        workbook = openpyxl.load_workbook('barcode_data.xlsx')
        sheet = workbook.active
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Timestamp", "Item Name"])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append([timestamp, data])
    workbook.save('barcode_data.xlsx')

# Function to open file dialog and scan barcode
def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        barcode_data = scan_barcode(file_path)
        if barcode_data:
            save_to_excel(barcode_data)
            result_label.config(text=f"Barcode Data: {barcode_data}")
        else:
            result_label.config(text="No barcode found")

# Create the main window
root = tk.Tk()
root.title("Barcode Scanner")

# Create and place the widgets
scan_button = tk.Button(root, text="Scan Barcode", command=open_file_dialog)
scan_button.pack(pady=20)

result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# Run the application
root.mainloop()
