@echo off

rem ******************************
rem * 按时间删除文件目录的批处理 *
rem ******************************

rem 设置临时目录的路径
set tempDir=%tmp%\remove_%date:~0,10%
if not exist %tempDir% md %tempDir%
rem 设置处理日期的脚本文件的路径
set scriptFile=%tempDir%\get_date.vbs

rem 获得要保留的天数
set days=%~1
if "%days%" == "" goto printUsage
rem 获得目标目录的路径
set dirPath=%~2
if "%dirPath%" == "" set dirPath=.
rem 获得要操作的文件形式
set fileSpec=%~3
if "%fileSpec%" == "" set fileSpec=*.*

rem 生成计算日期的脚本文件并获得删除的截止日期
echo d=date()-%1 > %scriptFile%
echo s=right("0000" ^& year(d),4) ^& "-" ^& right("00" ^& month(d),2) ^& "-" ^& right("00" ^& day(d),2) >> %scriptFile%
echo wscript.echo s >> %scriptFile%
for /f %%i in ('cscript /nologo %scriptFile%') do set lastDate=%%i

rem 处理目标目录里的每个对象
for /f "tokens=1,2,3* delims=<> " %%i in ('dir "%dirPath%\%fileSpec%" /a /-c /tc') do call :proc "%%i" "%%j" "%%k" "%%l"
goto :done

rem 处理目标目录里对象的过程
:proc
rem 获得对象的创建日期并判断是否为有效格式
set fileDate=%~1
echo %fileDate% | findstr "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]" > nul
if errorlevel 1 goto end
rem 获得对象的类型
set fileType=%~3
if "%fileType%" == "" goto end
rem 获得对象的名称
set fileName=%~4
if "%fileName%" == "" goto end
if "%fileName%" == "." goto end
if "%fileName%" == ".." goto end
if "%fileName%" == "字节" goto end
if "%fileName%" == "可用字节" goto end
rem 判断对象日期是否小于或等于删除的截止日期
if "%fileDate:~0,10%" leq "%lastDate%" (
 echo deleting "%fileName%" ...
 if "%fileType%" == "DIR" ( rd /s /q "%dirPath%\%fileName%" ) else ( del /q /f "%dirPath%\%fileName%" )
)
goto end

:error
echo An error occurred during backuping.

:done
rd /s /q %tempDir%
goto end

:printUsage
echo Usage: %0 ^<Days^> [Work directory] [Target file specification (can include wildcards)]
goto end

:end