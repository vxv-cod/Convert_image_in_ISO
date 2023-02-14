xcopy %CD%\*.ico %CD%\dist /H /Y /C /R
pyinstaller -w -F -i "logo.ico" Convert_image_in_ICO.py

