# Lustrous Launcher
_The Sleek, Simple Game Launcher_

### What is Lustrous Launcher?
Lustrous Launcher is the sleek, simple game launcher, designed to make launching games a more pleasant experience.
Lustrous Launcher opens quickly and doesn't hang around in the background hogging resources!

### Version 1.5 Released: A message from Spatchy (THIS IS HUGE!)
Version 1.5 has just dropped with a search bar, redesigned settings menu and FREAKIN' STEAM LIBRARY INTEGRATION! Check out the rest of the changes below! Sorry this one took so long, I've had exams but now they're over and I can get back to maintaining the project!

### Tutorial
Online help and a tutorial can now be found [here](https://spatchy.github.io/Lustrous-Launcher/tutorial)

### EXE version
The EXE version can be downloaded from the [releases page](https://github.com/Spatchy/Lustrous-Launcher/releases/latest)

### Dependencies (Python Script Only)
all dependencies *MUST* be installed before the Lustrous Launcher python script can be used
- [Pillow (PIL)](https://pillow.readthedocs.io/en/latest/installation.html)

### Changelog
###### 1.5
- Fixed bug that caused the back pannel to appear behind other windows or dissappear altogether
- Added search bar! Press enter to search through your huge game library!
- Added Steam button to launch Steam directly from Lustrous Launcher
- Added Steam library integration [Beta]! This new tool in the `Add Games` menu allows you to import your whole library!
- Added auto-updater. No more visiting GitHub, just press the button and the latest version will be installed automatically!
- Redesigned settings menu that's far more user friendly
- Added a bunch of new settings for Steam and the search bar
- A couple of GUI tweaks to make things look a bit nicer
###### 1.4
- `Fix banners` tool added to settings menu to fix transparency issues with some banner images
- Lustrous Launcher no longer crashes when a banner doesn't exist
- Added default.png to assets folder to be used when banner is not found
- Game title is displayed on cards that use the default banner
- Added link to online tutorial in settings
- Made scrolling twice a smooth
- Fixed a bug that started cutting the bottom few pixels off cards if enough games were added
###### 1.3
- Fixed a pretty big bug that cut off the last line of games
###### 1.2
- EXE version is now available! [Get it here!](https://github.com/Spatchy/Lustrous-Launcher/releases/latest)
- `Check for updates` button in settings now does its job and tells you if there's a new version available
- Some code changed behind the scenes for compatibility with EXE version
- Slightly improved speed when loading (json library now used instead of ast)
###### 1.1
- Fixed bug which stopped many games with launchers and DRM from launching
- Added support for all common image types for use as banners
###### 1.0
- First Release

### First Launch (Python Script and <v1.5 Only)
###### From v1.5 onwards, this no longer applies to the EXE version
When you run Lustrous Launcher for the first time, it is very likely you will see an error:
```
Could not install required font.
Try running Lustrous Launcher with admin privileges
```
This is due to the `Font Awesome 5 Free-Solid-900.otf` font file not being able to be installed.
To complete the setup, Lustrous Launcher needs to be run with admin privileges (run the python script from an elevated command window)
Alternatively, you can install the `Font Awesome 5 Free-Solid-900.otf` file manually (it is located in the assets folder) and create two directories `games` and `banners` in the root of the Lustrous Launcher folder

### Coming Soon
- Big customization features!
- Probably lots more
