python -m nuitka --follow-imports --onefile --standalone --include-package=pygments --include-package-data=playwright --windows-icon-from-ico=icon.ico new.py
for /d %i in (*) do if "%i" == "new.build" rd /s /q "%i"
for /d %i in (*) do if "%i" == "new.dist" rd /s /q "%i"
for /d %i in (*) do if "%i" == "new.onefile-build" rd /s /q "%i"
