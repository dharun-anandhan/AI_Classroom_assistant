import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--add-data=assets;assets',
    '--icon=assets/icon.ico',
    '--name=Classroom_Assistant_v2'
])