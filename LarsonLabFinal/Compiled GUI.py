#Compiled GUI.py
#Programmer: Garrett E. Tisdale

#Imports
import ttk
import sys
import csv
import shutil
import string
import codecs
import fnmatch
import matplotlib
import xlsxwriter
import subprocess
import numpy as np
import os, fnmatch
import pandas as pd
import Tkinter as tk
from Tkinter import *
import matplotlib as mp
import tkMessageBox as tmb
from ScrolledText import *
from shutil import copyfile
from Tkinter import StringVar
import matplotlib.pyplot as plt
from ttk import Frame, Button, Style


#Style for MatPlotLib graphs
matplotlib.use("TkAgg")

#Fonts for GUI
LARGE_FONT = ("Verdana", 18)
NORM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 10)


#Continously updated global values for assigning burst
combind_burst_num = 0
data_set_number = 1


#Continously updated global values for locating files
test_file = ''
path_entry = ''
selection_list = []
trk_list = []
trk_list_ordered = []
end_list = []
tempsave1 = [0]
tempsave2 = [0]
csv_list = []

#Dictionary for converting letters to numbers a=1, b=2, c=3, etc.
di=dict(zip(string.letters,[ord(c)%32 for c in string.letters]))


#Default message for unused parts of the GUI that could be used in the future
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


#Creates the labels for the right click options in the GUI
def make_menu(w):
    global copy_paste_menu
    copy_paste_menu = Menu(w, tearoff=0)
    copy_paste_menu.add_command(label="Cut")
    copy_paste_menu.add_command(label="Copy")
    copy_paste_menu.add_command(label="Paste")


#Displays the right click options in the GUI
def show_menu(e):
    w = e.widget
    copy_paste_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    copy_paste_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    copy_paste_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    copy_paste_menu.tk.call("tk_popup", copy_paste_menu, e.x_root, e.y_root)


#Core of the GUI
#This is the main class under which all other GUI pages/classes must be placed
class MainGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        #Activates and initializes assigned values to tkinter GUI
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Clustering Program")
        containter = tk.Frame(self)
        containter.pack(side="top", fill="both", expand=True)
        containter.grid_rowconfigure(0, weight=1)
        containter.grid_columnconfigure(0, weight=1)

        #The menu bar located at the top of the GUI
        #Currently not in significant use
        menubar = tk.Menu(containter)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Option for future development. Not in use."))

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)


        #Location for adding new pages to the GUI
        #These pieses of code continously update the pages under the main GUI
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            frame = F(containter, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    #Brings the desired page to the front to view while interacting with the GUI
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


#The very first page displayed when opening the GUI
#The main content of the GUI is located here; that being extracting the bursts 
#from the data sets
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        #Initializes tkinter window
        tk.Frame.__init__(self, parent)
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        
        #The title and location of the page
        label = tk.Label(frame, text="Create Burst Matrix", font=LARGE_FONT)
        label.pack(anchor='center', padx=5, pady=5)
        self.pack(fill=BOTH, expand=True)
        
        #Two subframes used for viewing which data sets are being analyzed
        #These two frames hold scroll bars
        frame1 = Frame(frame, relief=GROOVE, width=530, height=548, borderwidth=1)
        frame2 = Frame(frame, relief=GROOVE, width=530, height=100, borderwidth=1)

        #Page dictionary for holding infomation about the data sets being analyzed
        d = {}

        #Assigns place holders for the data sets such that the scroll bar will 
        #work when the data sets are updated
        def data():
            for i in range(1000):
                Label(frame4, text=i + 1).grid(row=i + 1, column=0)
                d["Label{0}".format(i + 1)] = Label(frame4, text="FILE NAME " + str(i + 1))
                d["Label" + str(i + 1)].grid(row=i + 1, column=1, sticky=W)

        #Configures the scroll bar canvases for the frames
        def ConfigCanvas1(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=530, height=540)

        def ConfigCanvas2(event):
            canvas2.configure(scrollregion=canvas.bbox("all"), width=530, height=540)


        #Labels for the entry fields in the page
        Path_label = Label(frame, text='Enter Path', font=NORM_FONT)
        test_file_name_label = Label(frame, text='Test File Name', font=NORM_FONT)
        select_file_name_label = Label(frame, text='Select Regions', font=NORM_FONT)

        #Entry fields for the various inputs
        Path_Entry = Entry(frame)
        test_file_name_Entry = Entry(frame)
        select_file_name_Entry = Entry(frame)

        #Placing the entries and labels
        Path_label.place(x=100, y=45)
        Path_Entry.place(width=490,x=100, y=69)
        
        test_file_name_label.place(x=600, y=45)
        test_file_name_Entry.place(width=250, x=600, y=69)
        
        select_file_name_label.place(x=860, y=45)
        select_file_name_Entry.place(x=860, y=69)
        
        #Text box that updates when selection for the test filename is active
        text_box1 = Text(frame, wrap=WORD, width=45, height=20)
        text_box1.place(width=200, height=20, x=994, y=69)
    
        #Placing frames and features for viewing what data sets are active
        frame1.place(x=100, y=100)
        canvas2 = Canvas(frame1)
        frame3 = Frame(canvas2)
        myscrollbar = Scrollbar(frame1, orient="vertical", command=canvas2.yview)
        canvas2.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="left", fill=BOTH)
        canvas2.pack(side="left")
        canvas2.create_window((0, 0), window=frame3, anchor='nw')
        frame3.bind("<Configure>", ConfigCanvas2)

        frame2.place(x=640, y=100)
        canvas = Canvas(frame2)
        frame4 = Frame(canvas)
        myscrollbar = Scrollbar(frame2, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right", fill="y")
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=frame4, anchor='nw')
        frame4.bind("<Configure>", ConfigCanvas1)


        #Labels to be placed inside the frames for viewing what data sets are active
        Label(frame3, text='Entry').grid(row=0, column=0, sticky=W)
        Label(frame3, text='Name of Experiment').grid(row=0, column=1, sticky=W)

        Label(frame4, text='Entry').grid(row=0, column=0, sticky=W)
        Label(frame4, text='Name of File').grid(row=0, column=1, sticky=W)


        #Check buttons for deciding if the said tasks should be processed
        var1 = IntVar()
        traceCheckButton = Checkbutton(frame, text="Save Individual Traces as Pictures", variable=var1)
        traceCheckButton.place(x=990, y=0)

        var2 = IntVar()
        picturesCheckButton = Checkbutton(frame, text="Save Individual Burst as Pictures", variable=var2)
        picturesCheckButton.place(x=990, y=20)

        var3 = IntVar()
        letterToNumber = Checkbutton(frame, text="Second Indicator Convert Letter to Number", variable=var3)
        letterToNumber.place(x=990, y=40)

    
        #Assigning place holders to data viewing frames
        data()


        #Retrieves test_file_name_Entry and saves as global value
        def TestFileName_Entry_Get():
            global test_file
            if test_file_name_Entry.get() != '':
                test_file = test_file_name_Entry.get().strip()
                print test_file
                

        #Retrieves select_file_name_Entry and saves as global value
        #Also updates text box to show what regions were selected in the test file 
        def TestRegion_Entry_Get():
            global test_file
            global selection_list
            global combind_burst_num
            if select_file_name_Entry.get() != '':
                selection_list = []
                instance1 = select_file_name_Entry.get()
                instance2 = instance1.replace('(', '').replace(')', '').split(',')
                for i in range(0,len(instance2)):
                    if i % 2:
                        selection_list.append([int(instance2[i-1]),int(instance2[i])])
                
                temp_list = []
                
                for i in range(0, len(selection_list)):
                    range1 = selection_list[i][0]
                    range2 = selection_list[i][1]
                    
                    print test_file[range1:range2]

                    if i == 1:
                        if var3.get() == 1:
                            temp_list.append(str(di[test_file[range1:range2]]))
                        else:
                            temp_list.append(str(re.sub('[^0-9]', '', test_file[range1:range2])))
                    else:
                        temp_list.append(str(re.sub('[^0-9]', '', test_file[range1:range2])))

                text_box1.delete('1.0', END)
                
                temp = ''
                
                for i in range(0,len(temp_list)):
                    temp = temp+temp_list[i]
                    if i == 0:
                        temp = temp + '.'
                
                text_box1.insert(INSERT, temp)
                

        #Retrieves Path_Entry and saves as global value
        def Path_Entry_Get():
            global path_entry
            if Path_Entry.get() != '':
                path_entry = Path_Entry.get()
                print path_entry
        

        #Extracts and creates the burst data
        def Print_Entry():
            global trk_list
            global trk_list_ordered
            global path_entry
            global data_set_number
            global combind_burst_num
            global tempsave1
            global tempsave2
            global csv_list

            if Path_Entry.get() != '':
                path_entry = path_entry[:-2] + path_entry[-2:].strip()

                #Lists that the files in the designated path will go into
                trk_list = []
                trk_list_ordered = []
                forward = True

                #Creates a slash designated for the fileing system of your platform
                if sys.platform == 'win32':
                    tempslash = "\\"
                else:  # sys.platform=='darwin':
                    tempslash = "//"


                #Creating names for use in new CSV file creation
                #CSV files will eventualy contain the bursts
                data_set_name = path_entry.split(tempslash)[-1].rstrip().strip(tempslash)

                csv_name1 = str(data_set_number) + r'_Matrix_csv_' + data_set_name + '_intensity.csv'
                csv_name2 = str(data_set_number) + r'_Matrix_csv_' + data_set_name + '_frames.csv'


                #Temparary numbers for assigning bursts
                #Keeps track of which bursts is what
                burst_count_number_img = combind_burst_num
                burst_count_number_img_view = combind_burst_num + 1
                burst_count_number_index = []
                trk_count = 0

                #finds all files with a certain extension
                def findFiles(path_entry, filter):
                    for root, dirs, files in os.walk(path_entry):
                        for file in fnmatch.filter(files, filter):
                            yield os.path.join(file)

                #Appends trkfile list for every trk filename in path
                for trkFile in findFiles(path_entry, '*.trk'):
                    print trkFile
                    trk_list.append(trkFile)
                    
                #Finds the number tags for every file name
                for i in trk_list:
                    for x in range(0,10):
                        if var3.get() == 1:
                            if int(di[i[selection_list[1][0]:selection_list[1][1]]]) == x:
                                temp = ''
                                for z in range(0, len(selection_list)):
                                    range1 = selection_list[z][0]
                                    range2 = selection_list[z][1]

                                    print i[range1:range2]

                                    if z == 1:
                                        if var3.get() == 1:
                                            temp = temp + '.' + str(di[i[range1:range2]])
                                        else:
                                            temp = temp + '.' + str(re.sub('[^0-9]', '', i[range1:range2]))
                                    else:
                                        temp = temp + str(re.sub('[^0-9]', '', i[range1:range2]))

                                trk_list_ordered.append(temp)

                        else:
                            if int(re.sub('[^0-9]', '', i[selection_list[1][0]:selection_list[1][1]])) == x:
                                temp = str(re.sub('[^0-9]', '', i[selection_list[0][0]:selection_list[0][1]])) + str('.') + str(x)

                                trk_list_ordered.append(temp)

                print trk_list_ordered

                #Organize the list of trk files such that the data is ordered
                def enumerate_list(trk_list, forward):
                    global trk_list_ordered
                    global end_list

                    constant = -1
                    end_list = []
                    end_list1 = []
                    end_list2 = []
                    source = []

                    identity_list = []

                    for i in trk_list:
                        constant = constant + 1
                        identity_list.append(constant)
                        for x in range(0, 10):
                            if var3.get() == 1:
                                if int(di[i[selection_list[1][0]:selection_list[1][1]]]) == x:
                                    temp = ''
                                    for z in range(0, len(selection_list)):
                                        range1 = selection_list[z][0]
                                        range2 = selection_list[z][1]

                                        print i[range1:range2]

                                        if z == 1:
                                            if var3.get() == 1:
                                                temp = temp + '.' + str(di[i[range1:range2]])
                                            else:
                                                temp = temp + '.' + str(re.sub('[^0-9]', '', i[range1:range2]))
                                        else:
                                            temp = temp + str(re.sub('[^0-9]', '', i[range1:range2]))

                                    end_list1.append(float(temp))

                            else:
                                if int(re.sub('[^0-9]', '', i[selection_list[1][0]:selection_list[1][1]])) == x:
                                    temp = str(re.sub('[^0-9]', '', i[selection_list[0][0]:selection_list[0][1]])) + str(
                                        '.') + str(x)

                                    end_list1.append(float(temp))

                    #This will inverse the order but it is currently not used
                    if forward is False:
                        for j in range(0, len(identity_list)):
                            for i in identity_list:
                                if i >= 0:
                                    if end_list1[i] is max(end_list1):
                                        if end_list1[i] >= 0:
                                            source.append(trk_list[i])
                                            end_list2.append(end_list1[i])
                                            end_list1[i] = -1
                                            identity_list[i] = -1

                    #This insures that the files are listed in order 0-X
                    if forward is True:
                        for j in range(0, len(identity_list)):
                            for i in identity_list:
                                if i >= 0:
                                    if end_list1[i] is min(end_list1):
                                        if end_list1[i] >= 0:
                                            source.append(trk_list[i])
                                            end_list2.append(end_list1[i])
                                            end_list1[i] = 9999
                                            identity_list[i] = -1
                                            
                    #Updates the values for latter use
                    end_list = end_list2
                    trk_list_ordered = source

                #Organize the trk list
                enumerate_list(trk_list, forward)

                #Show the experiment name within the GUI
                tempsave1.append(tempsave1[-1] + 1)
                Label(frame3, text=(tempsave1[-1])).grid(row=tempsave1[-1], column=0, sticky=W)
                Label(frame3, text=data_set_name).grid(row=tempsave1[-1], column=1, sticky=W)

                #Dictionary that will hold all of the information about the burst
                #for latter call back
                d_matrix_hold = {}

                #Extracts bursts for every trk file
                for x in trk_list_ordered:
                    #Define Path and file
                    path = path_entry
                    file = x

                    #Shos the trk file being used in the GUI
                    tempsave2.append(tempsave2[-1] + 1)
                    Label(frame4, text=file).grid(row=tempsave2[-1], column=1, sticky=W)


                    #Creates a slash designated for the fileing system of your platform
                    if sys.platform == 'win32':
                        tempslash = "\\"
                    else:  # sys.platform=='darwin':
                        tempslash = "//"


                    #Finds which organization structure was used (new data should be _idealized_traces)
                    if os.path.exists(path+tempslash+x[:-4]+'_idelized_traces.txt.hist.txt') is True:
                        file2 = x.strip('.trk')+'_idelized_traces.txt.hist.txt'
                    if os.path.exists(path+tempslash+x[:-4]+"_idealized_traces.txt") is True:
                        file2 = x[:-4]+'_idealized_traces.txt'


                    #Defines the lists to put the information of a trace into
                    Intensity = []
                    Frame = []
                    HMM = []

                    
                    #These two if statments determine which fileing system to 
                    #use and extract he information appropriately
                    if os.path.exists(path+tempslash+x[:-4]+"_idealized_traces.txt") is True:
                        for i in open(path+tempslash+file, 'r'):
                            z = i.split()
                            Intensity.append(z[2])
                            Frame.append(z[3])


                        for i in open(path+tempslash+file2, 'r'):
                            HMM.append(float(i.strip('\n'))+1)
                    if os.path.exists(path+tempslash+x[:-4]+'_idelized_traces.txt.hist.txt') is True:
                        for i in open(path+tempslash+file, 'r'):
                            x = i.split(',')
                            for y in x:
                                if y == x[2]:
                                    Intensity.append(y)
                                if y == x[3]:
                                    Frame.append(y)
                        try:
                            for i in open(path+tempslash+file2, 'r'):
                                HMM.append(float(i.strip('\n'))+1)
                            #HMM.append(int(0))
                        except:
                            pass


                    #Defines the minimum and maximum values of the HMM for redefinng to 0 an 1
                    max_HMM = max(HMM)
                    min_HMM = min(HMM)
                    
                    #Redefines each value in the HMM to 0 or 1
                    for i in range(0,len(HMM)):
                        if HMM[i] == min_HMM:
                            HMM[i] = 0
                        if HMM[i] == max_HMM:
                            HMM[i] = 1
                        if i == 0:
                            HMM[0] = 0
                    #HMM.append(0)

                    #Dictionary to store local information about the bursts
                    d_List = {}
                    hold = 0

                    #Defining the windowing for each burst
                    field_range1_start = 1
                    field_range1 = 1
                    field_range2 = 4


                    #Determining where to extract each burst in a trace
                    #Summarized as if 1 append to appropriate d_List dictionary
                    #else dont, but if begging or ending add 3 to appropiate end
                    for i in range(0,len(HMM)):
                        if HMM[i] == 1:
                            if i in range(0,3):
                                key = "Burst{0}".format(hold)
                                if d_List.has_key(key) is False:
                                    d_List["Burst{0}".format(hold)] = []
                                    a =  d_List["Burst" + str(hold)]

                                    d_List["Intensity{0}".format(hold)] = []
                                    b =  d_List["Intensity" + str(hold)]

                                    d_List["Frame{0}".format(hold)] = []
                                    c =  d_List["Frame" + str(hold)]

                                if d_List.has_key(key) is True:
                                    a =  d_List["Burst" + str(hold)]
                                    b =  d_List["Intensity" + str(hold)]
                                    c =  d_List["Frame" + str(hold)]

                                if i == 1:
                                    a.append(int(1))
                                    b.append(Intensity[i-1])
                                    c.append(Frame[i-1])

                                a.append(int(1))
                                b.append(Intensity[i])
                                c.append(Frame[i])

                                if HMM[i+1] == 0:
                                    for x in range(field_range1_start,field_range2):
                                        a.append(int(0))
                                        b.append(Intensity[i+x])
                                        c.append(Frame[i+x])

                                    hold = hold + 1
                            elif i in range(len(HMM)-3,len(HMM)):
                                key = "Burst{0}".format(hold)
                                if d_List.has_key(key) is False:
                                    d_List["Burst{0}".format(hold)] = []
                                    a =  d_List["Burst" + str(hold)]

                                    d_List["Intensity{0}".format(hold)] = []
                                    b =  d_List["Intensity" + str(hold)]

                                    d_List["Frame{0}".format(hold)] = []
                                    c =  d_List["Frame" + str(hold)]

                                if d_List.has_key(key) is True:
                                    a =  d_List["Burst" + str(hold)]
                                    b =  d_List["Intensity" + str(hold)]
                                    c =  d_List["Frame" + str(hold)]

                                if HMM[i-1] == 0:
                                    for x in range(field_range1,field_range2):
                                        h = field_range2 - x
                                        a.append(int(0))
                                        b.append(Intensity[i-h])
                                        c.append(Frame[i-h])

                                a.append(int(1))
                                b.append(Intensity[i])
                                c.append(Frame[i])

                                n_add1 = 1
                                n_add2 = len(HMM)-i

                                for x in range(n_add1,n_add2):

                                    a.append(int(0))
                                    b.append(Intensity[i+x])
                                    c.append(Frame[i+x])
                                hold = hold +1
                                break

                            else:
                                key = "Burst{0}".format(hold)
                                if d_List.has_key(key) is False:
                                    d_List["Burst{0}".format(hold)] = []
                                    a =  d_List["Burst" + str(hold)]

                                    d_List["Intensity{0}".format(hold)] = []
                                    b =  d_List["Intensity" + str(hold)]

                                    d_List["Frame{0}".format(hold)] = []
                                    c =  d_List["Frame" + str(hold)]

                                if d_List.has_key(key) is True:
                                    a =  d_List["Burst" + str(hold)]
                                    b =  d_List["Intensity" + str(hold)]
                                    c =  d_List["Frame" + str(hold)]

                                if HMM[i-1] == 0:
                                    for x in range(field_range1,field_range2):
                                        h = field_range2 - x
                                        a.append(int(0))
                                        b.append(Intensity[i-h])
                                        c.append(Frame[i-h])

                                    a.append(int(1))
                                    b.append(Intensity[i])
                                    c.append(Frame[i])

                                if HMM[i+1] == 1:
                                    if HMM[i-1] != 0:
                                        a.append(int(1))
                                        b.append(Intensity[i])
                                        c.append(Frame[i])

                                if HMM[i+1] == 0:
                                    if HMM[i-1] != 0:
                                        a.append(int(1))
                                        b.append(Intensity[i])
                                        c.append(Frame[i])

                                    for x in range(field_range1,field_range2):
                                        a.append(int(0))
                                        b.append(Intensity[i+x])
                                        c.append(Frame[i+x])
                                    hold = hold +1

                    #Add one frame to HMM if not the appropriate length
                    if len(Frame) != len(HMM):
                        HMM.append(int(0))


                    #Determine if the whole trace should be saved as a picture
                    #If so simply plot and save the graph and create folder if needed
                    if var1.get() == 1:
                        directory1 = str(os.path.dirname(os.path.realpath(__file__))) + r'\ImageFolder'
                        if not os.path.exists(directory1):
                            os.makedirs(directory1)

                        fig, ax1 = plt.subplots()

                        ax1.plot(Frame, Intensity, 'b-')
                        ax1.set_xlabel('Frame')
                        ax1.set_ylabel('Intensity', color='b')
                        ax1.tick_params('y', colors='b')

                        ax2 = ax1.twinx()

                        ax2.plot(Frame, HMM, 'r--')
                        ax2.set_ylabel('HMM', color='r')
                        ax2.tick_params('y', colors='r')

                        fig.savefig(directory1+tempslash+file[:-4]+'.png')

                        plt.clf()
                        #plt.close()
                        
                        
                        #Write trace in easier to access format
                        with open(directory1+tempslash+file[:-4]+'_csv_trace.csv', 'wb') as myfile:
                            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                            wr.writerow(Intensity)
                        

                    #for every burst put burst to matrix for saving to CSV file
                    for i in range(0, len(d_List)/3):
                        if len(d_List['Frame'+str(i)]) >= 1:
                            #Determine if the individual bursts should be saved as a picture
                            #If so simply plot and save the graph and create folder if needed
                            if var2.get() == 1:

                                directory2 = str(os.path.dirname(os.path.realpath(__file__))) + r'\ImageFolder\BurstImages'
                                if not os.path.exists(directory2):
                                    os.makedirs(directory2)

                                fig, ax = plt.subplots()
                                ax.plot(d_List['Frame'+str(i)], d_List['Intensity'+str(i)], 'b-')
                                ax.set_xlabel('Frame')
                                ax.set_ylabel('Intensity', color='b')
                                ax.tick_params('y', colors='b')

                                fig.savefig(directory2+tempslash+file[:-4]+ "_RANGE_Burst_" +str(burst_count_number_img_view)+'.png')

                                plt.clf()
                                #plt.close()


                            Burst_Name = data_set_name + str("_") + str(data_set_number) + str("_") + str(end_list[trk_count]) + '_Burst_Number_' + str(burst_count_number_img_view)

                            burst_count_number_index.append(burst_count_number_img_view)
                            d_matrix_hold["Burst_Name_{0}".format(burst_count_number_img_view)] = Burst_Name

                            int_hold1 = []
                            int_hold2 = []

                            for z in range(0, len(d_List['Frame'+str(i)])):
                                int_hold1.append(d_List['Frame'+str(i)][z])
                                int_hold2.append(d_List['Intensity'+str(i)][z])

                            #Used to make the matricies the same length
                            for z in range(len(d_List['Frame'+str(i)]), 4000):
                                int_hold1.append("")
                                int_hold2.append("")


                            data_matrix_temp = np.column_stack((int_hold1, int_hold2))
                            d_matrix_hold["Data_burst{0}".format(burst_count_number_img_view)] = data_matrix_temp
                            burst_count_number_img_view = burst_count_number_img_view + 1
                    trk_count += 1

                #The rest of the code is simply saving the bursts to the CSV file
                
                #Creating blank values as to not cause an error
                Header_Row = []
                element_hold = 1
                matrix1 = np.array(element_hold)
                matrix2 = np.array(element_hold)
                header_array = np.array(element_hold)

                #Create the header/name of bursts for the CSV file
                for i in range(0, len(burst_count_number_index)):
                    Header_Row.append(d_matrix_hold["Burst_Name_"+str(burst_count_number_index[i])])
                    header_array = np.asarray(Header_Row)

                #Create matrix containing all bursts
                for i in range(combind_burst_num+1, burst_count_number_img_view):
                    if i == combind_burst_num+1:
                        matrix1 = np.array(d_matrix_hold["Data_burst"+str(i)][:,1])
                        matrix2 = np.array(d_matrix_hold["Data_burst"+str(i)][:,0])


                    if i > combind_burst_num+1:
                        matrix1 = np.vstack((matrix1, np.array(d_matrix_hold["Data_burst"+str(i)][:,1])))
                        matrix2 = np.vstack((matrix2, np.array(d_matrix_hold["Data_burst"+str(i)][:,0])))


                #Save the intensities as one data set
                with open(csv_name1, "wb") as f:
                    writer = csv.writer(f)
                    writer.writerows(np.vstack((header_array, matrix1.transpose())))

                #Save the Frames as another data set
                with open(csv_name2, "wb") as f:
                    writer = csv.writer(f)
                    writer.writerows(np.vstack((header_array, matrix2.transpose())))

                #Put names of CSV files into list to use for combinding files if neccessary
                csv_list.append([csv_name1, csv_name2])


                #Update the global values for last burst creates and data set number
                #Data set number is simply the numeric value assocated with each experiment as it is read in
                data_set_number = data_set_number + 1
                combind_burst_num = burst_count_number_img_view - 1


        #Used to combind all of the CSV files created
        def Combind_csv_files():
            if Path_Entry.get() != '':
                if len(csv_list) != 0:
                    print csv_list
                    d = {}
                    for i in range(0,len(csv_list)):
                        d["dataFrame1_{0}".format(i)] = pd.read_csv(csv_list[i][0])
                        d["dataFrame2_{0}".format(i)] = pd.read_csv(csv_list[i][1])

                    list_of_dataFrames1 = []
                    list_of_dataFrames2 = []

                    for i in range(0,len(d)/2):
                        list_of_dataFrames1.append(d["dataFrame1_"+str(i)])
                        list_of_dataFrames2.append(d["dataFrame2_"+str(i)])

                    dataFrame1 = pd.concat(list_of_dataFrames1, axis=1)
                    dataFrame2 = pd.concat(list_of_dataFrames2, axis=1)


                    dataFrame1.to_csv('Compiled_Matrix_Intensity.csv', index=False)
                    dataFrame2.to_csv('Compiled_Matrix_Frames.csv', index=False)


        #Buttons for move around the GUI
        button1 = ttk.Button(self, text="Clustering", command=lambda: controller.show_frame(PageOne))
        button1.pack(side=LEFT, padx=5, pady=5)
        button2 = ttk.Button(self, text="Analysis", command=lambda: controller.show_frame(PageTwo))
        button2.pack(side=LEFT, padx=5, pady=5)

        Combind = Button(self, text="Combined CSV Files", command=lambda: Combind_csv_files())
        Combind.pack(side=RIGHT, padx=5, pady=5)
        PrintButton = Button(self, text="Create Matrix", command=lambda: Print_Entry())
        PrintButton.pack(side=RIGHT, padx=5, pady=5)
        PathButton = Button(self, text="Get Path", command=lambda: Path_Entry_Get())
        PathButton.pack(side=RIGHT, padx=5, pady=5)
        TestButton = Button(self, text="Get Test Regions", command=lambda: TestRegion_Entry_Get())
        TestButton.pack(side=RIGHT, padx=5, pady=5)
        FileButton = Button(self, text="Get Test File", command=lambda: TestFileName_Entry_Get())
        FileButton.pack(side=RIGHT, padx=5, pady=5)


#The second page of the GUI
#The clustering options are located within this page; you can also run rScript.Rmd from this page 
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        #Initializes tkinter window
        tk.Frame.__init__(self, parent)
        frame1 = Frame(self, relief=RAISED, borderwidth=1)
        frame1.pack(fill=BOTH, expand=True)
        
        #The title and location of the page
        label = tk.Label(frame1, text="Clustering Program", font=LARGE_FONT)
        label.pack(anchor='center', padx=5, pady=5)
        self.pack(fill=BOTH, expand=True)

        global csv_list

        #Labels and Entries for the various parameters to be feed into rScript
        parameter1_label = Label(frame1, text='Name of csv File', font=SMALL_FONT)
        parameter1 = Entry(frame1)
        parameter2_label = Label(frame1, text='Name of Clustering Folder', font=SMALL_FONT)
        parameter2 = Entry(frame1)
        parameter3_label = Label(frame1, text='Name of Test', font=SMALL_FONT)
        parameter3 = Entry(frame1)
        parameter4_label = Label(frame1, text='Interpolation', font=SMALL_FONT)
        parameter4 = Entry(frame1)
        parameter5_label = Label(frame1, text='Window Size', font=SMALL_FONT)
        parameter5 = Entry(frame1)
        parameter6_label = Label(frame1, text='Maximum Clusters', font=SMALL_FONT)
        parameter6 = Entry(frame1)
        parameter7_label = Label(frame1, text='Significant Clusters Threshold', font=SMALL_FONT)
        parameter7 = Entry(frame1)
        parameter8_label = Label(frame1, text='Percent Similarity Threshold', font=SMALL_FONT)
        parameter8 = Entry(frame1)
        parameter9_label = Label(frame1, text='Max Iterations', font=SMALL_FONT)
        parameter9 = Entry(frame1)
        parameter10_label = Label(frame1, text='Vigilance Parameter', font=SMALL_FONT)
        parameter10 = Entry(frame1)
        parameter11_label = Label(frame1, text='Picture: Number of Rows', font=SMALL_FONT)
        parameter11 = Entry(frame1)
        parameter12_label = Label(frame1, text='Picture: Number of Columns', font=SMALL_FONT)
        parameter12 = Entry(frame1)

        #Text automatically put into the entry fields
        parameter1.insert(END, 'Compiled_Matrix_Intensity.csv')
        parameter2.insert(END, str(os.path.dirname(os.path.realpath(__file__)))+r'\Script_Workspace')
        parameter3.insert(END, 'Full_Test_')
        parameter4.insert(END, '100')
        parameter5.insert(END, '6')
        parameter6.insert(END, '80')
        parameter7.insert(END, '5')
        parameter8.insert(END, '.75')
        parameter9.insert(END, '10')
        parameter10.insert(END, '0')
        parameter11.insert(END, '4')
        parameter12.insert(END, '5')

        #Sets the default position for aligning all of the labels and entries
        Label_x_variable = 75
        Entry_x_variable = 300
        Entry_width_variable = 350

        parameter1_label.place(x=Label_x_variable, y=100)
        parameter1.place(width=Entry_width_variable, x=Entry_x_variable, y=100)
        parameter2_label.place(x=Label_x_variable, y=125)
        parameter2.place(width=Entry_width_variable, x=Entry_x_variable, y=125)
        parameter3_label.place(x=Label_x_variable, y=150)
        parameter3.place(width=Entry_width_variable, x=Entry_x_variable, y=150)
        parameter4_label.place(x=Label_x_variable, y=175)
        parameter4.place(width=Entry_width_variable, x=Entry_x_variable, y=175)
        parameter5_label.place(x=Label_x_variable, y=200)
        parameter5.place(width=Entry_width_variable, x=Entry_x_variable, y=200)
        parameter6_label.place(x=Label_x_variable, y=225)
        parameter6.place(width=Entry_width_variable, x=Entry_x_variable, y=225)
        parameter7_label.place(x=Label_x_variable, y=250)
        parameter7.place(width=Entry_width_variable, x=Entry_x_variable, y=250)
        parameter8_label.place(x=Label_x_variable, y=275)
        parameter8.place(width=Entry_width_variable, x=Entry_x_variable, y=275)
        parameter9_label.place(x=Label_x_variable, y=300)
        parameter9.place(width=Entry_width_variable, x=Entry_x_variable, y=300)
        parameter10_label.place(x=Label_x_variable, y=325)
        parameter10.place(width=Entry_width_variable, x=Entry_x_variable, y=325)
        parameter11_label.place(x=Label_x_variable, y=350)
        parameter11.place(width=Entry_width_variable, x=Entry_x_variable, y=350)
        parameter12_label.place(x=Label_x_variable, y=375)
        parameter12.place(width=Entry_width_variable, x=Entry_x_variable, y=375)


        #Text box for useful information
        text_box1 = Text(frame1, wrap=WORD, width=45, height=20)
        text_box1.place(width=505, height=300, x=675, y=100)

        text_box1.insert(END, '** The Percent Similarity Threshold is taken as 1 - the value given when used for '
                              'naming. This indicates what top percentage value is represented in the clustering '
                              'patterns. \n \n** The vigilance parameter should stay at 0 to establish the competitive '
                              'behavior of the network. The vigilance parameter will not be put on the name of the '
                              'files, so besure to rename if necessary \n \n** The picture options will allow you to '
                              'change how many burst averages appear in the resulting picture. To update the picture'
                              ' run the last line of the rScript.Rmd file before the data is replaced or deleted.')


        #Creats CSV file with all of the parameters to be used in rScript
        def Update_Parameters_Write():
            #Retrieve all of the parameters from the entires
            value1 = parameter1.get()
            value2 = parameter2.get()
            value3 = parameter3.get()
            value4 = parameter4.get()
            value5 = parameter5.get()
            value6 = parameter6.get()
            value7 = parameter7.get()
            value8 = parameter8.get()
            value9 = parameter9.get()
            value10 = parameter10.get()
            value11 = parameter11.get()
            value12 = parameter12.get()

            #Put parameters in numpy array and create dummy for structure
            value_list = np.array([value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12])
            dummy_list = np.array([' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '])

            value_matrix = np.vstack([value_list,dummy_list])

            #Save parameter array to csv file
            with open('Script_Parameters.csv', "wb") as f:
                writer = csv.writer(f)
                writer.writerows(value_matrix)

            #Create Folder for data to be saved into if it does not exist
            directory3 = str(value2)
            if not os.path.exists(directory3):
                os.makedirs(directory3)


        #Runs rScript.Rmd to clustering program
        def run_rScript():
            os.startfile("rScript.Rmd")
            #subprocess.call("rScript.Rmd", shell=True)


        #Buttons for navigating GUI
        button1 = ttk.Button(self, text="Create Matrix", command=lambda: controller.show_frame(StartPage))
        button1.pack(side=LEFT, padx=5, pady=5)
        button2 = ttk.Button(self, text="Analysis", command=lambda: controller.show_frame(PageTwo))
        button2.pack(side=LEFT, padx=5, pady=5)

        Run_Script = Button(self, text="Run R Script", command=lambda: run_rScript())
        Run_Script.pack(side=RIGHT, padx=5, pady=5)
        Update_Parameters = Button(self, text="Update Parameters", command=lambda: Update_Parameters_Write())
        Update_Parameters.pack(side=RIGHT, padx=5, pady=5)


#The third page of the GUI
#The analysis programs are inside this code
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        #Initializes tkinter window
        tk.Frame.__init__(self, parent)
        frame1 = Frame(self, relief=RAISED, borderwidth=1)
        frame1.pack(fill=BOTH, expand=True)
        
        #The title and location of the page
        label = tk.Label(frame1, text="Analysis", font=LARGE_FONT)
        label.pack(anchor='center', padx=5, pady=5)
        self.pack(fill=BOTH, expand=True)


        Section1_label = Label(frame1, text='Assign Burst Images', font=NORM_FONT)
        Section2_label = Label(frame1, text='Statistics', font=NORM_FONT)
        Section1_label.place(x=260, y=60)
        Section2_label.place(x=900, y=60)


        #Creates a slash designated for the fileing system of your platform
        if sys.platform == 'win32':
            tempslash = "\\"
        else:  # sys.platform=='darwin':
            tempslash = "//"


        #Labels and entries for various inputs
        File_Name_label = Label(frame1, text='Path for Clustering File', font=SMALL_FONT)
        File_Name = Entry(frame1)
        Folder_Name_label = Label(frame1, text='Name of Clustering Folder', font=SMALL_FONT)
        Folder_Name = Entry(frame1)
        SubFolder_label = Label(frame1, text='Name of Test', font=SMALL_FONT)
        SubFolder = Entry(frame1)

        TXT_File_Name_label = Label(frame1, text='Path for Clustering File', font=SMALL_FONT)
        TXT_File_Name = Entry(frame1)
        CSV1_File_Name_label = Label(frame1, text='Path for Frames File', font=SMALL_FONT)
        CSV1_File_Name = Entry(frame1)
        CSV2_File_Name_label = Label(frame1, text='Path for Intensity File', font=SMALL_FONT)
        CSV2_File_Name = Entry(frame1)
        New_File_Name_label = Label(frame1, text='Name of Statistics File', font=SMALL_FONT)
        New_File_Name = Entry(frame1)


        #Text automatically put into the entry fields
        File_Name.insert(END, os.path.dirname(os.path.realpath(__file__)) + tempslash + 'Script_Workspace' + tempslash +
                         'Full_Test_NN_Training_Results_top-5_max_clusters-80_more_than-5_vigilance-0.txt')
        Folder_Name.insert(END, r'Clustered Images')
        SubFolder.insert(END, 'Test_1')

        TXT_File_Name.insert(END, os.path.dirname(os.path.realpath(__file__)) + tempslash + 'Script_Workspace' + tempslash +
                         'Full_Test_NN_Training_Results_top-5_max_clusters-80_more_than-5_vigilance-0.txt')
        CSV1_File_Name.insert(END, os.path.dirname(os.path.realpath(__file__)) + tempslash + 'Script_Workspace' + tempslash +
                         'Compiled_Matrix_Frames.csv')
        CSV2_File_Name.insert(END, os.path.dirname(os.path.realpath(__file__)) + tempslash + 'Script_Workspace' + tempslash +
                         'Compiled_Matrix_Intensity.csv')
        New_File_Name.insert(END, 'Clustering_Statistics_Data.csv')



        #Variables for standardized placement of labels and entries
        Label_x_variable1 = 75
        Entry_x_variable1 = 300
        Entry_width_variable1 = 325

        Label_x_variable2 = 650
        Entry_x_variable2 = 850
        Entry_width_variable2 = 325

        File_Name_label.place(x=Label_x_variable1, y=100)
        File_Name.place(width=Entry_width_variable1, x=Entry_x_variable1, y=100)
        Folder_Name_label.place(x=Label_x_variable1, y=125)
        Folder_Name.place(width=Entry_width_variable1, x=Entry_x_variable1, y=125)
        SubFolder_label.place(x=Label_x_variable1, y=150)
        SubFolder.place(width=Entry_width_variable1, x=Entry_x_variable1, y=150)

        TXT_File_Name_label.place(x=Label_x_variable2, y=100)
        TXT_File_Name.place(width=Entry_width_variable2, x=Entry_x_variable2, y=100)
        CSV1_File_Name_label.place(x=Label_x_variable2, y=125)
        CSV1_File_Name.place(width=Entry_width_variable2, x=Entry_x_variable2, y=125)
        CSV2_File_Name_label.place(x=Label_x_variable2, y=150)
        CSV2_File_Name.place(width=Entry_width_variable2, x=Entry_x_variable2, y=150)
        New_File_Name_label.place(x=Label_x_variable2, y=175)
        New_File_Name.place(width=Entry_width_variable2, x=Entry_x_variable2, y=175)


        #Assign images to windows explorer folder
        def ImageFolder_Assign():
            #Creates a slash designated for the fileing system of your platform
            if sys.platform == 'win32':
                tempslash = "\\"
            else:  # sys.platform=='darwin':
                tempslash = "//"

            #Check to make sure that the ImageFolder does exist
            if os.path.exists(os.path.dirname(os.path.realpath(__file__)) + tempslash + 'ImageFolder') is True:
                #Retrieving entries
                path = str(os.path.dirname(os.path.realpath(__file__)))
                file_name = File_Name.get()
                new_folder = tempslash + Folder_Name.get()
                sub_folder = tempslash + SubFolder.get()

                file = open(file_name)

                hclust = False

                #Creating list for number of bursts and cluster numbers
                Burst_Hold = []
                Cluster_Hold = []

                #Extract burst cluster numbers and save to list
                for i in file:
                    a = i.strip("\n")
                    b = a.strip()

                    Cluster_Hold.append(int(b.split()[-1]))
                    if hclust == True:
                        Burst_Hold.append(b.split()[0][-5:].strip("b").strip("e").strip("r").strip("_").strip("\""))

                    if hclust == False:
                        Burst_Hold.append(b.split()[0][-5:].strip("b").strip("e").strip("r").strip("_").strip("\""))

                number_of_clusters = max(Cluster_Hold)

                #finds all files with a certain extension
                def findFiles(path, filter):
                    for root, dirs, files in os.walk(path):
                        for file in fnmatch.filter(files, filter):
                            yield os.path.join(file)

                #Create list to store the names of the images
                png_List = []
                
                #Find and save all burst images in ImageFolder to list
                for pngFile in findFiles(path + "\ImageFolder", '*.png'):
                    a = pngFile[-23:-4]
                    print a

                    if '_' in a[0:3]:
                        a = a.replace("_", "", 1)
                    if '_' in a[0:3]:
                        a = a.replace("_", "", 1)
                    if '0' in a[0:3]:
                        a = a.replace("0", "", 1)
                    if '1' in a[0:3]:
                        a = a.replace("1", "", 1)
                    if '2' in a[0:3]:
                        a = a.replace("2", "", 1)
                    if '3' in a[0:3]:
                        a = a.replace("3", "", 1)

                    if "Burst_" in a:
                        png_List.append("\\" + pngFile)

                #Create folders for every cluster if one do not exist
                for i in range(1, int(number_of_clusters) + 1):
                    Cluster = r"\Cluster {0}"
                    if not os.path.exists(path + new_folder + sub_folder + Cluster.format(i)):
                        os.makedirs(path + new_folder + sub_folder + Cluster.format(i))

                #Copy and paste image to appropriate cluster folder
                for i in range(0, len(Burst_Hold)):
                    for x in range(0, len(png_List)):
                        if "RANGE_Burst_{0}.png".format(str(int(Burst_Hold[i]))) in png_List[x]:
                            cluster = Cluster_Hold[i]
                            print path + png_List[x]
                            Cluster = r"\Cluster {0}"

                            shutil.copy(path + "\\Imagefolder\\BurstImages\\" + png_List[x],
                                        path + new_folder + sub_folder + Cluster.format(str(cluster)))
                            break


        def Statistics():
            #Creates a slash designated for the fileing system of your platform
            if sys.platform == 'win32':
                tempslash = "\\"
            else:  # sys.platform=='darwin':
                tempslash = "//"

            #Retrieving entries for variables
            path = str(os.path.dirname(os.path.realpath(__file__)))

            txt_name1 = TXT_File_Name.get()

            csv_frames = CSV1_File_Name.get()
            csv_intensity = CSV2_File_Name.get()

            new_file_name = New_File_Name.get()


            #Creating lists temporarily saving burst data
            burst_name = []
            burst_number_list = []
            burst_cluster_set1 = []

            #Creating dictionaries for temporarily saving burst data
            d_burst_frame = {}
            d_burst_intensity = {}

            #Extracting and saving clusters and name information to lists
            txt_open1 = open(txt_name1, 'r')
            for i in txt_open1:
                burst_name.append(i.strip("\n").split()[0])
                burst_cluster_set1.append(int(i.strip("\n").split()[1]))
            burst_name = burst_name[1:]
            burst_cluster_set1 = burst_cluster_set1[1:]

            #Decomposing names of bursts back to numbers for organizing
            for i in burst_name:
                burst_number_temp = re.sub("[^0-9]", "", i[-5:])
                burst_number_list.append(int(burst_number_temp))

            #Extracting and saving frame information to lists
            with open(csv_frames, 'rb') as f:
                #Skip the first line
                next(f)
                reader = csv.reader(f)

                create = 0
                burst_number = 1

                #Save informaiton to dictionary
                for row in reader:
                    for i in range(0, len(row)):
                        if create == 0:
                            d_burst_frame["Burst_frame_{0}".format(str(i + 1))] = []
                            a = d_burst_frame["Burst_frame_" + str(i + 1)]

                            a.append(float(row[i]))
                        if create != 0:
                            a = d_burst_frame["Burst_frame_" + str(i + 1)]
                            if row[i] != '':
                                a.append(float(row[i]))
                    create = 1

            #Extracting and saving intensity information to lists
            with open(csv_intensity, 'rb') as f:
                #Skip the first line
                next(f)
                reader = csv.reader(f)

                create = 0
                burst_number = 1

                #Save informaiton to dictionary
                for row in reader:
                    for i in range(0, len(row)):
                        if create == 0:
                            d_burst_intensity["Burst_intensity_{0}".format(str(i + 1))] = []
                            a = d_burst_intensity["Burst_intensity_" + str(i + 1)]
                            a.append(float(row[i]))

                        if create != 0:
                            a = d_burst_intensity["Burst_intensity_" + str(i + 1)]
                            if row[i] != '':
                                a.append(float(row[i]))
                    create = 1

            #Create matrix for saving matrix to CSV file
            track = 0
            for i in range(1, len(burst_name)):
                #Collect information together for a single burst
                intensity_temp = d_burst_intensity["Burst_intensity_" + str(i)]
                frame_temp = d_burst_frame["Burst_frame_" + str(i)]
                burst_name_temp = burst_name[i - 1]
                burst_number_temp = burst_number_list[i - 1]
                cluster_set1_temp = burst_cluster_set1[i - 1]
                frame_min = min(frame_temp)
                frame_max = max(frame_temp)
                frame_length = len(frame_temp)
                intensity_min = min(intensity_temp)
                intensity_max = max(intensity_temp)
                intensity_avg = np.average(intensity_temp)

                #Create header for CSV file
                if track == 0:
                    matrix_header = np.array(['Burst Name', 'Burst Number',
                                              'Beggining Frame', 'End Frame',
                                              'Length of Burst', 'Minimum Intensity',
                                              'Maximum Intensity', 'Average Intensity',
                                              'Cluster #', ])
                    matrix = np.array([burst_name_temp, burst_number_temp, frame_min,
                                       frame_max, frame_length, intensity_min, intensity_max,
                                       intensity_avg, cluster_set1_temp])

                #Add data to matrix
                if track != 0:
                    matrix_temp = np.array([burst_name_temp, burst_number_temp, frame_min,
                                            frame_max, frame_length, intensity_min,
                                            intensity_max, intensity_avg, cluster_set1_temp])
                    matrix = np.vstack((matrix, matrix_temp))

                track = 1

            #Write matrix to CSV file
            with open(new_file_name, "wb") as f:
                print new_file_name
                writer = csv.writer(f)
                writer.writerows(np.vstack((matrix_header, matrix)))


        #Buttons for navigating GUI
        button1 = ttk.Button(self, text="Create Matrix", command=lambda: controller.show_frame(StartPage))
        button1.pack(side=LEFT, padx=5, pady=5)
        button2 = ttk.Button(self, text="Clustering", command=lambda: controller.show_frame(PageOne))
        button2.pack(side=LEFT, padx=5, pady=5)

        py_list_file_button = Button(self, text="Statistics", command=lambda: Statistics())
        py_list_file_button.pack(side=RIGHT, padx=5, pady=5)
        save_py_list = Button(self, text="Assign Burst Images", command=lambda: ImageFolder_Assign())
        save_py_list.pack(side=RIGHT, padx=5, pady=5)


#Properly terminate the script upon exit
def end_program():
    app.destroy()
    sys.exit()

#Running the main GUI
app = MainGUI()
app.protocol('WM_DELETE_WINDOW', end_program)
app.resizable(width=False, height=False)
app.geometry("1280x720")
make_menu(app)
app.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
app.mainloop()
