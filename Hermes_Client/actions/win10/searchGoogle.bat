@echo off
set "searchString=%~1"
set "searchString=%searchString:search google=%"
powershell.exe start-process ('https://google.com/search?q=%searchString%')
