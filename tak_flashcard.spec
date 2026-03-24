# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Tak Flashcard application."""

a = Analysis(
    ['src/tak_flashcard/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/tak_flashcard/img/logo.png', 'tak_flashcard/img')],
    hiddenimports=[
        'sqlalchemy.dialects.sqlite',
        'tkinter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tak_flashcard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon='src/tak_flashcard/img/logo.png',
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
