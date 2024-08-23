# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run.py'],
    pathex=['C:\\Users\\joao.silva\\Desktop\\oficial-tavellas\\venv\\Lib\\site-packages'],
    binaries=[],
  datas=[
        ('C:\\Users\\joao.silva\\Desktop\\oficial-tavellas\\app\\public', 'app/public'),
        ('C:\\Users\\joao.silva\\Desktop\\oficial-tavellas\\app\\views', 'app/views'),
    ],
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
    name='run',
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
    icon=['C:\\Users\\joao.silva\\Downloads\\transportation_sport_bike_bicycle_summer_icon_251698.ico'],
)
