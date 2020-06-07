import csv
import os
import sys
from tkinter import filedialog
from tkinter import *
from tkinter import ttk

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


#Creating a Popup Message to show Conversion is Complete
def popupmsg(title, msg):
    popup = Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

# Opening the file containing a list of different packets and their APIDs
list_packets = []
with open("packet_apids.csv",'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        list_temp = []
        for key, value in row.items():
            list_temp.append(value)
        # Empty List for level 0 decoded telemetry
        list_temp.append([])
        # Empty List for level 1 decoded telemetry
        list_temp.append([])
        # Empty list for packet definations
        list_temp.append([])
        list_packets.append(list(list_temp))

# Reading the packet definations from the  packet_def.csv file
packets_def = []
with open("packet_def.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        list_temp = []
        for key, value in row.items():
            list_temp.append(value)
        packets_def.append(list(list_temp))

# This function performs a polynomial conversion on the level 0 data
# Can be extended to do other types of conversions
def performConversion(var,conversion):

    C0_minus_flag = 0
    C1_minus_flag = 0
    C2_minus_flag = 0
    C3_minus_flag = 0

    if(conversion[3]=='-'):
        C0=-(float(conversion[4:11]))
        C0_minus_flag = 1
    else:
        C0 = (float(conversion[3:10]))
    if (len(conversion) <= 12):
        convertedVar = C0
        return convertedVar

    if(conversion[15]=='-'):
        if(C0_minus_flag == 0):
            C1 = -(float(conversion[16:23]))
        else:
            C1 = -(float(conversion[17:24]))
        C1_minus_flag=1
    else:
        if (C0_minus_flag == 0):
            C1 = (float(conversion[15:22]))
        else:
            C1 = (float(conversion[16:23]))

    if ( 12 < len(conversion) <= 24):
        convertedVar = C0+C1*var
        return convertedVar

    if(conversion[27]=='-'):
        if(C1_minus_flag == 0):
            C2 = -(float(conversion[28:35]))
        else:
            C2 = -(float(conversion[29:36]))
        C2_minus_flag=1
    else:
        if (C1_minus_flag == 0):
            C2 = (float(conversion[27:34]))
        else:
            C2 = (float(conversion[28:35]))

    if ( 24 < len(conversion) <= 36):
        convertedVar = C0+C1*var+C2*var*var
        return convertedVar

def DecodePackets():
    raw_list = []
    # Opening multiple hydra log files
    root = Tk()
    root.withdraw()
    Path = filedialog.askdirectory()
    Path = Path + "/"
    filelist = os.listdir(Path)
    print(filelist)
    for i in filelist:
        with open(Path + i, 'rb') as f:
            while True:
                byte = f.read(1)
                if not byte:
                    break
                raw_list.append(int(ord(byte)))

    # Scanning through the list to look for different types of packets
    array_index = 0
    while (array_index < len(raw_list)):
        packet_apid = raw_list[array_index + 1]
        packet_length = 256 * raw_list[array_index + 4] + raw_list[array_index + 5]
        for j in range(0, len(list_packets), 1):
            if (packet_apid == int(list_packets[j][1])):
                list_packets[j][2].append(list(raw_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    # writing the raw different types of packets to level 0 csv files
    for j in range(0, len(list_packets), 1):
        if (len(list_packets[j][2]) > 0):
            name_str = str(list_packets[j][0]) + "_level_0.csv"
            with open(Path + name_str, "w") as f:
                writer = csv.writer(f)
                for row in list_packets[j][2]:
                    writer.writerow(row)


    # Arranging the definations as an array according to APIDs in the list_packets
    for m in range(0, len(packets_def), 1):
        curr_packet_apid = (int(packets_def[m][1]))
        for n in range(0, len(list_packets), 1):
            if (curr_packet_apid == int(list_packets[n][1])):
                list_packets[n][4].append(list(packets_def[m]))

    # Now implementing the level 1 conversions for also level 0 packets read
    for a in range(0, len(list_packets), 1):
        if (len(list_packets[a][2]) > 0):
            # Perform the level 1 conversions first
            cur_packet_decode_apid = int(list_packets[a][1])
            curr_packet_raw_array = list_packets[a][2]
            curr_packet_def = list_packets[a][4]

            curr_packet_decode_number = a
            curr_packet_header_array = []
            curr_packet_decoded_array = []
            curr_decoded_array_index = 0

            for i in range(0, len(curr_packet_raw_array), 1):
                for j in range(0, len(curr_packet_def), 1):
                    # Implementing decoding - combining bytes
                    type = curr_packet_def[j][2]
                    conversion = curr_packet_def[j][3]
                    endian = curr_packet_def[j][4]
                    if (type == 'U8' or type == 'D8' or type == 'I8' or type == 'F8'):
                        var = curr_packet_raw_array[i][curr_decoded_array_index]
                        if (conversion == ''):
                            curr_packet_decoded_array.append(var)
                        else:
                            curr_packet_decoded_array.append(performConversion(var, conversion))
                        curr_decoded_array_index += 1
                        # Collecting the 1st Row which has the variable name
                        if (i == 0):
                            curr_packet_header_array.append(curr_packet_def[j][0])
                    elif (type == 'U16' or type == 'D16' or type == 'I16' or type == 'F16'):
                        if (endian == 'big'):
                            var = 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] + \
                                  curr_packet_raw_array[i][
                                      curr_decoded_array_index]
                        else:
                            var = 256 * curr_packet_raw_array[i][curr_decoded_array_index] + curr_packet_raw_array[i][
                                curr_decoded_array_index + 1]
                        if (conversion == ''):
                            curr_packet_decoded_array.append(var)
                        else:
                            curr_packet_decoded_array.append(performConversion(var, conversion))
                        curr_decoded_array_index += 2
                        # Collecting the 1st Row which has the variable name
                        if (i == 0):
                            curr_packet_header_array.append(curr_packet_def[j][0])

                    elif (type == 'U24' or type == 'D24' or type == 'I24' or type == 'F24'):

                        if (endian == 'big'):
                            var = 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index + 2] \
                                  + 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] \
                                  + curr_packet_raw_array[i][curr_decoded_array_index]
                        else:
                            var = 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index] \
                                  + 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] \
                                  + curr_packet_raw_array[i][curr_decoded_array_index + 2]

                        if (conversion == ''):
                            curr_packet_decoded_array.append(var)
                        else:
                            curr_packet_decoded_array.append(performConversion(var, conversion))
                        curr_decoded_array_index += 3
                        # Collecting the 1st Row which has the variable name
                        if (i == 0):
                            curr_packet_header_array.append(curr_packet_def[j][0])

                    elif (type == 'U32' or type == 'D32' or type == 'I32' or type == 'F32'):

                        if (endian == 'big'):
                            var = 256 * 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index + 3] \
                                  + 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index + 2] \
                                  + 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] \
                                  + curr_packet_raw_array[i][curr_decoded_array_index]
                        else:
                            var = 256 * 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index] \
                                  + 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] \
                                  + 256 * curr_packet_raw_array[i][curr_decoded_array_index + 2] \
                                  + curr_packet_raw_array[i][curr_decoded_array_index + 3]

                        if (conversion == ''):
                            curr_packet_decoded_array.append(var)
                        else:
                            curr_packet_decoded_array.append(performConversion(var, conversion))
                        curr_decoded_array_index += 4
                        # Collecting the 1st Row which has the variable name
                        if (i == 0):
                            curr_packet_header_array.append(curr_packet_def[j][0])
                    elif (type == 'U608'):
                        for p in range(0, 76, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1

                    elif (type == 'D1600'):
                        for p in range(0, 200, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1
                    elif (type == 'U1024'):
                        for p in range(0, 128, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1
                    elif (type == 'U1280'):
                        for p in range(0, 160, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1
                    elif (type == 'C1920'):
                        for p in range(0, 240, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1
                    elif (type == 'C1864'):
                        for p in range(0, 233, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1
                    elif (type == 'C184'):
                        for p in range(0, 23, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1
                    elif (type == 'U624'):
                        for p in range(0, 78, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1

                list_packets[curr_packet_decode_number][3].append(list(curr_packet_decoded_array))
                curr_decoded_array_index = 0
                curr_packet_decoded_array = []

            # Store the level 1 data in CSV files
            name_str_l1 = str(list_packets[curr_packet_decode_number][0]) + "_level_1.csv"
            with open(Path + name_str_l1, "w") as f:
                writer = csv.writer(f)
                writer.writerow(curr_packet_header_array)
                for row in list_packets[curr_packet_decode_number][3]:
                    writer.writerow(row)

    popupmsg("Success","Done! Level 0 and Level 1 Packets Created")


def About():
    popupmsg("About","INSPIRE Telemetry Decoder Version 4.0, Created by: Anant")


root = Tk()
root.iconbitmap(default='inspire_logo_icon.ico')
root.title("INSPIRE Telemetry Decoder v4.0")
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Select Folder and Decode Packets", command=DecodePackets)

filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)


text1 = Text(root, height=30, width=75)
photo = PhotoImage(file='./INSPIRE_logo.png')
text1.insert(END, '\n')
text1.image_create(END, image=photo)
text1.pack(side=LEFT)


text2 = Text(root, height=30, width=55)
scroll = Scrollbar(root, command=text2.yview)
text2.configure(yscrollcommand=scroll.set)
text2.tag_configure('bold_italics', font=('Verdana', 12, 'bold', 'italic'))
text2.tag_configure('big', font=('Verdana', 16, 'bold'))
text2.tag_configure('color',
                    foreground='#476042',
                    font=('Verdana', 12, 'bold'))
text2.tag_bind('follow',
               '<1>',
               lambda e, t=text2: t.insert(END, "Not now, maybe later!"))
text2.insert(END,'\nHow to Run\n', 'big')
quote = """
This application can be used to generate 
Level 0 and Level 1 telemetry for INSPIRESat-1 
raw data files obtained from Hydra:

1. Click Menu-> Select Folder and Decode Packets
2. Open the folder containing the Raw Log files

Done!

"""
text2.insert(END, quote, 'color')
text2.pack(side=LEFT)
scroll.pack(side=RIGHT, fill=Y)
mainloop()















