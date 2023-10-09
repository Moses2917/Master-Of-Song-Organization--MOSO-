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
from multiprocessing import Process
from multiprocessing import Pool

listy = []

def add_songWIP():
    song_num = entry.get()
    property = radio_var.get()
    if song_num == "" or property == "":
        messagebox.showerror("Error", "Please enter a song number and choose a property")
    else:
        listbox.delete(first=0,last=listbox.size()) ##Clears listbox
        listy.append(f"{song_num} ({property})")
        # listbox.insert(tk.END, f"{song_num} ({property})")
        # entry.delete(0, tk.END)
        for number, letter in enumerate(listy):
            # clr_listbox()
            song_num = re.findall("[0-9][0-9][0-9]",letter)[0] #CAN"T PROCESS 22 for some reason fix it
            property = re.findall("(o|n)", letter)[0]
            listbox.insert(tk.END, str(number+1) + "." + f"{song_num} ({property})")
            # listbox.insert(tk.END, str(number+1) + "." + f"{song_num} ({property})")
            entry.delete(0, tk.END)
            
def add_song():
    song_num = entry.get()
    property = radio_var.get()
    if song_num == "" or property == "":
        messagebox.showerror("Error", "Please enter a song number and choose a property")
    else:
        if 'n' in property: property = 'New'
        else: property = 'Old'
        dupSong = SD.songChecker(songNum=song_num,book=property)
        print(dupSong)
        if dupSong: # get value and if used then ask if they wish to continue
            errMes = messagebox.askyesno("Error: That song was used before in the last 3 months","Do you wish to proced with this song {}".format(song_num + " " + property))
            if errMes:
                listbox.insert(tk.END, f"{song_num} ({property})")
                entry.delete(0, tk.END)
            else:
                entry.delete(0, tk.END)
        else:
            if 'New' in property: property = 'n'
            else: property = 'o'
            listbox.insert(tk.END, f"{song_num} ({property})")
            entry.delete(0, tk.END)

def edit_song():
    curr_selection = listbox.curselection()
    if not curr_selection:
        messagebox.showerror("Error", "Please select a song to edit")
    else:
        curr_song = listbox.get(curr_selection)
        song_num, property = curr_song.split(" (")
        property = property[0]
        entry.delete(0, tk.END)
        entry.insert(0, song_num)
        radio_var.set(property)
        listbox.delete(curr_selection)
        # update_indexes()

def delete_song():
    curr_selection = listbox.curselection()
    if not curr_selection:
        messagebox.showerror("Error", "Please select a song to delete")
    else:
        listbox.delete(curr_selection)

def move_up():
    curr_selection = listbox.curselection()
    if not curr_selection:
        messagebox.showerror("Error", "Please select a song to move")
    elif curr_selection[0] == 0:
        messagebox.showinfo("Info", "Song is already at the top")
    else:
        curr_song = listbox.get(curr_selection)
        listbox.delete(curr_selection)
        listbox.insert(curr_selection[0]-1, curr_song)
        listbox.selection_clear(0, tk.END)
        listbox.activate(curr_selection[0]-1)
        listbox.selection_set(curr_selection[0]-1, last=None)
        # update_indexes()

def move_down():
    curr_selection = listbox.curselection()
    if not curr_selection:
        messagebox.showerror("Error", "Please select a song to move")
    elif curr_selection[0] == listbox.size()-1:
        messagebox.showinfo("Info", "Song is already at the bottom")
    else:
        curr_song = listbox.get(curr_selection)
        listbox.delete(curr_selection)
        listbox.insert(curr_selection[0]+1, curr_song)
        listbox.selection_clear(0, tk.END)
        listbox.activate(curr_selection[0]+1)
        listbox.selection_set(curr_selection[0]+1, last=None)
        # update_indexes()

def clr_listbox():
    listbox.delete(first=0,last=listbox.size())
    listy.clear()

def viewPosSongs():
    songsList = listbox.get(0, tk.END)
        #Sort out the old and new, and all numbers
    book = []
    for x in songsList:
        book.append(re.findall("(o|n)", x)[0])
    songNum = []
    for i in songsList:
        songNum.append(re.findall("\S[0-9][0-9]?|[0-9]",i)[0])

    posibleSongsList = createfile.getPosibleSongs(songNum, book)
    viewWin = tk.Tk()
    viewWin.geometry("280x435")
    viewWin.title("Found Songs")
    posibleSongs = tk.Listbox(viewWin)
    posibleSongs.grid(row=0, column=1)
    posibleSongs.config(width=25, height=18, font=myFont)
    for fv in posibleSongsList:
        posibleSongs.insert(tk.END,fv)
    posibleSongsList.clear()

def create_File():
    print("Firing up databases...")
    ##Used to determine which file path to save to
    user = ""
    if os.path.exists("C:/Users/moses/"):
        user = "moses"
    else:
        user = "Armne"
    songsList = listbox.get(0, tk.END)

    #Sort out the old and new, and all numbers
    book = []
    for x in songsList:
        book.append(re.findall("(o|n)", x)[0])
    songNum = []
    for i in songsList:
        songNum.append(re.findall("\S[0-9][0-9]?|[0-9]",i)[0])
    print("Downloading songs...")
    #Now send cmd to make file
    my_doc = createfile.getPcSongs(songNum, book, user)
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
        if day_var.get() == "Sunday":
            my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + "PORC_PORC.docx")
            quit(root.mainloop())
        if day_var.get() == "Tuesday":
               my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + ".docx")
        else:
            my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + "TESTSAVE.docx")
    else:
        os.mkdir("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear)
        if day_var.get() == "Sunday":
            my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + "PORC_PORC.docx")
        if day_var.get() == "Tuesday":
               my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + ".docx")
        else:
            my_doc.save("C:/Users/" + user + "/OneDrive/Երգեր/" + month + "." + fullYear + "/" + month + "." + day + "." + year + "TESTSAVE.docx")

def ChooseFile():
    from tkinter import filedialog as fd
    filetypes = ( ('word doc', '*.docx'), ('All files', '*.*') )
    input_filename = None
    input_filename = fd.askopenfilename(
                        title='Open a file',
                        initialdir='C:/Users/{}/OneDrive/Երգեր'.format(os.environ.get("USERNAME")),
                        filetypes=filetypes)
    # Possibly throw a window to double check if it really is the file you want
    if input_filename != None:
        message= messagebox.askyesnocancel("MOSO is asking:","Do you wish to update this file: " + input_filename + "\n\nYes to cont., No to start again, Cancel to stop")
        print(message)
        if message == "yes" or message == True:
            SongUpdater.getDocTextAndIndentation(input_filename)
        elif message == False:
            ChooseFile()
        else:
            print("Closing window")
        
def SongCheck():
    viewWin = tk.Tk()
    viewWin.geometry("512x256")
    viewWin.title("Song Checker")

def screen():
    root = tk.Tk()
    style = ttk.Style()
    root.title("Master Of Song Organization (MOSO)") #Old Title: "Song Manager"
    root.geometry("1099x720")

    txtbox_font = TkFont.Font(family="Tahoma", size=18)

    label = tk.Label(root, text="Song Num:", font=txtbox_font)
    label.grid(row=0, column=4)

    entry_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=entry_var, width=50)
    entry.grid(row=0, column=5, pady=10)


    tickBox_font = TkFont.Font(family="Arial", size=15)

    radio_var = tk.StringVar()
    tk.Radiobutton(root, text="Old", variable=radio_var, value="o",font=tickBox_font, relief="raised", bg="#0000a0", fg="#f9d4b8", bd=8).grid(row=2, column=4)
    tk.Radiobutton(root, text="New", variable=radio_var, value="n",font=tickBox_font, relief="raised", bg="#741a1c", fg="#ffce00", bd=8).grid(row=2, column=5)

    day_var = tk.StringVar()
    tk.Radiobutton(root, text="Tues/Thurs", variable=day_var, value="Tuesday", font=tickBox_font, relief="raised", bd=8).grid(row=3, column=4, padx=10)
    tk.Radiobutton(root, text="None", variable=day_var, value=None, font=tickBox_font, relief="raised", bd=8).grid(row=3, column=4,columnspan=5)
    tk.Radiobutton(root, text="Sun/Porc", variable=day_var, value="Sunday",font=tickBox_font, relief="raised", bd=8).grid(row=3, column=6)


    create_File_Button = Button(root, text="Create File", relief="raised", bg="#0000a0", fg='#FFC107', bd=5, padx=10, pady=10, font=('Arial', 15), command=create_File)
    create_File_Button.grid(row=1, column=2)

    PosisbleSongs = Button(root, text="Possible Songs", relief="raised", bg="#0000a0", fg='#FFC107', bd=5, pady=10, font=('Arial', 15), command=viewPosSongs)
    PosisbleSongs.grid(row=1, column=1)

    # SongChecker = Button(root, text="SongChecker", relief="raised", bg="#0000a0", fg='#FFC107', bd=5, pady=10, font=('Arial', 15), command=SongCheck)
    # SongChecker.grid(row=1, column=0)

    add_button = Button(root, text="Add Song", relief="raised", bg="#741a1c", fg='#FFC107', bd=5, padx=22, pady=10, font=('Arial', 15), command=add_song)
    add_button.grid(row=2, column=2)


    BGroupRow = 3
    BGroupCol = 0

    delete_button = Button(root, text="Delete Song", bg='#741a1c', fg='#FFC107', font=('Arial', 15), command=delete_song, padx=10, pady=10, bd=5, relief="raised")
    delete_button.grid(row=2, column=1)

    edit_button = Button(root, text="Edit Song", bg='#741a1c', fg='#FFC107', font=('Arial', 15), command=edit_song,padx=10, pady=10, bd=5, relief="raised")
    edit_button.grid(row=2, column=0)

    move_up_button = Button(root, text="Move Up", fg='#cc0000', font=('Arial', 15), command=move_up, padx=13, pady=10, bd=5, relief="raised")
    move_up_button.grid(row=BGroupRow, column=BGroupCol,sticky='ew')

    move_down_button = Button(root, text="Move Down", fg='#cc0000', font=('Arial', 15), command=move_down, padx=10, pady=10, bd=5, relief="raised")
    move_down_button.grid(row=BGroupRow, column=BGroupCol+1)

    clr_button = Button(root, text="Clear Songs", fg='#cc0000', font=('Arial', 15), command=clr_listbox, padx=10, pady=10, bd=5, relief="raised")
    clr_button.grid(row=BGroupRow, column=BGroupCol+2)


    Update_Label = tk.Label(root, text="Song Updater:", font=txtbox_font,bg='#741a1c', fg='#FFC107', padx=20)
    Update_Label.grid(row=6, column=1)
    openFile = Button(root, text="Select file to update", command=ChooseFile)
    openFile.grid(row=7, column=1)


    #create size 22 font, arial
    myFont = TkFont.Font(family="Arial", size=18)

    listbox = tk.Listbox(root)
    listbox.grid(row=10, column=5)
    listbox.config(width=25, height=18, font=myFont)

    # listbox.bind("<<ListboxSelect>>", update_indexes)

    root.mainloop()

##Notes:
#Add song updater, that  can pick any date and analyize the song and display it in the listbox

if __name__ == "__main__":
    processes = []

    RecentSongs = Process(target=SD.getAllNums)
    processes.append(RecentSongs)
    RecentSongs.start()
    MOSO = Process(target=screen)
    MOSO.start()
    processes.append(MOSO)

    for process in processes:
        process.join()