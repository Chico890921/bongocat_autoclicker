# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['BongoCat_AutoClicker.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('fonts', 'fonts'),  # 包含 fonts 資料夾
    ],
    hiddenimports=[
        'win32timezone',
        'pkg_resources.py2_warn',
        'kivymd',
        'kivymd.app',
        'kivymd.uix.screen',
        'kivymd.uix.boxlayout',
        'kivymd.uix.label',
        'kivymd.uix.textfield',
        'kivymd.uix.card',
        'kivymd.uix.button',
        'kivymd.icon_definitions',
        'kivymd.icon_definitions.md_icons',
        'kivy.core.text',
        'kivy.core.window',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BongoCat_AutoClicker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不顯示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
