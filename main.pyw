#Lustrous Launcher
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import threading
import subprocess
import time
import os
import webbrowser
import glob
from PIL import Image, ImageTk
import urllib.request
import json
import fontinstall
from sys import exit

if not os.path.exists("./games"): #first launch
    try:
        if getattr(sys, 'frozen', False): #check if the version is exe or not
            currentdir = os.path.dirname(sys.executable)
        else:
            currentdir = os.path.dirname(__file__)
        fontinstall.install_font(currentdir + "\\assets\\Font Awesome 5 Free-Solid-900.otf")
        root = Tk()
        root.withdraw()
        os.makedirs("./games")
        os.makedirs("./banners")
        messagebox.showinfo("Setup Complete", "initial setup is complete!\nPlease run Lustrous Launcher again!")
        exit()
    except PermissionError as permerror:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error","Could not install required font.\nTry running Lustrous Launcher with admin privileges\n\nInstall failed with following error:\n" + str(permerror))
        exit()


global exitcode
global VERSION
exitcode = 0
VERSION = "1.4"

root = Tk()
root.geometry(str(root.winfo_screenwidth()) + "x" + str(int(root.winfo_screenheight())-40))
root.overrideredirect(1)
root.config(bg="#000000")
root.wm_attributes("-alpha","0.7")

#set up toplevel for alpha-free controls
top = Toplevel()
top.geometry(str(root.winfo_screenwidth()) + "x" + str(int(root.winfo_screenheight())-40))
top.overrideredirect(1)
top.config(bg="#000001")
top.wm_attributes("-topmost",1)
top.wm_attributes("-transparentcolor","#000001")#hopefully no one uses this in steam banners in large amounts

#various closing conditions
def close(event):
    root.destroy()
    try:
        if event in [0,1,2]:
            global exitcode
            exitcode = event
    except:
        pass
root.bind("<Button-1>",close)
root.bind("<Escape>",close)
top.bind("<Button-1>",close)
top.bind("<Escape>",close)
top.bind("<FocusOut>",close)


#sidebar
sidebar = Frame(top, height = (int(root.winfo_screenheight())-40), width = 48, bg = "#060606")
sidebar.pack(side = LEFT)
sidebar.pack_propagate(0)


#sidebar buttons
def btnhover(btn, istrue): #hover event
    if istrue:
        btn.config(bg = "#222222")
    else:
        btn.config(bg = "#060606")
    
addgamebtn = Label(sidebar, text="", font=("Font Awesome 5 Free Solid", 16), fg = "#FFFFFF", bg = "#060606", justify = CENTER)
addgamebtn.pack(side = BOTTOM, pady = (0,10), anchor = CENTER)
addgamebtn.bind("<Enter>", lambda x: btnhover(addgamebtn, True))
addgamebtn.bind("<Leave>", lambda x: btnhover(addgamebtn, False))
addgamebtn.bind("<Button-1>", lambda x: close(2))

settingsbtn = Label(sidebar, text="", font=("Font Awesome 5 Free Solid", 16), fg = "#FFFFFF", bg = "#060606", justify = CENTER)
settingsbtn.pack(side = BOTTOM, pady = (0,20), anchor = CENTER)
settingsbtn.bind("<Enter>", lambda x: btnhover(settingsbtn, True))
settingsbtn.bind("<Leave>", lambda x: btnhover(settingsbtn, False))
settingsbtn.bind("<Button-1>", lambda x: close(1))

class Gamelink(Frame):
    def __init__(self, parent, bannerimg, link, title):
        super(Gamelink, self).__init__(parent)
        self.pack_propagate(1)
        self.pilimage = Image.open(bannerimg)
        self.imggif = ImageTk.PhotoImage(self.pilimage)
        self.banner = Label(self, width = 460, height = 215, image = self.imggif, bg = "#000001")
        self.banner.image = self.imggif
        if bannerimg == glob.glob(os.path.join("./assets", "default.png"))[0]:
            self.titlelbl = Label(self, text = title, bg = "#D83434", fg = "#FFFFFF")
            self.titlelbl.place(relx = 0.0, rely = 0.0)
        self.banner.pack()
        def opengame(event):
            def openit():
                subprocess.run(link, shell=True)
            self.t = threading.Thread(target = openit)
            self.t.start()
            time.sleep(2)
            close(0)
        def onhover(event):
            self.banner.config(bg = "#777777")
        def onleave(event):
            self.banner.config(bg = "#000001")
        self.banner.bind("<Button-1>",opengame)
        self.banner.bind("<Enter>",onhover)
        self.banner.bind("<Leave>",onleave)
        
        

class Gamegrid(Frame):
    def __init__(self, parent, columns, h, w):
        super(Gamegrid, self).__init__(parent)
        self.config(bg = "#000001")
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.area = Canvas(self, yscrollcommand=self.scrollbar.set, width = w, height = h, bg = "#000001", bd = 0, highlightthickness = 0)
        self.gridframe = Frame(self, width = w, bg = "#000001")
        self.gridframe.pack_propagate(0)
        self.area.create_window((0, 0), window = self.gridframe, anchor = N)
        Columns = int((w-48)/540)-1 #(screen width-sidebar)/width of card+padding, -1 because columns start at 0
        Column = 0
        Row = 0
        for file in os.listdir("./games"): #recur through json files
            content = json.loads(open("./games/"+str(file)).read()) #read content of json to dict
            gametitle = content["title"] #get game title
            try:
                imgpath = glob.glob(os.path.join("./banners", str(content["bannername"]) + '.*'))[0] #get banner path
            except IndexError: #God knows why an IndexError is raised if the banner doesn't exist!
                imgpath = glob.glob(os.path.join("./assets", "default.png"))[0]
            linkpath = content["path"] #get exe path
            if Column > Columns:
                Column = 0
                Row += 1
            if Row == 0: #additional top padding
                Gamelink(self.gridframe, imgpath, linkpath, gametitle).grid(column = Column, row = Row, padx = (80, 0), pady = (80, 40))
            else:
                Gamelink(self.gridframe, imgpath, linkpath, gametitle).grid(column = Column, row = Row, padx = (80, 0), pady = (0, 40))
            Column += 1
            if Row < 4:
                self.gridframe.config(height = (259*4)+80) #this prevents a weird 'negative scroll'
            else:
                self.gridframe.config(height = (259*(Row+1))+80)#create enough height for everything (259=card height+padding+bd)(+80 for top padding) +1 BEACUSE ROWS START AT 0!!!
        if Column == 0 and Row == 0: #means there are no games added
            nogameslbl = Label(self, text = "You have no games - Click  to add some\nClick anywhere or press ESC to close", bg = "#000001", fg = "#FFFFFF", font=("Font Awesome 5 Free Solid",16))
            nogameslbl.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        self.area.pack()
        self.area.config(scrollregion = (self.area.bbox("all")))
        self.scrollbar.config(command = self.area.yview)
        def onScroll(event):
            self.area.yview_scroll(int(-1*(event.delta/60)), "units")
        self.area.bind_all("<MouseWheel>", onScroll)
        self.scrollbar.pack_forget() #scroll wheel still works!

        
        
testgrid = Gamegrid(top, 2,root.winfo_screenheight(), root.winfo_screenwidth()-48)
testgrid.pack(side = RIGHT, anchor = CENTER)
    

root.mainloop()


def settings():
    root = Tk()
    root.config(bg = "#FFFFFF")
    root.geometry(str(int(int(root.winfo_screenwidth()/3))) + "x" + str(int(int(root.winfo_screenheight())/3)))
    root.wm_title("Settings")
    root.iconbitmap("./assets/logo.ico")

    while True:
        try:
            settingsfile = open("settings.ini","r+")
            break
        except FileNotFoundError:
            settingsfile = open("settings.ini","w")
            if getattr(sys, 'frozen', False): #check if version is exe or pyw
                settingsfile.write("flavour=exe")
            else:
                settingsfile.write("flavour=pyw")
            settingsfile.close()

    settingsdict = {}#read settings.ini to dict for easier editing
    for line in settingsfile:
        settingsdict[line.split("=")[0]] = line.split("=")[1].strip("\n")
    def update():
        latestrelease = json.loads(urllib.request.urlopen("https://api.github.com/repos/Spatchy/Lustrous-Launcher/releases/latest").read().decode('utf-8'))["tag_name"]
        if int(latestrelease.replace(".","")) > int(VERSION.replace(".","")):
            if messagebox.askyesno("Update Available!", "This version is: {0}\nThe latest release is: {1}\n\nDo you want to go to Github and download it now?".format(VERSION, latestrelease)):
                webbrowser.open("https://github.com/Spatchy/Lustrous-Launcher/releases/tag/" + latestrelease)
        else:
            messagebox.showinfo("Up To Date!", "Lustrous Launcher is up to date!")
    checkupdatebtn = Button(root, text = "Check for updates", command = update)
    checkupdatebtn.pack(side = BOTTOM)

    fixbannersframe = Frame(root, bg = "#FFFFFF")
    fixbannerslbl = Label(fixbannersframe, text = "Lustrous Launcher treats the hex color #000001 as transparent\nIf a banner contains this color, it can appear broken", bg = "#FFFFFF")
    fixbannerslbl.grid(row = 0, column = 0)
    
    def bannerfix(): #replaces #000001 with #000000
        numfixed = 0
        numchecked = 0
        for banner in os.listdir("./banners"):
            numchecked += 1
            detected = False
            img = Image.open("./banners/" + banner)
            pixdata = img.load()
            progtext.set("Banners checked: {0}/{1}".format(numchecked, str(len(os.listdir("./banners")))))
            fixbannersprogresslbl.update_idletasks()
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    if pixdata[x, y] == (0, 0, 1):
                        pixdata[x, y] = (0, 0, 0)
                        detected = True #detects if the banner needed fixing
            if detected:
                numfixed += 1
            img.save("./banners/" + banner)
        if messagebox.showinfo("Complete", "{0} banners were detected as broken and were fixed".format(numfixed)):
            progtext.set("") 
    fixbannersbtn = Button(fixbannersframe, text = "Fix broken banners", command = bannerfix)
    progtext = StringVar()
    fixbannersprogresslbl = Label(fixbannersframe, textvariable = progtext, bg = "#FFFFFF")
    fixbannersprogresslbl.grid(row = 1, column = 0, columnspan = 2)
    fixbannersbtn.grid(row = 0, column = 1)
    fixbannersframe.pack()

    def opentutorial():
        webbrowser.open("https://spatchy.github.io/Lustrous-Launcher/tutorial")
    helpframe = Frame(root, bg = "#FFFFFF")
    helplbl = Label(helpframe, text = "Help documentation is now available online", bg = "#FFFFFF")
    tutorialbtn = Button(helpframe, text = "View online help", command = opentutorial)
    helplbl.grid(row = 0, column = 0)
    tutorialbtn.grid(row = 0, column = 1)
    helpframe.pack()
    
    root.mainloop()

def addgame():
    root = Tk()
    root.wm_title("Add Game")
    root.iconbitmap("./assets/logo.ico")
    root.geometry(str(int(int(root.winfo_screenwidth()/3))) + "x" + str(int(int(root.winfo_screenheight())/3)))

    titleframe = Frame(root)
    titlelbl = Label(titleframe, text = "Game Title: ", width = 15)
    titleenter = Entry(titleframe)
    titlelbl.grid(column = 0, row = 0, sticky = W)
    titleenter.grid(column = 1, row = 0, sticky = W+E)
    titleframe.pack(expand = True, fill = X)

    titleframe.grid_columnconfigure(1, weight=3)

    bannerframe = Frame(root)
    bannerlbl = Label(bannerframe, text = "Banner Name: ", width = 15)
    bannerenter = Entry(bannerframe)
    def openbannerfolder():
        if getattr(sys, 'frozen', False):
            currentdir = os.path.dirname(sys.executable)
            print(currentdir)
        else:
            currentdir = os.path.dirname(__file__)
        bannersdir = currentdir + "\\banners"
        subprocess.Popen(["explorer.exe", bannersdir])
    bannerbtn = Button(bannerframe, text = "Open Banner Folder", command = openbannerfolder)
    bannerwarn = Label(bannerframe, text = "Banners must be in the 'banners' folder - DO NOT include path or file extension")
    bannerlbl.grid(row = 0, column = 0, sticky = W)
    bannerenter.grid(row = 0, column = 1, sticky = E+W)
    bannerbtn.grid(row = 0, column = 2, sticky = E)
    bannerwarn.grid(row = 1, column = 0, columnspan = 3)
    bannerframe.pack(expand = True, fill = X)

    bannerframe.grid_columnconfigure(1, weight=3)
    
    pathframe = Frame(root)
    pathstring = StringVar()
    pathlbl = Label(pathframe, text = "Path To Game: ", width = 15)
    pathbox = Entry(pathframe, textvariable = pathstring)
    def getpath():
        gamefile = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("EXE Files","*.exe"),("Shortcuts","*.lnk"),("Steam Internet Shortcut","*.url")))
        pathstring.set(str(gamefile))

    pathbtn = Button(pathframe, text = "Choose Game Path", command = getpath)
    pathlbl.grid(row = 0, column = 0)
    pathbox.grid(row = 0, column = 1, sticky = E+W)
    pathbtn.grid(row = 0, column = 2)
    pathframe.pack(expand = True, fill = X)

    pathframe.grid_columnconfigure(1, weight=3)

    def savegame():
        jsondict = {}
        jsondict["title"] = titleenter.get()
        jsondict["path"] = pathbox.get()
        jsondict["bannername"] = bannerenter.get()
        jsonfile = open("./games/" + titleenter.get() + ".json","w")
        jsonfile.write(str(jsondict).replace("'",'"'))
        if messagebox.askyesno("Done!", "Would you like to add another game?"):
            titleenter.delete(0, END)
            pathbox.delete(0, END)
            bannerenter.delete(0, END)
        else:
            root.destroy()
        
        

    savebtn = Button(root, text = "Add Game To Launcher", command = savegame)
    savebtn.pack(side = BOTTOM)
    root.mainloop()
    

if exitcode == 1:
    settings()
elif exitcode == 2:
    addgame()
