import os
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

def compress_pdf(input_pdf, output_pdf, quality="screen"):
    """Compress the PDF using Ghostscript."""
    if not os.path.exists(GS_PATH):
        print("Error: Ghostscript executable not found. Check GS_PATH.")
        return

    command = [
        GS_PATH, "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/" + quality,
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={output_pdf}",
        input_pdf
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✅ Compressed: {output_pdf}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Compression failed for {input_pdf}: {e}")

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
        print(f"Original size: {os.path.getsize(input_pdf) / 1024 / 1024:.2f} MB")

        # Try different compression levels
        for quality in ["prepress", "ebook", "screen"]:
            print(f"🔹 Trying compression level: {quality}...")
            compress_pdf(input_pdf, output_pdf, quality)

            # Check new size
            if os.path.exists(output_pdf):
                new_size = os.path.getsize(output_pdf) / 1024 / 1024
                print(f"➡️ Compressed size: {new_size:.2f} MB")

                # Stop if it's under 1MB
                if new_size < 1:
                    print("✅ Successfully compressed below 1MB!\n")
                    break
                else:
                    print("🔄 Trying a lower quality setting...\n")

    print("🎉 Compression complete. Check the 'compressed' folder!")

if __name__ == "__main__":
    main()
