@echo off

set repository_url=https://vcgitlab.iwr.uni-heidelberg.de/lmarks/plugins.git
set "folder_name=%~dp0"
set additional_folder=plugins
set script_name=load_plugins.py
set version_control_file=version_control.txt

set "python_script=%folder_name%paraview.py"
python "%python_script%"

set "line_number=1"
set "branch_name="

for /f "usebackq skip=%line_number% delims=" %%G in ("%folder_name%%version_control_file%") do (
    set "branch_name=%%G"
    goto :next
)
:next
<"%folder_name%%version_control_file%" set /p version_name=
echo The extracted line: %branch_name%
if exist "%folder_name%%additional_folder%\" (
    rem If the folder exists, perform a Git pull to update the repository
    echo Updating existing repository for Paraview version %branch_name%...
    cd %folder_name%%additional_folder%
    git checkout %branch_name%
    git pull
) else (
    rem If the folder does not exist, perform a Git clone to create the repository
    echo Cloning new repository for Paraview version %branch_name%...
    echo  %branch_name% %repository_url% %folder_name%%additional_folder%
    git clone -b %branch_name% %repository_url%
)



set script_path=%folder_name%%additional_folder%\%script_name%
set paraview_cmd="%folder_name%Paraview\%version_name%\bin\paraview.exe"

start "ParaView" /B %paraview_cmd% --script="%script_path%"
echo ParaView started.
timeout /t 5 >nul

