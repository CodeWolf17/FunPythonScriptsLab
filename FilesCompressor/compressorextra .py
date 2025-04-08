import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog

# Path to Ghostscript (Update if needed)
GS_PATH = r"C:\Program Files\gs\gs10.05.0\bin\gswin64c.exe"

def select_pdfs():
    """Open file dialog to select multiple PDF files."""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    file_paths = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF Files", "*.pdf")])
    return file_paths

def compress_pdf(input_pdf, output_pdf):
    """Compress the PDF using Ghostscript with 'screen' quality."""
    if not os.path.exists(GS_PATH):
        print("Error: Ghostscript executable not found. Check GS_PATH.")
        return False

    command = [
        GS_PATH, "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/screen",
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={output_pdf}",
        input_pdf
    ]

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Compression failed for {input_pdf}")
        return False

def main():
    input_pdfs = select_pdfs()
    if not input_pdfs:
        print("No files selected. Exiting.")
        return
    
    # Create compressed folder if it doesn't exist
    compressed_folder = "compressed"
    os.makedirs(compressed_folder, exist_ok=True)

    for input_pdf in input_pdfs:
        filename = os.path.basename(input_pdf)
        output_pdf = os.path.join(compressed_folder, filename)

        print(f"\n📂 Processing: {filename}")
        original_size = os.path.getsize(input_pdf)
        print(f"Original size: {original_size / 1024:.2f} KB")

        # Compress file
        success = compress_pdf(input_pdf, output_pdf)
        
        if success and os.path.exists(output_pdf):
            compressed_size = os.path.getsize(output_pdf)
            print(f"➡️ Compressed size: {compressed_size / 1024:.2f} KB")
            
            # If the compressed file is larger, keep the original instead
            if compressed_size >= original_size:
                print("⚠️ Compressed file is larger, keeping the original file.")
                shutil.copy(input_pdf, output_pdf)
        else:
            print("⚠️ Compression failed, keeping the original file.")
            shutil.copy(input_pdf, output_pdf)
    
    print("🎉 Compression complete. Check the 'compressed' folder!")

if __name__ == "__main__":
    main()
