How to convert your .o8s sets into .o8c files
---------

You should use this guide if you've already downloaded sets before the 3.1 version of OCTGN (or possibly made your own uncensored ones) and want a way to migrate those images into OCTGN 3.1

This guide will show you some simple steps to achieve this in MS Windows (In other OS' the steps are the same, but you need to run the o8build in some kind of win emulator or wine.)

1. Put all your .o8s set files **except markers** into a folder somewhere. Say ```C:\Sets```
2. Press **Win+R** (i.e. press and hold the windows key and press R) (On WinXP, just go Start -> Run). A new window will pop-up.
3. In there copy-paste the following (note that the below command assumes your installation directory and sets directory are the ones presented here. If your "Documents" directory is elsewhere, you need to modity the command to point to it, say ```F:\Documents\Octgn\Octgn```. If you put your sets folder in a different location, you need to put that directory in between the "double quotes"
  
  ```C:\Documents\Octgn\OCTGN\o8build.exe -d "C:\Sets" -c```
4. If you did everything correctly, you should see a window open up, run for a bit and close again. If you see red letters before it closes, you did something wrong. Double check the directory paths you put in your command.
5. Go to the directory you put your .o8s files. Inside you will see a "Conversion" folder. Open it.
6. Inside you will see two folders. "Sets" and "SetImages". Enter "SetImages"
7. Inside you will see a folder named as a GUID. Right click this folder and compress it into a .zip file with whatever program you want. Make sure you use the ZIP algorithm and nor rar or 7z! 
8. Once you have a .zip file, rename it, and change .zip to .o8c. Your card file is now ready for import. You can now delete the conversion folder.

Once you have your .o8c file, adding it into OCTGN is very easy. Simply go "Game Manager", Press "add .o8c" and select your newly created file.
