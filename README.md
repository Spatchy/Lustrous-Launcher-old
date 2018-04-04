# Lustrous Launcher
_The Sleek, Simple Game Launcher_

### What is Lustrous Launcher?
Lustrous Launcher is the sleek, simple game launcher, designed to make launching games a more pleasant experience.
Lustrous Launcher opens quickly and doesn't hang around in the background hogging resources!
Download the latest release [here](https://spatchy.github.io/Lustrous-Launcher/tutorial)

### Tutorial
Online help and a tutorial can now be found [here](https://spatchy.github.io/Lustrous-Launcher/tutorial)

### EXE version
The EXE version can be downloaded from the [releases page](https://github.com/Spatchy/Lustrous-Launcher/releases/latest)

### Dependencies (Python Script Only)
all dependencies *MUST* be installed before the Lustrous Launcher python script can be used
- [Pillow (PIL)](https://pillow.readthedocs.io/en/latest/installation.html)

### First Launch
When you run Lustrous Launcher for the first time, it is very likely you will see an error:
```
Could not install required font.
Try running Lustrous Launcher with admin privileges
```
This is due to the `Font Awesome 5 Free-Solid-900.otf` font file not being able to be installed.
To complete the setup, Lustrous Launcher needs to be run with admin privileges (run the python script from an elevated command window)
Alternatively, you can install the `Font Awesome 5 Free-Solid-900.otf` file manually (it is located in the assets folder) and create two directories `games` and `banners` in the root of the Lustrous Launcher folder

### Changelog
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

### Coming Soon
- A Completed settings menu
- Steam library integration
- Big customization features!
- Quicker launching when there are lots of games
- Probably lots more
