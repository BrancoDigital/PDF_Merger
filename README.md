# PDF Merger

PDF Merger makes one double-sided PDF from two single-sided scans. You scan all the front sides into one PDF and all the back sides into a second PDF. The tool puts the pages in order: front 1, back 1, front 2, back 2, and so on.

An auto-feed scanner gives the back sides in reverse order (last page first). The tool reverses the back sides by default. If you scanned the back sides by hand in the same order as the front sides, turn this off.

Both PDFs must have the same number of pages.

## Use the macOS app

1. Download `pdf-merger-macos.zip` from the [Releases page](https://github.com/BrancoDigital/PDF_Merger/releases).
2. Unzip the file and open `PDF Merger.app`.
3. If macOS blocks the app, right-click it and select Open. The app is not signed.
4. Select the front PDF, the back PDF, and the output file.
5. Click Merge PDFs.

## Run from source

You need Python 3.13 on macOS. The GUI uses Tkinter, which comes with the python.org installer and with Homebrew `python-tk`.

1. Make a virtual environment (a private folder of Python packages for this project):

   ```bash
   python3 -m venv venv
   ```

2. Install the packages:

   ```bash
   venv/bin/pip install -r requirements.txt
   ```

3. Start the GUI:

   ```bash
   venv/bin/python pdf_merger_gui.py
   ```

To use the command line instead of the GUI, run `merge_pdfs.py`:

```bash
venv/bin/python merge_pdfs.py front.pdf back.pdf merged.pdf
```

If the back sides are in the same order as the front sides, add `--no-reverse-back`. The script exits with code 1 if the merge fails.

## Develop

1. Install the development packages into the virtual environment:

   ```bash
   venv/bin/pip install -r requirements-dev.txt
   ```

2. Run the tests:

   ```bash
   venv/bin/python -m pytest
   ```

3. Build the macOS app:

   ```bash
   venv/bin/pyinstaller --noconfirm pdf_merger.spec
   ```

The build writes `dist/PDF Merger.app`. To make the release zip, run this command:

```bash
ditto -c -k --keepParent "dist/PDF Merger.app" dist/pdf-merger-macos.zip
```
