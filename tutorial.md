_Lustrous Launcher was designed to be as easy to use as possible but in case you needed help with something, this tutorial exists. If you have any feedback or suggestions on how Lustrous Launcher could be improved, don't hesitate to make a post over on the [Lustrous Luncher Subreddit](https://www.reddit.com/r/lustrouslauncher/)_

# Getting Started
_here's how to get started using Lustrous Launcher for the first time_
1. Download Lustrous Launcher from [The Realeases Page](https://github.com/Spatchy/Lustrous-Launcher/releases/latest) (the portable EXE is recommended, only download the Python source code if you know what you're doing!)
2. Move the .zip out of your downloads folder and into a more suitable location (where you move it to is up to you)
3. Unzip the file (right click -> extract all)
4. You should now have a folder named `Lustrous Launcher v1.X` where X is a number denoting the version you have (note: this folder may be inside another folder with the same name as the .zip you extracted)
##### For the EXE version:
5. Inside that folder you should run the file called `main.exe` (or just `main` if you don't have show extensions enabled in windows)
6. It is likely you will see an error `Could not install required font. Try running Lustrous Launcher with admin privillages` Don't worry, this is normal
7. Right click on `main.exe` and select `run as administrator` select `yes` at the UAC prompt
8. You should recieve a confirmation message `Inintial setup is complete. Please run Lustrous Launcher again`
9. You should now run `main.exe` again normally (you do NOT have to run it as administrator anymore)
##### For the Python version (EXE users should skip this!):
5. As with the EXE version, the `main.pyw` must be run as administrator
6. Open an elevated command prompt window (search for cmd then right click -> run as administrator)
7. In the CMD window, CD into the directory where `main.pyw` is contained.
8. type `python main.pyw` and press enter (this assumes python has been added to your windows environment variables)
9. You should recieve a confirmation message `Inintial setup is complete. Please run Lustrous Launcher again`
10. Lustrous Launcher can now be run normally 

# Adding Games
1. To add a game to Lustrous Launcher, press the `+` button on the bottom left in the sidebar
2. The main screen should close and you should be presented with the `Add Games` window
3. Type the name of the game you want to add in the `Title` field (note: Games are sorted by title in alphabetical order, this title will also be used when searching with the search bar in the upcoming version 1.5)
4. In the `Banner` field, you should type the name of the corresponding banner in the `banners` folder (Note: Official banner images can be downloaded from Steam - many more options are available from [Cryotank](http://steam.cryotank.net/), [SteamgridDB](http://www.steamgriddb.com/) and [the Steam Grid subreddit](https://www.reddit.com/r/steamgrid/))
5. To make it easier to drag and drop banner images, you can click the `Open Banner Folder` button to open an explorer window to the `banners` folder.
6. Click the `Choose Game Path` button and select the game EXE from its install location (Note: Some games have multiple EXEs and you need to make sure you select the right one for it to work)
7. Click `Save Game` to add the game to Lustrous Launcher
