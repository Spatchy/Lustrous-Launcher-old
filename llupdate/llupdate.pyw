import urllib.request
from urllib.request import urlretrieve
import json
import zipfile
import os
import shutil
from tkinter import *
from tkinter import messagebox as tkm
import threading
import webbrowser
from sys import exit


root = Tk()
root.geometry(str(int(int(root.winfo_screenwidth()/6))) + "x" + str(int(int(root.winfo_screenheight())/6)))
root.config(bg = "#FFFFFF")
root.wm_title("Auto-Updater")
root.iconbitmap("./logo.ico")
updatevar = StringVar()

def update(flavour, installdir):
    #Obtain latest version number and locate file for download
    updatevar.set("Collecting version info")
    try:
        latestrelease = json.loads(urllib.request.urlopen("https://api.github.com/repos/Spatchy/Lustrous-Launcher/releases/latest").read().decode('utf-8'))["tag_name"]
        updatevar.set("Downloading Lustrous Launcher v"+latestrelease)
        if flavour == "pyw":
            zipurl = "https://github.com/Spatchy/Lustrous-Launcher/archive/{0}.zip".format(latestrelease)
            foldername = "Lustrous-Launcher-{0}".format(latestrelease)
        else:
            zipurl = "https://github.com/Spatchy/Lustrous-Launcher/releases/download/{0}/Portable-EXE.zip".format(latestrelease)
            foldername = "Lustrous Launcher v{0}".format(latestrelease)

        #check if updatedir exists and create it if not
        try:
            os.stat("./updatedir/")
        except FileNotFoundError:
            os.mkdir("./updatedir/")  

        #download zip to updatedir
        urlretrieve(zipurl, filename = "./updatedir/update.zip")
        updatevar.set("Archive downloaded, preparing to extract files")

        #extract zip file
        zip_ref = zipfile.ZipFile("./updatedir/update.zip", 'r')
        zip_ref.extractall("./updatedir/")
        zip_ref.close()
        
        for file in os.listdir("./updatedir/"+foldername):
            try:
                if file != "llupdate/":
                    try:
                        shutil.copytree("./updatedir/"+foldername+"/"+file+"/", installdir+"/"+file)
                    except FileExistsError: #delete existing file then try again
                        shutil.rmtree(installdir+"/"+file)
                        shutil.copytree("./updatedir/"+foldername+"/"+file+"/", installdir+"/"+file)
            except:
                try:
                    shutil.copy("./updatedir/"+foldername+"/"+file, installdir+"/"+file)
                except FileExistsError: #delete existing file then try again
                    os.remove(installdir+"/"+file)
                    shutil.copy("./updatedir/"+foldername+"/"+file, installdir+"/"+file)
            updatevar.set(file+" copied")
            
        shutil.rmtree("./updatedir/")
        if tkm.askyesno("Success!", "Update completed successfully!\nWould you like to view the changlog?"):
            webbrowser.open("https://github.com/Spatchy/Lustrous-Launcher/blob/master/README.md")
            exit()
        else:
            exit()
                    
                
    except Exception as error:
        tkm.showerror("Error", "An error occurred, please check your connection.\nIf the error persists, please download manually")
        errorlog = open("errorlog.txt", "w")
        errorlog.write(str(error))
        errorlog.close()

def updatethread():
    if getattr(sys, 'frozen', False):
        installdir = str(os.path.dirname(sys.executable)).replace("\\llupdate","")
        flavour = "exe"
        print(installdir)
    else:
        installdir = str(os.path.dirname(__file__)).replace("\\llupdate","")
        flavour = "pyw"
        print(installdir)
    
    t = threading.Thread(target = lambda: update(flavour, installdir))
    t.start()
    updatebtn.pack_forget()


updatevar.set("Click the update button to proceed")
updatelbl = Label(root, textvariable = updatevar, bg = "#FFFFFF")
root.update_idletasks()
updatelbl.pack()
updatebtn = Button(root, text = "Update", command = updatethread)
updatebtn.pack()
root.mainloop()



