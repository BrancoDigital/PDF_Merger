import tkinter as tk
from tkinter import filedialog, ttk

from merge_pdfs import merge_double_sided


class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("600x400")

        self.front_path = tk.StringVar()
        self.back_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.reverse_back = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        self._file_row("Front PDF", self.front_path, lambda: self.browse_file(self.front_path))
        self._file_row("Back PDF", self.back_path, lambda: self.browse_file(self.back_path))
        self._file_row("Output PDF", self.output_path, self.browse_output)

        options_frame = ttk.LabelFrame(self.root, text="Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=5)
        ttk.Checkbutton(
            options_frame,
            text="Reverse back pages (for auto-feed scanners)",
            variable=self.reverse_back,
        ).pack(anchor="w")

        ttk.Button(self.root, text="Merge PDFs", command=self.merge_pdfs).pack(pady=20)

        self.status_label = ttk.Label(self.root, text="", wraplength=560)
        self.status_label.pack(pady=10)

    def _file_row(self, title, path_var, command):
        frame = ttk.LabelFrame(self.root, text=title, padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame, textvariable=path_var).pack(side="left", fill="x", expand=True)
        ttk.Button(frame, text="Browse", command=command).pack(side="right")

    def browse_file(self, path_var):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            path_var.set(filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.output_path.set(filename)

    def merge_pdfs(self):
        if not all([self.front_path.get(), self.back_path.get(), self.output_path.get()]):
            self.status_label.config(text="Please select all PDF files")
            return

        try:
            merge_double_sided(
                self.front_path.get(),
                self.back_path.get(),
                self.output_path.get(),
                self.reverse_back.get(),
            )
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
            return

        self.status_label.config(text="PDF successfully merged!")


def main():
    root = tk.Tk()
    PDFMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
