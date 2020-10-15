for /f "tokens=1 delims=." %%d in ('dir /b /d *tar.gz') do (
md %%d
@echo Directory %%~nd Created
7z x %%d.tar.gz
7z x -o%%~nd %%d.tar
del /S %%d.tar
@echo Archive %%~nd %%d.tar.gz uncompressed
break)