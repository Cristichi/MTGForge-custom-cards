echo off
echo Install custom MTG Forge content. This process will copy new cards into the appropriate directories and update existing ones, but will not remove any cards that were removed from the custom MTG editions/cards. To continue, please confirm by pressing any key. Otherwise, press Ctrl+C to cancel.
PAUSE

echo Copy custom cards and tokens
xcopy "%~dp0custom" "%APPDATA%\Forge\custom" /E /Y /I

echo Copy custom decks
xcopy "%~dp0decks" "%APPDATA%\Forge\decks\commander" /E /Y /I

echo Copy custom images
xcopy "%~dp0pics" "%LOCALAPPDATA%\Forge\Cache\pics" /E /Y /I

echo Installation complete! Press any key to exit.
pause