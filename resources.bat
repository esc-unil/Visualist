@echo on
pylupdate5 -noobsolete i18n\visualist.pro

@echo off
call "C:\Program Files\QGIS 3.22.0\bin\o4w_env.bat"
call "C:\Program Files\QGIS 3.22.0\bin\qt5_env.bat"
call "C:\Program Files\QGIS 3.22.0\bin\py3_env.bat"

@echo on
pyrcc5 -o resources.py resources.qrc
