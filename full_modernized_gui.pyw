
 # import textToWord
import docx, os, time, re
from docx.shared import Pt
import createfile
import WordSongUpdater as SongUpdater
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as TkFont
from tkinter import Button
import scanningDir as SD
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tbs
from ttkbootstrap.constants import *
# from multiprocessing import Process
# from multiprocessing import Pool


class ModernSongManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Master Of Song Organization (MOSO)")
        self.master.geometry("1280x720")
        
        # Use ttkbootstrap for a modern look
        self.style = tbs.Style(theme="darkly")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Top frame for input and radio buttons
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=X, pady=(0, 20))
        
        # Song number input
        ttk.Label(top_frame, text="Song Num:", font=("Roboto", 14)).pack(side=LEFT, padx=(0, 10))
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(top_frame, textvariable=self.entry_var, width=20, font=("Roboto", 14))
        self.entry.pack(side=LEFT, padx=(0, 20))
        
        # Database selection
        self.radio_var = tk.StringVar()
        ttk.Radiobutton(top_frame, text="Old", variable=self.radio_var, value="o", style="TRadiobutton").pack(side=LEFT, padx=(0, 10))
        ttk.Radiobutton(top_frame, text="New", variable=self.radio_var, value="n", style="TRadiobutton").pack(side=LEFT, padx=(0, 20))
        
        # Release date selection
        self.day_var = tk.StringVar()
        ttk.Radiobutton(top_frame, text="Tues/Thurs", variable=self.day_var, value="Tuesday", style="TRadiobutton").pack(side=LEFT, padx=(0, 10))
        ttk.Radiobutton(top_frame, text="None", variable=self.day_var, value=None, style="TRadiobutton").pack(side=LEFT, padx=(0, 10))
        ttk.Radiobutton(top_frame, text="Sun/Porc", variable=self.day_var, value="Sunday", style="TRadiobutton").pack(side=LEFT)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=X, pady=(0, 20))
        
        # Action buttons
        ttk.Button(buttons_frame, text="Add Song", command=self.add_song, style="success.TButton").pack(side=LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Delete Song", command=self.delete_song, style="danger.TButton").pack(side=LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Edit Song", command=self.edit_song, style="info.TButton").pack(side=LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Move Up", command=self.move_up, style="warning.TButton").pack(side=LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Move Down", command=self.move_down, style="warning.TButton").pack(side=LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Clear Songs", command=self.clr_listbox, style="secondary.TButton").pack(side=LEFT, padx=(0, 10))
        
        # Additional action buttons
        ttk.Button(buttons_frame, text="Create File", command=self.create_File, style="primary.TButton").pack(side=LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Compatibility", command=self.Compatibility, style="primary.TButton").pack(side=LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Possible Songs", command=self.viewPosSongs, style="primary.TButton").pack(side=LEFT, padx=(0, 10))
        
        # Listbox frame
        self.listbox_frame = ttk.Frame(main_frame)
        self.listbox_frame.pack(fill=BOTH, expand=YES)
        
        # Using the  originalself.listbox
        self.listbox = tk.Listbox(self.listbox_frame, width=25, height=18, font=("Roboto", 14))
        self.listbox.pack(side=LEFT, fill=BOTH, expand=YES)
        
        # Scrollbar  forself.listbox
        scrollbar = ttk.Scrollbar(self.listbox_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Database updater frame
        updater_frame = ttk.Frame(main_frame)
        updater_frame.pack(fill=X, pady=(20, 0))
        
        ttk.Label(updater_frame, text="Database Updater:", font=("Roboto", 14)).pack(side=LEFT, padx=(0, 10))
        ttk.Button(updater_frame, text="Select file to update", command=self.ChooseFile, style="outline.info.TButton").pack(side=LEFT)
        
        # Bind events
        self.master.bind("<Return>", self.add_song)
        self.master.bind("<Delete>", self.delete_song)
        self.master.bind("<BackSpace>", self.delete_song)
            

        listy = []

    def add_song(self,event=None):
        song_num = self.entry_var.get()
        bookType = self.radio_var.get()
        if song_num == "" or bookType == "":
            if song_num == "" and (bookType == 'n' or bookType == 'o'):
                messagebox.showerror("Error", "Please enter a song number")
            elif bookType == "" and song_num != "":
                messagebox.showerror("Error", "Please choose a database")
            else:
                messagebox.showerror("Error", "Please enter a song number and choose a database")
        else:
            if 'n' in bookType: bookType = 'New'
            else: bookType = 'Old'
            dupSong = SD.songChecker(songNum=song_num,book=bookType)
            print(dupSong)
            if dupSong: # get value and if used then ask if they wish to continue
                errMes = messagebox.askyesno("Error: That song was used before in the last 3 months",
                                            "Do you wish to proceed with this song {}\nFilename/Date: {}".format(song_num + " " + bookType, dupSong[1])#SD.getSongDate(songNum=song_num,book=bookType))
                                            )
                if errMes:
                    if 'New' in bookType: bookType = 'n'
                    else: bookType = 'o'                
                    self.listbox.insert(tk.END, f"{song_num} ({bookType})")
                    self.entry.delete(0, tk.END)
                else:
                    self.entry.delete(0, tk.END)
            else:
                if 'New' in bookType: bookType = 'n'
                else: bookType = 'o'
                self.listbox.insert(tk.END, f"{song_num} ({bookType})")
                self.entry.delete(0, tk.END)

    def edit_song(self):
        curr_selection = self.listbox.curselection()
        if not curr_selection:
            messagebox.showerror("Error", "Please select a song to edit")
        else:
            curr_song = self.listbox.get(curr_selection)
            song_num, property = curr_song.split(" (")
            property = property[0]
            self.entry.delete(0, tk.END)
            self.entry.insert(0, song_num)
            self.radio_var.set(property)
            self.listbox.delete(curr_selection)
            # update_indexes()

    def delete_song(self,event=None):
        curr_selection = self.listbox.curselection()
        if not curr_selection:
            messagebox.showerror("Error", "Please select a song to delete")
        else:
            self.listbox.delete(curr_selection)

    def move_up(self):
        curr_selection = self.listbox.curselection()
        if not curr_selection:
            messagebox.showerror("Error", "Please select a song to move")
        elif curr_selection[0] == 0:
            messagebox.showinfo("Info", "Song is already at the top")
        else:
            curr_song = self.listbox.get(curr_selection)
            self.listbox.delete(curr_selection)
            self.listbox.insert(curr_selection[0]-1, curr_song)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.activate(curr_selection[0]-1)
            self.listbox.selection_set(curr_selection[0]-1, last=None)
            # update_indexes()

    def move_down(self):
        curr_selection = self.listbox.curselection()
        if not curr_selection:
            messagebox.showerror("Error", "Please select a song to move")
        elif curr_selection[0] == self.listbox.size()-1:
            messagebox.showinfo("Info", "Song is already at the bottom")
        else:
            curr_song = self.listbox.get(curr_selection)
            self.listbox.delete(curr_selection)
            self.listbox.insert(curr_selection[0]+1, curr_song)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.activate(curr_selection[0]+1)
            self.listbox.selection_set(curr_selection[0]+1, last=None)
            # update_indexes()

    def clr_listbox(self):
        self.listbox.delete(first=0,last=self.listbox.size())
        self.listy.clear()

    def viewPosSongs(self):
        songsList = self.listbox.get(0, tk.END)
            #Sort out the old and new, and all numbers
        book = []
        for x in songsList:
            book.append(re.findall("(o|n)", x)[0])
        songNum = []
        for i in songsList:
            songNum.append(re.findall("\S[0-9][0-9]?|[0-9]",i)[0])

        posibleSongsList = createfile.getPosibleSongs(songNum, book)
        viewWin = tk.Tk()
        # viewWin.geometry("280x435")
        viewWin.geometry("480x200")
        viewWin.columnconfigure(1,weight=1)    #confiugures column 1 to stretch with a scaler of 1.
        viewWin.rowconfigure(0,weight=1)       #confiugures row 0 to stretch with a scaler of 1.
        viewWin.title("Found Songs")
        posibleSongs = tk.Listbox(viewWin)
        posibleSongs.grid(row=0, column=1,sticky='nsew')
        # posibleSongs.config(width=25, height=18, font=myFont)
        for fv in posibleSongsList:
            posibleSongs.insert(tk.END,fv)
        posibleSongsList.clear()

    def create_File(self):
        print("Firing up databases...")
        ##Used to determine which file path to save to
        user = os.environ.get("USERNAME")
        songsList = self.listbox.get(0, tk.END)

        #Sort out the old and new, and all numbers
        book = []
        for x in songsList:
            book.append(re.findall("(o|n)", x)[0])
        songNum = []
        for i in songsList:
            songNum.append(re.findall("\S[0-9][0-9]?|[0-9]",i)[0])
        print("Downloading songs...")
        #Now send cmd to make file
        fail = False
        try:    my_doc = createfile.getPcSongs(songNum, book, user)
        except BaseException as err:
            fail = True
            messagebox.showerror(err,str(err))
        
        print("Adjusting for readability....")
        font = my_doc.styles['Normal'].font
        font.name = 'Arial'
        font.size = Pt(22)
        print("it is done")
        
        #gets date and time
        month = time.strftime('%m')
        year = time.strftime('%y')
        fullYear = time.strftime('%Y')
        day = time.strftime('%d')

        #checks if path exists if not makes one
        if os.path.exists("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear):
            if self.day_var.get() == "Sunday":
                my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + "PORC_PORC.docx")
                quit(root.mainloop())
            if self.day_var.get() == "Tuesday":
                my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + ".docx")
            else:
                my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + "TESTSAVE.docx")
        else:
            os.mkdir("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear)
            if self.day_var.get() == "Sunday":
                my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + "PORC_PORC.docx")
            if self.day_var.get() == "Tuesday":
                my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + ".docx")
            else:
                my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + "TESTSAVE.docx")
        import scanningDir
        try:
            scanningDir.findNewFiles()
        except:
            messagebox.showerror("File Open","A word doc is probably open, please close it and then try to create the file.")

    def ChooseFile(self):
        from tkinter import filedialog as fd
        filetypes = ( ('word doc', '*.docx'), ('All files', '*.*') )
        input_filename = None
        input_filename = fd.askopenfilename(
                            title='Open a file',
                            initialdir='C:/Users/{}/OneDrive/Երգեր'.format(os.environ.get("USERNAME")),
                            filetypes=filetypes)
        # Possibly throw a window to double check if it really is the file you want
        if input_filename != None:
            message= messagebox.askyesno("MOSO is asking:","Do you wish to update this file: " + input_filename + "\n\nYes to cont., No to stop")
            print(message)
            if message == "yes" or message == True:
                SongUpdater.getDocTextAndIndentation(input_filename)
            # elif message == False:
            #     ChooseFile()
            else:
                print("Closing window")

    def Compatibility(self):
        song_num = self.entry.get()
        bookType = self.radio_var.get()
        myFont = TkFont.Font(family="Arial", size=18)
        import threading as th

        def clicked(event=None): #curselection give the index of the thing clicked, in a tuple ie:(10,)
            MS_WORD = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
            index = PastSongsListbox.curselection()[0]
            selected_item = PastSongsListbox.get(index)
            PastSongsListbox.activate(index)
            Path = ""
            if 'Filename' in selected_item: #if filename is clicked THEN open Word
                Path = selected_item.split(": ")[1]#Should be mm.dd.yy.docx
                for attr in pastSongs:
                    if Path in attr['Filename/Date']:
                        basePth = "C:/Users/{}/OneDrive/".format(os.environ.get("USERNAME"))+attr['basePath']                    
                wordDocThread = th.Thread(target=openWord,args=[MS_WORD,basePth+"/"+Path])
                wordDocThread.start()
                # wordDocThread.run()
                
        def openWord(MS_WORD,path):
            import subprocess
            subprocess.run([MS_WORD,path])
            
        if song_num == "" or bookType == "":
            if song_num == "" and (bookType == 'n' or bookType == 'o'):
                messagebox.showerror("Error", "Please enter a song number")
            elif bookType == "" and song_num != "":
                messagebox.showerror("Error", "Please choose a database")
            else:
                messagebox.showerror("Error", "Please enter a song number and choose a database")
        else:
            if self.radio_var.get() == 'n':
                bookType = "New"
            else:
                bookType = "Old"
                
            pastSongs=SD.songSearch(song_num, bookType)
            if pastSongs:
                # messagebox.showinfo(title="Compatability Chart",message="Filename/Date:"+pastSongs["Filename/Date"])
                windowListSize = len(pastSongs)
                viewWin = tk.Tk()
                viewWin.geometry("280x{}".format(260*windowListSize))
                viewWin.title("Past Songs")
                viewWin.columnconfigure(1,weight=1)    #confiugures column 1 to stretch with a scaler of 1.
                viewWin.rowconfigure(0,weight=1)       #confiugures row 0 to stretch with a scaler of 1.
                viewWin.bind("<Button-1>",clicked)
                viewWin.bind("<Return>",clicked)
                PastSongsListbox = tk.Listbox(viewWin)
                PastSongsListbox.grid(row=0, column=1,sticky='nsew')
                PastSongsListbox.config(width=25, height=18, font=myFont)
                
                for attr in pastSongs:
                    filename = attr['Filename/Date']
                    folderPath = attr['basePath']
                    PastSongsListbox.insert(tk.END,"Folder: " + folderPath)
                    PastSongsListbox.insert(tk.END,"Filename/Date: " + filename)
                    PastSongsListbox.insert(tk.END,"\nSongs:")
                    for song in attr['songs']:
                        PastSongsListbox.insert(tk.END,song) #making a list allows me to dodge the edge cases of song search results
                
            else:
                messagebox.showinfo(title="Compatability Chart",message=f"Song number: {song_num} in Book: {bookType} not found.")


if __name__ == "__main__":
    root = tbs.Window(themename="darkly")
    app = ModernSongManager(root)
    root.mainloop()