# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['QR_base_attandance.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/gulsu/AppData/Local/Programs/Python/Python313/Lib/site-packages/pyzbar', 'pyzbar')],
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
    a.binaries,
    a.datas,
    [],
    name='QR_Yoklama_Sistemi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
