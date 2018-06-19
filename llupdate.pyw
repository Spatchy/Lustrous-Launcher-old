import urllib.request
from urllib.request import urlretrieve
import json
import zipfile
import os
import shutil
import errno
from tkinter import *
from tkinter import messagebox as tkm
import threading
import webbrowser

root = Tk()
root.geometry(str(int(int(root.winfo_screenwidth()/6))) + "x" + str(int(int(root.winfo_screenheight())/6)))
root.config(bg = "#FFFFFF")
root.wm_title("Auto-Updater")
root.iconbitmap("./assets/logo.ico")
updatevar = StringVar()

def update(flavour):
    updatevar.set("Collecting version info")
    try:
        latestrelease = json.loads(urllib.request.urlopen("https://api.github.com/repos/Spatchy/Lustrous-Launcher/releases/latest").read().decode('utf-8'))["tag_name"]
        updatevar.set("Downloading Lustrous Launcher v"+latestrelease)
        if flavour == "pyw":
            zipurl = "https://github.com/Spatchy/Lustrous-Launcher/archive/{0}.zip".format(latestrelease)
        else:
            zipurl = "https://github.com/Spatchy/Lustrous-Launcher/releases/download/{0}/Portable-EXE.zip".format(latestrelease)

        #check if updatedir exists and create it if not
        try:
            os.stat("./updatedir/")
        except FileNotFoundError:
            os.mkdir("./updatedir/")  
        
        urlretrieve(zipurl, filename = "./updatedir/update.zip")
        updatevar.set("Archive downloaded, preparing to extract files")

        zip_ref = zipfile.ZipFile("./updatedir/update.zip", 'r')
        zip_ref.extractall("./updatedir/")
        zip_ref.close()
        
        for file in os.listdir("./updatedir/Lustrous Launcher v{0}".format(latestrelease)):
            try:
                try:
                    shutil.copytree("./updatedir/Lustrous Launcher v{0}".format(latestrelease)+"/"+file+"/", "./"+file)
                except FileExistsError: #delete existing file then try again
                    shutil.rmtree("./"+file)
                    shutil.copytree("./updatedir/Lustrous Launcher v{0}".format(latestrelease)+"/"+file+"/", "./"+file)
            except:
                if file != "llupdate.pyw" and file != "update.zip" and file != "llupdate.exe":
                    try:
                        shutil.copy("./updatedir/Lustrous Launcher v{0}".format(latestrelease)+"/"+file, "./"+file)
                    except FileExistsError: #delete existing file then try again
                        shutil.rmtree("./"+file)
                        shutil.copy("./updatedir/Lustrous Launcher v{0}".format(latestrelease)+"/"+file, "./"+file)
            updatevar.set(file+" copied")
            
        shutil.rmtree("./updatedir/")
        if tkm.askyesno("Success!", "Update completed successfully!\nWould you like to view the changlog?"):
            webbrowser.open("https://github.com/Spatchy/Lustrous-Launcher/blob/master/README.md")
            exit()
        else:
            exit()
                    
                
    except Exception as error:
        tkm.showerror("Error", "An error occurred, please check your connection.\nIf the error persists, please download manually")

def updatethread(flavour):
    t = threading.Thread(target = lambda: update(flavour))
    t.start()
    updatebtn.pack_forget()

settingsfile = open("settings.ini","r")
global settingsdict    
settingsdict = {} #read settings.ini to dict for easier parsing
for line in settingsfile:
    settingsdict[line.split("=")[0]] = line.split("=")[1].strip("\n")
settingsfile.close()

flavour = settingsdict["flavour"]

updatevar.set("Click the update button to proceed")
updatelbl = Label(root, textvariable = updatevar, bg = "#FFFFFF")
root.update_idletasks()
updatelbl.pack()
updatebtn = Button(root, text = "Update", command = lambda: updatethread(flavour))
updatebtn.pack()
root.mainloop()



