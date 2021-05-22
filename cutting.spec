# -*- mode: python -*-

block_cipher = None


a = Analysis(['cutting.py'],
             pathex=['F:\\GitHub\\FF14-Tools-Package'],
             binaries=[],
             datas=[('F:\\GitHub\\FF14-Tools-Package\\lib\\start.mp3','.'),('F:\\GitHub\\FF14-Tools-Package\\lib\\end.mp3','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='cutting',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='F:\\GitHub\\FF14-Tools-Package\\fav.ico')
