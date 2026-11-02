# Installation of custom MTG Forge cards
I provide installation instructions ONLY FOR Windows. For installation on Linux, Android or any other system, everything should be similar but the location of the folders will be different. This is because Windows is what I use to play MTG Forge and where I have been developing this installation process and the cards I'm sharing with it.

## Windows manual installation (RECOMMENDED)
1. Open your computer's File Explorer and write "%APPDATA%\Forge\custom" (without quotes, of course) on the top bar (where the route or name of the current folder is written, like in a web browser) and click Enter to go there. Copy or move the files inside the provided "custom" folder into that opened folder. Remember that each card must go into a folder named after the first letter of its name. For instance "The Chronicler" goes into the folder named "%APPDATA%\Forge\custom\cards\t\the_chronicler.txt".
2. Open your computer's File Explorer and write "%APPDATA%\Forge\decks\commander" (without quotes, of course) on the top bar (where the route or name of the current folder is written, like in a web browser) and click Enter to go there. Copy or move the files inside the provided "decks" folder into that opened folder.
3. Open the File Explorer and go to "%LOCALAPPDATA%\Forge\Cache\pics" (notice the name between % is different than the previous step). Copy or move the files inside the provided "pics" folder into that opened folder. 

## Windows script installation, by Cristichi
I provide a "install custom cards.bat" script for Windows that automatically installs the custom cards and decks. Nonetheless, please make sure to check the script you downloaded line by line to make sure it's not downloading anything, or uploading anything, or executing external code, or doing anything unexpected. The script consists on a few echoes to print text and 3 simple copy files to Forge folders inside AppData.

Please never blindly run scripts from strangers like me. Please never run scripts from other people unless you trust them with your System (both for malicious purposes or skill issues). Also, don't forget to check the contents of the rest of the files you have downloaded. In fact, even if you trust me, please check everything before using it for the first time. You never know if a hacker introduced malware during your download or on whatever website I used to store these files and share them.

The reason why I have a script is mostly for my own use, and perhaps also for tech savvy people who can recognize malware if it is injected into my simple bat file. I can't undermine how much of a risk you accept when running something like this downloaded from the Internet, from both the author or malicious third parties.

After you checked everything and confirmed no malware is going to take all your passwords, you can continue reading.

To install the custom cards just run the script from the folder it was provided in. The script never deletes cards, only adds them (or updates them if you already had a previous version of those cards).

## After installation
Just open MTG Forge and use its built-in deckbuilder to build a deck with your new cards! If the custom cards developer added any decks, you should also have them available right away.