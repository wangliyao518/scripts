for %%i in (bydata-test_01) do (
   if exist %%i:\ (
      for /f "delims=" %%a in ('dir /ad /b /s "%%i:\"^|sort /r') do (
         rd "%%a"
      )
   )
)
pause