# Lustrous Launcher
_Sleek, Simple Game Launcher_

### What is Lustrous Launcher?
Lustrous Launcher is a sleek, simple game launcher designed to make launching games a more pleasant experience.
Lustrous Launcher launches quickly and doesn't hang around in the background hogging resources!

#####EXE version is now available! 
[Get it here!](https://github.com/Spatchy/Lustrous-Launcher/releases/tag/1.2)

###Dependencies
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
######1.2
- EXE version is now available! [Get it here!](https://github.com/Spatchy/Lustrous-Launcher/releases/tag/1.2)
- `Check for updates` button in settings now does its job and tells you if there's a new version available
- Some code changed behind the scenes for compatibility with EXE version
- Slightly improved speed when loading (json library now used instead of ast)
###### 1.1
- Fixed bug which stopped many games with launchers and DRM from launching
- Added support for all common image types for use as banners
###### 1.0
- First Release

### Coming Soon
- EXE version
- A Completed settings menu
- A Cleaned up `add game` GUI
- Steam library integration
- Quicker launching when there are lots of games
- Tutorial?
- Probably lots more
