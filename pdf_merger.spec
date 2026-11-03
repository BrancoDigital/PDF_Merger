# -*- mode: python ; coding: utf-8 -*-
# Build: pyinstaller --noconfirm pdf_merger.spec
# Output: dist/PDF Merger.app (windowed, no Terminal window)

a = Analysis(
    ['pdf_merger_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF Merger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='PDF Merger',
)
app = BUNDLE(
    coll,
    name='PDF Merger.app',
    icon=None,
    bundle_identifier='digital.branco.pdfmerger',
    info_plist={'CFBundleShortVersionString': '1.1.0'},
)
