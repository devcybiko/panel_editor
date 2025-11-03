# PyInstaller spec file for Panel Editor
# Run: pyinstaller panel_editor.spec

block_cipher = None

from PyInstaller.utils.hooks import collect_data_files

data_files = collect_data_files('src')

# Entry point
entry_script = 'src/panel_editor.py'

# If you need to include additional files (CSS, assets, etc.), add them to datas
# Example: datas = [('src/css/panel_editor.css', 'css')]
datas = data_files

# Build the executable

a = Analysis([
    entry_script
],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='panel_editor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)
