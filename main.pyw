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
import unicodedata
import re
import ctypes
from steamfiles import appinfo




#Theme data
PRIHLCOLOR = "#D83434"

def run_setup():
    try:
        if getattr(sys, 'frozen', False): #check if the version is exe or not
            currentdir = os.path.dirname(sys.executable)
        else:
            currentdir = os.path.dirname(__file__)
        fontinstall.install_font(currentdir + "\\assets\\Font Awesome 5 Free-Solid-900.otf")
        fontinstall.install_font(currentdir + "\\assets\\Font Awesome 5 Brands-Regular-400.otf")
        top = Tk()
        top.withdraw()
        os.makedirs("./games")
        os.makedirs("./banners")
        os.makedirs("./shortcuts")
        messagebox.showinfo("Setup Complete", "initial setup is complete!\nPlease run Lustrous Launcher again!")
        exit()
    except PermissionError as permerror:
        top = Tk()
        top.withdraw()
        messagebox.showerror("Error","Could not install required fonts.\nTry running Lustrous Launcher with admin privileges\n\nInstall failed with following error:\n" + str(permerror))
        exit()

if not os.path.exists("./games"): #first launch
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        run_setup()
    else:
        # Re-run the program with admin rights
        if getattr(sys, 'frozen', False):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
        else:    
            top = Tk()
            top.withdraw()
            messagebox.showerror("Error","UAC-elevation is not supported in the py version.\nPlease run main.py once from an admin CMD.\n\nAlternatively, setup manually - see the tutorial on spatchy.github.io")
            exit()
else:
    defaultslist = ["searchonstart=false", "showsearchprompt=true", "solidsearchbg=false", "showsteambtn=true", 'steampath="C:/Program Files (x86)/Steam/Steam.exe"']
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
            settingsfile = open("settings.ini","a")
            for item in defaultslist:
                settingsfile.write("\n"+str(item))
            settingsfile.close()
            
    def settingscompat(defaultslist):
        global settingsdict
        for item in defaultslist:
            if item.split("=")[0] not in settingsdict:
                settingsdict[item.split("=")[0]] = item.split("=")[1]
        settingsfile = open("settings.ini", "w")
        firstline = True
        for item in settingsdict: #save settingsdict to file
            filestring = str(item) + "=" + str(settingsdict[item])
            if firstline:
                settingsfile.write(filestring)
                firstline = False
            else:
                settingsfile.write("\n"+filestring)
        settingsfile.close()
            
    settingsfile = open("settings.ini","r")
    global settingsdict    
    settingsdict = {} #read settings.ini to dict for easier parsing
    for line in settingsfile:
        settingsdict[line.split("=")[0]] = line.split("=")[1].strip("\n")
    settingsfile.close()
    if len(settingsdict) < len(defaultslist):
        settingscompat(defaultslist)


    global exitcode
    global VERSION
    exitcode = 0
    VERSION = "1.6"

    root = Tk()
    root.geometry(str(root.winfo_screenwidth()) + "x" + str(int(root.winfo_screenheight())-40))
    root.overrideredirect(1)
    root.config(bg="#000001")
    root.wm_attributes("-topmost",1)
    root.wm_attributes("-transparentcolor","#000001")#hopefully no one uses this in steam banners in large amounts


    #set up toplevel for semi-transparent backdrop
    top = Toplevel()
    top.geometry(str(root.winfo_screenwidth()) + "x" + str(int(root.winfo_screenheight())-40))
    top.overrideredirect(1)
    top.config(bg="#000000")
    top.wm_attributes("-topmost",1)
    top.wm_attributes("-alpha","0.7")


    #various closing conditions
    def close(event):
        global exitcode
        root.destroy()
        try:
            if event in [0,1,2,3]:
                exitcode = event
            elif type(event) is Gamelink:
                exitcode = event
                
        except:
            pass
    top.bind("<Button-1>",close)
    top.bind("<Escape>",close)
    root.bind("<Button-1>",close)
    root.bind("<Escape>",close)
    root.bind("<FocusOut>",close)


    #sidebar
    sidebar = Frame(root, height = (int(root.winfo_screenheight())-40), width = 48, bg = "#060606")
    sidebar.pack(side = LEFT)
    sidebar.pack_propagate(0)


    #sidebar buttons
    def btnhover(btn, frame, istrue): #hover event
        if istrue:
            btn.config(bg = "#222222")
            frame.config(bg = "#222222")
        else:
            btn.config(bg = "#060606")
            frame.config(bg = "#060606")

    addgamebtnframe = Frame(sidebar, bg = "#060606", width = 48, height = 45)
    addgamebtnframe.pack_propagate(0)
    addgamebtnframe.pack(side = BOTTOM, anchor = CENTER)
    addgamebtn = Label(addgamebtnframe, text="", font=("Font Awesome 5 Free Solid", 16), fg = "#FFFFFF", bg = "#060606", justify = CENTER)
    addgamebtn.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    addgamebtnframe.bind("<Enter>", lambda x: btnhover(addgamebtn, addgamebtnframe, True))
    addgamebtnframe.bind("<Leave>", lambda x: btnhover(addgamebtn, addgamebtnframe, False))
    addgamebtn.bind("<Button-1>", lambda x: close(2))
    addgamebtnframe.bind("<Button-1>", lambda x: close(2))

    settingsbtnframe = Frame(sidebar, bg = "#060606", width = 48, height = 45)
    settingsbtnframe.pack_propagate(0)
    settingsbtnframe.pack(side = BOTTOM, anchor = CENTER)
    settingsbtn = Label(settingsbtnframe, text="", font=("Font Awesome 5 Free Solid", 16), fg = "#FFFFFF", bg = "#060606", justify = CENTER)
    settingsbtn.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    settingsbtnframe.bind("<Enter>", lambda x: btnhover(settingsbtn, settingsbtnframe, True))
    settingsbtnframe.bind("<Leave>", lambda x: btnhover(settingsbtn, settingsbtnframe, False))
    settingsbtn.bind("<Button-1>", lambda x: close(1))
    settingsbtnframe.bind("<Button-1>", lambda x: close(1))

    if settingsdict["showsteambtn"] == "true":
        steambtnframe = Frame(sidebar, bg = "#060606", width = 48, height = 45)
        steambtnframe.pack_propagate(0)
        steambtnframe.pack(side = BOTTOM, anchor = CENTER)
        steambtn = Label(steambtnframe, text="", font=("Font Awesome 5 Brands Regular", 20), fg = "#FFFFFF", bg = "#060606", justify = CENTER)
        steambtn.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        steambtnframe.bind("<Enter>", lambda x: btnhover(steambtn, steambtnframe, True))
        steambtnframe.bind("<Leave>", lambda x: btnhover(steambtn, steambtnframe, False))
        steambtn.bind("<Button-1>", lambda x: close(3))
        steambtnframe.bind("<Button-1>", lambda x: close(3))

    class Gamelink(Frame):
        def __init__(self, parent, bannerimg, link, title, jsonfile):
            super(Gamelink, self).__init__(parent)
            self.pack_propagate(1)
            self.bannerpilimage = Image.open(bannerimg)
            self.bannerimggif = ImageTk.PhotoImage(self.bannerpilimage)
            self.title = title
            self.bannername = bannerimg
            self.jsonfile = jsonfile
            self.path = link
            self.banner = Label(self, width = 460, height = 215, image = self.bannerimggif, bg = "#000001")
            self.banner.image = self.bannerimggif
            if bannerimg == glob.glob(os.path.join("./assets", "default.png"))[0]:
                self.titlelbl = Label(self, text = title, bg = PRIHLCOLOR, fg = "#FFFFFF")
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
            self.banner.bind("<Button-3>", self.editmenu)
        def editmenu(self, event):
            def edit(event):
                close(self)
            def cancel(event):
                self.editlbl.destroy()
            self.editpilimage = Image.open("./assets/edit.png")
            self.editimggif = ImageTk.PhotoImage(self.editpilimage)
            self.editlbl = Label(self, image = self.editimggif, justify = CENTER, bg = "#777777")
            self.editlbl.image = self.editimggif
            self.editlbl.place(relx = 0, rely = 0)
            self.editlbl.bind("<Button-1>", edit)
            self.editlbl.bind("<Button-3>", cancel)
            self.editlbl.bind("<Leave>", cancel)
            
            
            

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
            self.Columns = Columns #expose columns to public
            for c in range(0, Columns+1):
                self.gridframe.columnconfigure(c, minsize = (int(1/Columns))*w)
            Column = 0
            Row = 1
            self.gridframe.rowconfigure(0, minsize = 80)
            self.collection = []
            self.itemsdict = {} #dictionary containing all grided items and their grid values
            for file in os.listdir("./games"): #recur through json files
                content = json.loads(open("./games/"+str(file)).read()) #read content of json to dict
                gametitle = content["title"] #get game title
                self.collection.append(gametitle)
                try:
                    imgpath = glob.glob(os.path.join("./banners", str(content["bannername"]) + '.*'))[0] #get banner path
                except IndexError: #IndexError is raised if the banner doesn't exist
                    imgpath = glob.glob(os.path.join("./assets", "default.png"))[0]
                linkpath = content["path"] #get exe path
                if Column > Columns:
                    Column = 0
                    Row += 1
                Gamelink(self.gridframe, imgpath, linkpath, gametitle, file).grid(column = Column, row = Row, padx = (80, 0), pady = (0, 40))
                Column += 1
                if Row < 4:
                    self.gridframe.config(height = (259*4)+80) #this prevents a weird 'negative scroll'
                else:
                    self.gridframe.config(height = (259*(Row))+80)#create enough height for everything (259=card height+padding+bd)(+80 for root padding) +1 BEACUSE ROWS START AT 0!!!
            if Column == 0 and Row == 1: #means there are no games added
                nogameslbl = Label(self, text = "You have no games - Click  to add some\nClick anywhere or press ESC to close", bg = "#000001", fg = "#FFFFFF", font=("Font Awesome 5 Free Solid",16))
                nogameslbl.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            self.area.pack()
            self.area.config(scrollregion = (self.area.bbox("all")))
            self.scrollbar.config(command = self.area.yview)
            def onScroll(event):
                self.area.yview_scroll(int(-1*(event.delta/60)), "units")
            self.area.bind_all("<MouseWheel>", onScroll)
            self.scrollbar.pack_forget() #scroll wheel still works!
        def getGameTitles(self): #return dict that links card widget object IDs with titles
            returndict = {}
            x = 0
            for game in list(reversed(self.gridframe.grid_slaves())):
                returndict[self.collection[x]] = game
                x += 1
            return returndict
        def getGridPositions(self): #return dict that links card widget object IDs with grid column and row data 
            positiondict = {}
            for child in self.gridframe.children.values():
                xylist = [child.grid_info()["row"], child.grid_info()["column"]]
                positiondict[child] = xylist
            return positiondict
        def displayResults(self, gridlist):
            for game in list(reversed(self.gridframe.grid_slaves())): #clear the frame
                game.grid_forget()
            Columns = self.Columns
            Column = 0
            Row = 1
            for item in gridlist:
                item.grid(row = Row, column = Column, padx = (80, 0), pady = (0, 40))
                Column += 1
                if Column > Columns:
                    Column = 0
                    Row += 1
        def restoreGrid(self, positiondict): #restore all games back to the grid
            for game in list(reversed(self.gridframe.grid_slaves())): #clear the frame
                game.grid_forget()
            for item in positiondict:
                item.grid(row = positiondict[item][0], column = positiondict[item][1], padx = (80, 0), pady = (0, 40))
            

    testgrid = Gamegrid(root, 2,root.winfo_screenheight(), root.winfo_screenwidth()-48)
    testgrid.pack(side = RIGHT, anchor = CENTER)

    class Searchbar(Frame):
        def __init__(self, parent, w):
            super(Searchbar, self).__init__(parent)
            self.w = w
            self.searchtarget = testgrid.getGameTitles()
            self.config(width = w, height = 48)
            self.pack_propagate(0)
            self.updatevar = StringVar() #search entry is bound to this 
            self.typearea = Entry(self, relief = FLAT, justify = CENTER, insertbackground = "#FFFFFF", font = ("",30), fg = "#FFFFFF", textvariable = self.updatevar)
            if settingsdict["solidsearchbg"] == "true":
                self.config(bg = "#060606")
                self.typearea.config(bg = "#060606")
            else:
                self.config(bg = "#000001")
                self.typearea.config(bg = "#000001")
            self.typearea.pack(fill = BOTH)
            self.typearea.focus_set()
            self.updatevar.trace("w", self.search) #when updatevar changes, search is called
            self.positiondict = testgrid.getGridPositions()
        def search(self, *args):
            testgrid.restoreGrid(self.positiondict) #put everything back before searching through it
            self.livelist = []
            gamedict = testgrid.getGameTitles()
            for item in gamedict:
                if item.lower().startswith(self.typearea.get().lower()):
                    self.livelist.append(gamedict[item])
            testgrid.displayResults(self.livelist)

                
    def startsearch(event):
        search = Searchbar(root, root.winfo_screenwidth())
        search.place(y = 0, x = 48)

    if settingsdict["searchonstart"] == "true":
        startsearch(None)
    else:
        if settingsdict["showsearchprompt"] == "true":
            promptframe = Frame(root, width = root.winfo_screenwidth()-48, height = 48)
            promptframe.pack_propagate(0)
            promptlbl = Label(promptframe, text = "Press enter to search", font = ("",12), fg = "#FFFFFF")
            promptlbl.place(anchor = CENTER, relx = 0.5, rely = 0.5)
            promptframe.place(x=48, y=0)
            if settingsdict["solidsearchbg"] == "true":
                promptframe.config(bg = "#060606")
                promptlbl.config(bg = "#060606")
            else:
                promptframe.config(bg = "#000001")
                promptlbl.config(bg = "#000001")
        root.focus_set()
        root.bind("<Return>", startsearch)
        
    top.mainloop()

    class Checkbox(Label):
        def __init__(self, parent, enabled):
            super(Checkbox, self).__init__(parent)
            self.config(bg = "#FFFFFF")
            self.enabled = enabled
            if self.enabled == "true":
                self.enable()
            else:
                self.disable()
            self.bind("<Button-1>", lambda event: self.toggle())
        def toggle(self):
            if self.enabled == "true":
                self.disable()
            else:
                self.enable()
        def enable(self):
            self.enabled = "true"
            self.config(text = "", font = ("Font Awesome 5 Free Solid", 16), fg = PRIHLCOLOR)
        def disable(self):
            self.enabled = "false"
            self.config(text = "", font = ("Font Awesome 5 Free Solid", 16), fg = "#AAAAAA")
        def get(self):
            return self.enabled

    class ImportOption(Frame):
        def __init__(self, parent, appid, appname):
            super(ImportOption, self).__init__(parent)
            self.pack_propagate(0)
            self.config(bg = "#FFFFFF", height = 60, highlightthickness = 1, highlightcolor = "#090909")
            self.checkbox = Checkbox(self, "true")
            self.checkbox.grid(column = 0, row = 0, rowspan = 2, padx = 5)
            if self.checkbox.get() == "true":
                self.doimport = True
            else:
                self.doimport = False
            self.appname = appname
            self.appid = appid
            self.titlelbl = Label(self, text = self.appname, bg = "#FFFFFF")
            self.titlelbl.grid(column = 1, row = 0, sticky = W)

    class ImportPicker(Frame):
        def __init__(self, parent, nameidmap):
            super(ImportPicker, self).__init__(parent)
            def onFrameConfigure(canvas):
                self.area.config(scrollregion = canvas.bbox("all"))
            self.scrollbar = Scrollbar(self)
            self.scrollbar.pack(side = RIGHT, fill = Y)
            frameheight = 0
            for item in nameidmap.keys():
                frameheight += 46
            self.area = Canvas(self, yscrollcommand=self.scrollbar.set, bg = "#FFFFFF", bd = 0, highlightthickness = 0)
            self.listframe = Frame(self.area, bg = "#FFFFFF", width = 400, height = frameheight)
            self.listframe.pack_propagate(0)
            self.scrollbar.config(command = self.area.yview)
            self.area.pack(fill = BOTH, expand = True)
            self.area.create_window((0, 0), window = self.listframe, anchor = NW)
            self.listframe.bind("<Configure>", lambda event, canvas=self.area: onFrameConfigure(canvas))
            def onScroll(event):
                self.area.yview_scroll(int(-1*(event.delta/60)), "units")
            self.area.bind_all("<MouseWheel>", onScroll)
            self.doexpand()

            for item in nameidmap.keys():            
                ImportOption(self.listframe, item, nameidmap[item]).pack(fill = X, expand = True)
        def doexpand(self):
            parentwidth = self.area.winfo_width()
            self.listframe.config(width = parentwidth)
            self.after(1, self.doexpand)

        
            
            

    def settings():
        global settingsdict
        root = Tk()
        root.config(bg = "#FFFFFF")
        root.geometry(str(int(int(root.winfo_screenwidth()/3))) + "x" + str(int(int(root.winfo_screenheight())/3)))
        root.wm_title("Settings")
        root.iconbitmap("./assets/logo.ico")


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

        searchbarframe = Frame(root, bg = "#FFFFFF")
        searchbarframe.grid_columnconfigure(0, weight = 5)
        searchbarframe.grid_columnconfigure(1, weight = 1)
        searchsettingslbl = Label(searchbarframe, text = "Searchbar settings:", bg = "#FFFFFF")
        searchsettingslbl.grid(column = 0, row = 0, pady = (0, 5), sticky = W)
        showonstartlbl = Label(searchbarframe, text = "        Show search bar when the launcher starts", bg = "#FFFFFF")
        showonstartlbl.grid(column = 0, row = 1, sticky = W)
        showonstartbtn = Checkbox(searchbarframe, settingsdict["searchonstart"])
        showonstartbtn.grid(column = 1, row = 1, sticky = E)
        showpromptlbl = Label(searchbarframe, text = "        Show 'Press enter to search' prompt", bg = "#FFFFFF")
        showpromptlbl.grid(column = 0, row = 2, sticky = W)
        showpromptbtn = Checkbox(searchbarframe, settingsdict["showsearchprompt"])
        showpromptbtn.grid(column = 1, row = 2, sticky = E)
        solidbglbl = Label(searchbarframe, text = "        Make searchbar background solid", bg = "#FFFFFF")
        solidbglbl.grid(column = 0, row = 3, sticky = W)
        solidbgbtn = Checkbox(searchbarframe, settingsdict["solidsearchbg"])
        solidbgbtn.grid(column = 1, row = 3, sticky = E)
        searchbarframe.pack(padx = 20, fill = X)

        steampathstring = StringVar()
        steampathstring.set(settingsdict["steampath"])
        def browseforsteam():
            steampathstring.set(filedialog.askopenfilename(initialdir="C:", title="Browse", filetypes = (("EXE Files","*.exe"),("All Files","*.*"))))
        steamsettingsframe = Frame(root, bg = "#FFFFFF")
        steamsettingsframe.grid_columnconfigure(0, weight = 0)
        steamsettingsframe.grid_columnconfigure(1, weight = 2)
        steamsetingslbl = Label(steamsettingsframe, bg = "#FFFFFF", text = "\nSteam settings:")
        steamsetingslbl.grid(column = 0, row = 0, pady = (0, 5), sticky = W)
        showsteamlbl = Label(steamsettingsframe, bg = "#FFFFFF", text = "        Show Steam button on sidebar")
        showsteamlbl.grid(column = 0, row = 1, sticky = W)
        showsteambtn = Checkbox(steamsettingsframe, settingsdict["showsteambtn"])
        showsteambtn.grid(column = 2, row = 1, sticky = E)
        steampathlbl = Label(steamsettingsframe, bg = "#FFFFFF", text = "        Path to Steam:")
        steampathlbl.grid(column = 0, row = 2, sticky = W)
        steambrowsebox = Entry(steamsettingsframe, textvariable = steampathstring, relief = FLAT, highlightthickness = 1, highlightbackground = "#000000")
        steambrowsebox.grid(column = 1, row = 2, sticky = E+W)
        steambrowsebtn = Button(steamsettingsframe, text = "Browse", command=browseforsteam)
        steambrowsebtn.grid(column = 2, row = 2)
        steamsettingsframe.pack(padx = 20, fill = X)

        baseframe = Frame(root, bg = "#FFFFFF")
        baseframe.pack(side = BOTTOM)

        def opentutorial():
            webbrowser.open("https://spatchy.github.io/Lustrous-Launcher/tutorial")
        tutorialbtn = Button(baseframe, text = "View online help", command = opentutorial)
        tutorialbtn.grid(row = 0, column = 0, padx = 2, pady = 2)

        def update():
            latestrelease = json.loads(urllib.request.urlopen("https://api.github.com/repos/Spatchy/Lustrous-Launcher/releases/latest").read().decode('utf-8'))["tag_name"]
            if int(latestrelease.replace(".","")) > int(VERSION.replace(".","")):
                if messagebox.askyesno("Update Available!", "This version is: {0}\nThe latest release is: {1}\n\nDo you want to launch the updater?".format(VERSION, latestrelease)):
                    if getattr(sys, 'frozen', False):
                        currentdir = os.path.dirname(sys.executable)
                        updateapp = currentdir + "\\llupdate.exe"
                    else:
                        currentdir = os.path.dirname(__file__)
                        updateapp = currentdir + "\\llupdate.pyw"
                    subprocess.Popen(updateapp, shell = True)
                    root.destroy()
            else:
                messagebox.showinfo("Up To Date!", "Lustrous Launcher is up to date!")
        checkupdatebtn = Button(baseframe, text = "Check for updates", command = update)
        checkupdatebtn.grid(row = 0, column = 1, padx = 2, pady = 2)

        baseframe.pack(side = BOTTOM)

        def savesettings():
            settingsdict["searchonstart"] = showonstartbtn.get()
            settingsdict["showsearchprompt"] = showpromptbtn.get()
            settingsdict["solidsearchbg"] = solidbgbtn.get()
            settingsdict["showsteambtn"] = showsteambtn.get()
            settingsdict["steampath"] = steambrowsebox.get()
            
            settingsfile = open("settings.ini", "w")
            firstline = True
            for item in settingsdict: #save settingsdict to file
                filestring = str(item) + "=" + str(settingsdict[item])
                if firstline:
                    settingsfile.write(filestring)
                    firstline = False
                else:
                    settingsfile.write("\n"+filestring)
            settingsfile.close()
            root.destroy()

        root.protocol('WM_DELETE_WINDOW', savesettings)
        
        root.mainloop()

    def addgame(**kwargs):
        root = Tk()
        if kwargs == {}:
            root.wm_title("Add Game")
        else:
            root.wm_title("Edit Game")
                
        root.iconbitmap("./assets/logo.ico")
        root.config(bg = "#FFFFFF")
        root.geometry(str(int(int(root.winfo_screenwidth()/3))) + "x" + str(int(int(root.winfo_screenheight())/3)))

        def importsteam():
            top = Toplevel()
            top.wm_title("Import Steam Library")
            top.iconbitmap("./assets/logo.ico")
            top.config(bg = "#FFFFFF")
            top.geometry(str(int(int(root.winfo_screenwidth()/3))) + "x" + str(int(int(root.winfo_screenheight())/3)))
            top.grab_set()
            
            firstframe = Frame(top, bg = "#FFFFFF")
            libraryframe = Frame(firstframe, bg = "#FFFFFF")
            librarystring = StringVar()
            librarylbl = Label(libraryframe, text = "Library Path: ", width = 15, bg = "#FFFFFF")
            librarybox = Entry(libraryframe, textvariable = librarystring, bg = "#FFFFFF", relief = FLAT, highlightthickness = 1, highlightbackground = "#000000")
            def getpath():
                libraryfolder = filedialog.askdirectory(initialdir = "/",title = "Select Steam Library",)
                librarystring.set(str(libraryfolder))

            librarybtn = Button(libraryframe, text = "Select Steam Library Folder", command = getpath)
            explainlbl = Label(libraryframe, text = "The Steam Library folder should CONTAIN the steamapps folder", bg = "#FFFFFF")
            librarylbl.grid(row = 0, column = 0, sticky = W)
            librarybox.grid(row = 0, column = 1, sticky = E+W)
            librarybtn.grid(row = 0, column = 2, sticky = E)
            explainlbl.grid(row = 1, column = 0, columnspan = 3)
            libraryframe.pack(expand = True, fill = X)
            libraryframe.grid_columnconfigure(1, weight=3)

            def start(): #start import process - generate list of dictionaries of games and their attributes
                firstframe.pack_forget()
                searchinglbl = Label(top, text = "Searching, please wait.\n This may take a while")
                searchinglbl.pack()
                libpath = librarybox.get()+"/steamapps/"
                installedlist = []
                for file in os.listdir(libpath):
                    if file.startswith("appmanifest_"):
                        installedlist.append(file.replace("appmanifest_", "").replace(".acf", ""))
                try:
                    with open(settingsdict["steampath"].replace("Steam.exe", "appcache/appinfo.vdf"), 'rb') as f:
                        data = appinfo.load(f)
                except FileNotFoundError:
                    messagebox.showerror("Error", "Your Steam path seems to be wrong.\nPlease check your settings and try again")
                    top.destroy()
                nameidmap = {}
                for app in installedlist:
                    try:
                        gamename = (data[int(app)]["sections"][b"appinfo"][b"common"][b"name"]).decode("utf-8")
                        gamename = re.sub(r'[^a-zA-Z0-9_ !?#~%@]', '', gamename)
                        nameidmap[app] = gamename
                    except TypeError: #ignore irrelevant unparseable stuff
                        pass
                    except KeyError: #ignore irrelevant unparseable stuff
                        pass


                searchinglbl.pack_forget()
                secondframe.pack()
                usagelbl = Label(top, text = "Do you want to import the following games?", bg = "#FFFFFF")
                usagelbl.pack(fill = X)
                impicker = ImportPicker(top, nameidmap)
                impicker.pack(fill = BOTH, expand = True)
                buttonvar = StringVar()
                buttonvar.set("Complete Import")
                
                def generateimport():
                    x = 1
                    for item in list(reversed(impicker.listframe.pack_slaves())):
                        buttonvar.set("importing game {0}/".format(x)+str(len(list(reversed(impicker.listframe.pack_slaves())))))
                        x+=1
                        if item.checkbox.enabled == "true":
                            try:
                                #download banner
                                urllib.request.urlretrieve("https://steamcdn-a.akamaihd.net/steam/apps/{0}/header.jpg".format(item.appid), "./banners/"+item.appid+".jpg")

                                #create shortcut
                                urlfile = open("./shortcuts/"+item.appid+".url", "w")
                                target = "steam://rungameid/"+item.appid
                                urlfile.write('[InternetShortcut]\n')
                                urlfile.write('URL=%s' % target)
                                urlfile.close()

                                #create game json
                                if getattr(sys, 'frozen', False):
                                    currentdir = os.path.dirname(sys.executable).replace("\\","/")
                                else:
                                    currentdir = os.path.dirname(__file__).replace("\\","/")
                                gamefile = open("./games/"+item.appid+".json", "w")
                                gamestring = (str('{0}: "{1}", "path": "{2}", "bannername": "{3}"{4}').format('{"title"',item.appname, currentdir+"/shortcuts/"+item.appid+".url", item.appid, "}")) #.format causes problems... this was painful
                                gamefile.write(gamestring)
                                gamefile.close()
                            except urllib.error.URLError:
                                messagebox.showerror("Error", "There seems to be something wrong with your internet connection.\nCheck your connection and try again.")
                    if messagebox.showinfo("Success", "Your Steam library was successfully imported"):
                        top.destroy()
                    

                def importthread():
                    thread = threading.Thread(target = generateimport)
                    thread.start()
                completeimportbtn = Button(top, textvariable = buttonvar, command = importthread)
                completeimportbtn.pack(side = BOTTOM, pady = 1)

            def startbuffer():
                try:
                    os.listdir(librarybox.get()+"/steamapps/common")
                    start()
                except FileNotFoundError as e:
                    print(e)
                    messagebox.showerror("Error", "That folder is not a steam library.\nThe folder you select should contain the steamapps folder")

            proceedbtn = Button(firstframe, text = "Begin Import", command = startbuffer)
            proceedbtn.pack(side = BOTTOM)


            firstframe.pack(fill = BOTH)
            secondframe = Frame(top)
            
        steamimportbtn = Button(root, text = "Import Steam library", command = importsteam)
        ormanlbl = Label(root, text = "Or, import a game manually:", bg = "#FFFFFF")
        divframe = Frame(root, bg = "#FFFFFF", highlightthickness = 1, highlightbackground = "#AAAAAA")

        titleframe = Frame(root, bg = "#FFFFFF")
        titlelbl = Label(titleframe, text = "Game Title: ", width = 15, bg = "#FFFFFF")
        titleenter = Entry(titleframe, bg = "#FFFFFF", relief = FLAT, highlightthickness = 1, highlightbackground = "#000000")
        titlelbl.grid(column = 0, row = 0, sticky = W)
        titleenter.grid(column = 1, row = 0, sticky = W+E)
        

        titleframe.grid_columnconfigure(1, weight=3)

        bannerframe = Frame(root, bg = "#FFFFFF")
        bannerlbl = Label(bannerframe, text = "Banner Name: ", width = 15, bg = "#FFFFFF")
        bannerenter = Entry(bannerframe, bg = "#FFFFFF", relief = FLAT, highlightthickness = 1, highlightbackground = "#000000")
        def openbannerfolder():
            if getattr(sys, 'frozen', False):
                currentdir = os.path.dirname(sys.executable)
            else:
                currentdir = os.path.dirname(__file__)
            bannersdir = currentdir + "\\banners"
            subprocess.Popen(["explorer.exe", bannersdir])
        bannerbtn = Button(bannerframe, text = "Open Banner Folder", command = openbannerfolder)
        bannerwarn = Label(bannerframe, text = "Banners must be in the 'banners' folder - DO NOT include path or file extension\nAll banners must be 460x215px and can be in any common image format (PNG recommended)", bg = "#FFFFFF")
        bannerlbl.grid(row = 0, column = 0, sticky = W)
        bannerenter.grid(row = 0, column = 1, sticky = E+W)
        bannerbtn.grid(row = 0, column = 2, sticky = E)
        bannerwarn.grid(row = 1, column = 0, columnspan = 3)

        bannerframe.grid_columnconfigure(1, weight=3)
        
        pathframe = Frame(root, bg = "#FFFFFF")
        pathstring = StringVar()
        pathlbl = Label(pathframe, text = "Path To Game: ", width = 15, bg = "#FFFFFF")
        pathbox = Entry(pathframe, textvariable = pathstring, bg = "#FFFFFF", relief = FLAT, highlightthickness = 1, highlightbackground = "#000000")
        def getpath():
            gamefile = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("EXE Files","*.exe"),("Shortcuts","*.lnk"),("Steam Internet Shortcut","*.url")))
            pathstring.set(str(gamefile))

        pathbtn = Button(pathframe, text = "Choose Game Path", command = getpath)
        pathlbl.grid(row = 0, column = 0)
        pathbox.grid(row = 0, column = 1, sticky = E+W)
        pathbtn.grid(row = 0, column = 2)
        

        pathframe.grid_columnconfigure(1, weight=3)

        def savegame(doask):
            jsondict = {}
            jsondict["title"] = titleenter.get()
            jsondict["path"] = pathbox.get()
            jsondict["bannername"] = bannerenter.get()
            jsonfile = open("./games/" + titleenter.get() + ".json","w")
            jsonfile.write(str(jsondict).replace("'",'"'))
            if doask:
                if messagebox.askyesno("Done!", "Would you like to add another game?"):
                    titleenter.delete(0, END)
                    pathbox.delete(0, END)
                    bannerenter.delete(0, END)
                else:
                    root.destroy()
            else:
                root.destroy()

        savebtn = Button(root, text = "Add Game To Launcher", command = lambda: savegame(True))
        savebtn.pack(side = BOTTOM)
        
        if kwargs == {}:
            steamimportbtn.pack(side = TOP)
        else:
            titleenter.insert(0, kwargs["target"].title)
            bannerenter.insert(0, kwargs["target"].bannername.replace("./banners\\","").split(".")[0])
            pathbox.insert(0, kwargs["target"].path)
            savebtn.config(text = "Save Changes", command = lambda: savegame(False))
            def removegame():
                if messagebox.askokcancel("Delete Game", "This will remove " + kwargs["target"].title + " from Lustrous Launcher.\nThis cannot be undone."):
                    try:
                        os.remove("./games/"+kwargs["target"].jsonfile)
                        messagebox.showinfo("Success", "The game was removed successfully")
                        root.destroy()
                    except FileNotFoundError:
                        messagebox.showerror("Error", "The game seems to have already been deleted")
            removegamebtn = Button(root, text = "Remove Game", command = removegame)
            removegamebtn.pack()
        divframe.pack(expand = True, fill = X, padx = 30)
        if kwargs == {}:
            ormanlbl.pack()
        titleframe.pack(expand = True, fill = X)
        bannerframe.pack(expand = True, fill = X)
        pathframe.pack(expand = True, fill = X)
    
        root.mainloop()

    def opensteam():
        steampath = settingsdict["steampath"]
        subprocess.Popen(steampath, shell = True)
        

    if exitcode == 1:
        settings()
    elif exitcode == 2:
        addgame()
    elif exitcode == 3:
        opensteam()
    elif type(exitcode) is Gamelink:
        addgame(target = exitcode)
