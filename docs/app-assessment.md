# App assessment, November 2026

This document records an audit of PDF Merger from 2026-11-19. The audit answers three questions. Is the feature already in other tools? Is PDFgear open source? What work makes this repo a full app for macOS, Windows, and Linux? The audit changed no code.

## Result

The feature is a real need, but other tools have it. PDFgear is closed source, so a fork or a pull request is not possible. The recommended path is to keep the Python code and finish the macOS app first. Windows and Linux builds come after that.

## The feature in other tools

PDF Merger interleaves two scans. To interleave is to take pages from two files in turn: front 1, back 1, front 2, back 2. It also reverses the back sides, because an auto-feed scanner gives them last page first.

Adobe Acrobat has no command that interleaves two PDFs that exist. It can interleave during a scan, with the "Scan reverse sides" prompt. Users on the Adobe forums use third-party scripts or drag the pages by hand. The web search found no PDFgear documentation for an interleave feature.

These tools have the feature:

- PDFsam Basic: free, open source, for macOS, Windows, and Linux. The "Alternate Mix" tool has a reverse order setting for each file.
- Foxit PDF Editor: "Interleave Pages" in the Organize menu.
- Sejda: the "Alternate & Mix" tool.
- UPDF: an interleave pages tool.
- PDFtk: the `shuffle` command on the command line.

The gap is a small app that does only this job. The tools in the list are large suites, a Java app, a command-line tool, or web sites that need an upload.

## PDFgear

PDFgear is proprietary freeware. A Wikipedia mirror and AlternativeTo list the license as proprietary. No public source repository exists. The audit did not read the license text that ships with the app.

The only route to this feature in PDFgear is a feature request to PDFgear support. If you want to contribute to an open source tool, there are two candidates. PDFsam Basic already has the feature. PDF Mix Tool has an open request for it: issue 28 in `scarpetta/pdfmixtool` on GitLab.

## Audit of this repo

The repo holds 79 lines of merge logic in `merge_pdfs.py`, a Tkinter window in `pdf_merger_gui.py`, 5 tests, and a PyInstaller build file. The merge logic is correct for its tested cases. The audit found these gaps:

1. The app is not signed. macOS blocks it at the first start. A signed and notarized app needs an Apple Developer account, which costs $99 for each year.
2. The app is 27 MB and has no icon. The window does not accept files that you drag onto it.
3. The merge fails when the page counts differ (`merge_pdfs.py:25`). This occurs when the last sheet has a blank back side that you did not scan.
4. The app shows no preview of the page order before it writes the file.
5. The merge runs on the user interface thread. A large file freezes the window until the merge completes.
6. The build file makes only a macOS app. No build exists for Windows or Linux.

## Paths to a full app

The goal is one app for macOS, Windows, and Linux, with macOS first. A native SwiftUI app does not meet this goal, because SwiftUI runs only on Apple systems. The time values are estimates for work with Claude Code.

1. Keep Python and Tkinter (recommended start). `pypdf` and Tkinter run on all three systems, so the code needs no rewrite. Fix gaps 1 to 5 for macOS in about 1 day. Then add a GitHub Actions workflow that builds the app on each system, in about half a day. PyInstaller cannot build for one system from a different system.
2. Keep Python and replace Tkinter with PySide6 (Qt). The window gets a native look, drag and drop, and a page preview. The app grows to about 60 to 100 MB. About 2 days.
3. Rewrite with Tauri. Tauri is a toolkit that puts a web interface in a small native shell written in Rust. The app is about 10 MB on each system. The merge logic moves to Rust (`lopdf`) or JavaScript (`pdf-lib`). The page preview is easy, because `pdf.js` draws the pages in the web interface. About 3 days.
4. Rewrite in pure Rust with a toolkit such as `egui`, `iced`, or Slint. The result is one binary of about 5 to 10 MB with no web interface. The page preview is the hard part. It needs the Pdfium library in the app, which adds size and build work. About 2 to 3 days without a preview.

Paths 3 and 4 use Rust. Compared with Python, Rust gives a smaller app that starts faster. The app has no Python runtime, so fewer files need a signature. Rust also has costs. You write the merge logic and the 5 tests again. `lopdf` is a lower-level library than `pypdf`, so a page copy between documents takes more code. The audit did not test `lopdf` on scanned PDFs. You still build on each system in GitHub Actions.

Signing is separate work on each system. macOS needs the Apple Developer account. Windows shows a SmartScreen warning for an unsigned app, and a code signing certificate removes it. Linux needs no signature, but it needs a package format such as AppImage or Flatpak.

## Next step

When you return to this work, decide between path 1 and path 2. Path 1 is correct if the app is for you and a few users. Path 2 is correct if you want public releases with a preview and a native look. Path 3 is correct if you want public releases and a small app on all three systems. Of the two Rust paths, path 3 is the recommended one, because the preview is easy.

## Sources

- [Adobe community: merge even and odd pages](https://community.adobe.com/t5/acrobat-discussions/how-can-i-merge-even-and-odd-pages-of-a-pdf/m-p/15467625)
- [MetaFilter: interleave pages in Adobe Pro](https://ask.metafilter.com/354565/How-to-interleave-pages-in-Adobe-Pro)
- [nyoungstudios Acrobat PDF Tools scripts](https://github.com/nyoungstudios/Adobe-Acrobat-PDF-Tools)
- [PDFsam: mix PDF](https://pdfsam.org/mix-pdf/)
- [Foxit: Interleave Pages](https://resource-cms.foxit.com/foxit-pdf-editor-for-windows/interleave-pages)
- [UPDF: interleave pages](https://updf.com/ar/organize-pdf/interleave-pages/)
- [AlternativeTo: PDFgear](https://www.alternativeto.net/software/pdfgear/about/)
- [r/opensource: is PDFgear open source](https://axebps-redlib.hf.space/r/opensource/comments/1auim4h/is_pdfgear_open_source)
- [PDF Mix Tool issue 28: alternate mix request](https://gitlab.com/scarpetta/pdfmixtool/-/issues/28)
