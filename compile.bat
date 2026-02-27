@echo off
pyinstaller -F -i ikona.ico main.pyw
xcopy /e /k /h /i images\ dist\images\
ren "dist" "Eco Catcher"
cd "Eco Catcher"
ren main.exe EcoCatcher.exe
pause