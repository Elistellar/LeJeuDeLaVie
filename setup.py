from cx_Freeze import setup, Executable

setup(
    name='LeJeuDeLaVie',
    version='0.1',
    executables=[Executable('main.pyw', base='Win32GUI', icon='icon.ico')]
)