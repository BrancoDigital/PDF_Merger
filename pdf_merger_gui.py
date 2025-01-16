import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import sys
import os
from PyPDF2 import PdfReader, PdfWriter

class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("600x400")
        
        # File paths
        self.front_path = tk.StringVar()
        self.back_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.reverse_back = tk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Front PDF
        front_frame = ttk.LabelFrame(self.root, text="Front PDF", padding=10)
        front_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(front_frame, textvariable=self.front_path).pack(side="left", fill="x", expand=True)
        ttk.Button(front_frame, text="Browse", command=lambda: self.browse_file(self.front_path)).pack(side="right")
        
        # Back PDF
        back_frame = ttk.LabelFrame(self.root, text="Back PDF", padding=10)
        back_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(back_frame, textvariable=self.back_path).pack(side="left", fill="x", expand=True)
        ttk.Button(back_frame, text="Browse", command=lambda: self.browse_file(self.back_path)).pack(side="right")
        
        # Output PDF
        output_frame = ttk.LabelFrame(self.root, text="Output PDF", padding=10)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(output_frame, textvariable=self.output_path).pack(side="left", fill="x", expand=True)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).pack(side="right")
        
        # Options
        options_frame = ttk.LabelFrame(self.root, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Checkbutton(options_frame, text="Reverse back pages (for auto-feed scanners)", 
                       variable=self.reverse_back).pack(anchor="w")
        
        # Merge button
        ttk.Button(self.root, text="Merge PDFs", command=self.merge_pdfs).pack(pady=20)
        
        # Status
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def browse_file(self, path_var):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            path_var.set(filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.output_path.set(filename)

    def merge_pdfs(self):
        if not all([self.front_path.get(), self.back_path.get(), self.output_path.get()]):
            self.status_label.config(text="Please select all PDF files")
            return

        try:
            front_pdf = PdfReader(self.front_path.get())
            back_pdf = PdfReader(self.back_path.get())
            
            if len(front_pdf.pages) != len(back_pdf.pages):
                self.status_label.config(text="Error: Front and back PDFs must have the same number of pages")
                return
                
            output = PdfWriter()
            total_pages = len(front_pdf.pages)
            
            for front_index in range(total_pages):
                output.add_page(front_pdf.pages[front_index])
                
                if self.reverse_back.get():
                    back_index = total_pages - 1 - front_index
                else:
                    back_index = front_index
                    
                output.add_page(back_pdf.pages[back_index])
            
            with open(self.output_path.get(), 'wb') as output_file:
                output.write(output_file)
                
            self.status_label.config(text="PDF successfully merged!")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

def check_dependencies():
    try:
        import PyPDF2
    except ImportError:
        if sys.platform.startswith('win'):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "PyPDF2"])

def main():
    check_dependencies()
    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()