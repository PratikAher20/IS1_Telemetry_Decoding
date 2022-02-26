import csv
import os
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from satnogs.satnogs import Satnogs
import cubeds
import argparse


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

# This function performs a polynomial conversion on the level 0 data
# Can be extended to do other types of conversions
def performConversion(var,conversion):
    if (conversion[0] == ''):
        return var
    else:
        C0 = float(conversion[0])
        C1 = float(conversion[1])
        C2 = float(conversion[2])
        C3 = float(conversion[3])
        C4 = float(conversion[4])
        convertedVar = C0 + C1 * var + C2 * var * var + C3 * var * var * var + C4 * var * var * var * var
        return convertedVar

def performSignedValues(var, type):
    variable_type = type[0]
    numbits = int(type[1:])
    if(variable_type =='I'):
        if(var<2**(numbits-1)):
            return var
        else:
            return (var - 2**(numbits))
    else:
        return var

#OLD Function
# def DecodePacketsUHF():
#     # Opening the file containing a list of different packets and their APIDs
#     global list_packets
#     list_packets = []
#     with open("packet_apids.csv", 'r') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             list_temp = []
#             for key, value in row.items():
#                 list_temp.append(value)
#             # Empty List for level 0 decoded telemetry
#             list_temp.append([])
#             # Empty List for level 1 decoded telemetry
#             list_temp.append([])
#             # Empty list for packet definations
#             list_temp.append([])
#             list_packets.append(list(list_temp))
#
#     # Reading the packet definations from the  packet_def.csv file
#     packets_def = []
#     with open("packet_def.csv", 'r') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             list_temp = []
#             for key, value in row.items():
#                 list_temp.append(value)
#             packets_def.append(list(list_temp))
#
#     raw_list = []
#     # Opening multiple hydra log files
#     root = Tk()
#     root.withdraw()
#     Path = filedialog.askdirectory()
#     Path = Path + "/"
#     filelist = os.listdir(Path)
#     for i in filelist:
#         # print(i[0])
#         if (i[0] == 'c'):
#             with open(Path + i, 'rb') as f:
#                 while True:
#                     byte = f.read(1)
#                     if not byte:
#                         break
#                     raw_list.append(int(ord(byte)))
#
#     # Scanning through the list to look for different types of packets
#     array_index = 0
#     while (array_index < len(raw_list)):
#         packet_apid = raw_list[array_index + 1]
#         packet_length = 256 * raw_list[array_index + 4] + raw_list[array_index + 5]
#         for j in range(0, len(list_packets), 1):
#             if (packet_apid == int(list_packets[j][1])):
#                 list_packets[j][3].append(list(raw_list[array_index:array_index + packet_length + 7]))
#         array_index = array_index + packet_length + 7
#
#     # creating new level 0 and level 1 folders which would contain the decoded files
#     l0_directory = "Level 0 Packets"
#     path_new_l0 = os.path.join(Path, l0_directory)
#     os.mkdir(path_new_l0)
#
#     l1_directory = "Level 1 Packets"
#     path_new_l1 = os.path.join(Path, l1_directory)
#     os.mkdir(path_new_l1)
#
#     # writing the raw different types of packets to level 0 csv files
#     for j in range(0, len(list_packets), 1):
#         if (len(list_packets[j][3]) > 0):
#             name_str = str(list_packets[j][0]) + "_level_0.csv"
#             with open(path_new_l0 + "/" + name_str, "w") as f:
#                 writer = csv.writer(f)
#                 for row in list_packets[j][2]:
#                     writer.writerow(row)
#
#     # Arranging the definations as an array according to APIDs in the list_packets
#     for m in range(0, len(packets_def), 1):
#         curr_packet_apid = (int(packets_def[m][1]))
#         for n in range(0, len(list_packets), 1):
#             if (curr_packet_apid == int(list_packets[n][1])):
#                 list_packets[n][5].append(list(packets_def[m]))
#
#     # Now implementing the level 1 conversions for all level 0 packets read
#     for a in range(0, len(list_packets), 1):
#         if (len(list_packets[a][3]) > 0):
#             # Perform the level 1 conversions first
#             cur_packet_decode_apid = int(list_packets[a][1])
#             print("current APID is", cur_packet_decode_apid)
#             curr_packet_raw_array = list_packets[a][3]
#             curr_packet_actual_len = list_packets[a][2]
#             curr_packet_def = list_packets[a][5]
#
#             curr_packet_decode_number = a
#             curr_packet_header_array = []
#             curr_packet_decoded_array = []
#             curr_decoded_array_index = 0
#
#             for i in range(0, len(curr_packet_raw_array), 1):
#                 for j in range(0, len(curr_packet_def), 1):
#                     # Implementing decoding - combining bytes
#                     type = curr_packet_def[j][2]
#                     conversion = curr_packet_def[j][4:9]
#                     # print(conversion)
#                     endian = curr_packet_def[j][3]
#                     name = curr_packet_def[j][0]
#
#                     if (type == 'U8' or type == 'D8' or type == 'I8' or type == 'F8' or type == 'I6'):
#                         var = curr_packet_raw_array[i][curr_decoded_array_index]
#                         curr_packet_decoded_array.append(performConversion(performSignedValues(var, type), conversion))
#                         curr_decoded_array_index += 1
#                         # Collecting the 1st Row which has the variable name
#                         if (i == 0):
#                             curr_packet_header_array.append(curr_packet_def[j][0])
#
#
#                     elif (type == 'U16' or type == 'D16' or type == 'I16' or type == 'F16'):
#                         if (endian == 'big'):
#                             var = 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] + \
#                                   curr_packet_raw_array[i][
#                                       curr_decoded_array_index]
#                         else:
#                             var = 256 * curr_packet_raw_array[i][curr_decoded_array_index] + curr_packet_raw_array[i][
#                                 curr_decoded_array_index + 1]
#
#                         curr_packet_decoded_array.append(performConversion(performSignedValues(var, type), conversion))
#                         curr_decoded_array_index += 2
#                         # Collecting the 1st Row which has the variable name
#                         if (i == 0):
#                             curr_packet_header_array.append(curr_packet_def[j][0])
#
#                     elif (type == 'U24' or type == 'D24' or type == 'I24' or type == 'F24'):
#
#                         if (endian == 'big'):
#                             var = 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index + 2] \
#                                   + 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] \
#                                   + curr_packet_raw_array[i][curr_decoded_array_index]
#                         else:
#                             var = 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index] \
#                                   + 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] \
#                                   + curr_packet_raw_array[i][curr_decoded_array_index + 2]
#
#                         curr_packet_decoded_array.append(performConversion(performSignedValues(var, type), conversion))
#                         curr_decoded_array_index += 3
#                         # Collecting the 1st Row which has the variable name
#                         if (i == 0):
#                             curr_packet_header_array.append(curr_packet_def[j][0])
#
#                     elif (type == 'U32' or type == 'D32' or type == 'I32' or type == 'F32'):
#
#                         if (endian == 'big'):
#                             var = 256 * 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index + 3] \
#                                   + 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index + 2] \
#                                   + 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] \
#                                   + curr_packet_raw_array[i][curr_decoded_array_index]
#                         else:
#                             var = 256 * 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index] \
#                                   + 256 * 256 * curr_packet_raw_array[i][curr_decoded_array_index + 1] \
#                                   + 256 * curr_packet_raw_array[i][curr_decoded_array_index + 2] \
#                                   + curr_packet_raw_array[i][curr_decoded_array_index + 3]
#                         curr_packet_decoded_array.append(performSignedValues(performConversion(var, conversion), type))
#                         curr_decoded_array_index += 4
#                         # Collecting the 1st Row which has the variable name
#                         if (i == 0):
#                             curr_packet_header_array.append(curr_packet_def[j][0])
#                     elif (type == 'U608'):
#                         for p in range(0, 76, 1):
#                             # Collecting the 1st Row which has the variable name
#                             if (i == 0):
#                                 curr_packet_header_array.append(curr_packet_def[j][0])
#                             var = curr_packet_raw_array[i][curr_decoded_array_index]
#                             curr_packet_decoded_array.append(var)
#                             curr_decoded_array_index += 1
#
#                     elif (type == 'D1600'):
#                         for p in range(0, 200, 1):
#                             # Collecting the 1st Row which has the variable name
#                             if (i == 0):
#                                 curr_packet_header_array.append(curr_packet_def[j][0])
#                             var = curr_packet_raw_array[i][curr_decoded_array_index]
#                             curr_packet_decoded_array.append(var)
#                             curr_decoded_array_index += 1
#                     elif (type == 'U1024'):
#                         for p in range(0, 128, 1):
#                             # Collecting the 1st Row which has the variable name
#                             if (i == 0):
#                                 curr_packet_header_array.append(curr_packet_def[j][0])
#                             var = curr_packet_raw_array[i][curr_decoded_array_index]
#                             curr_packet_decoded_array.append(var)
#                             curr_decoded_array_index += 1
#                     elif (type == 'U1280'):
#                         for p in range(0, 160, 1):
#                             # Collecting the 1st Row which has the variable name
#                             if (i == 0):
#                                 curr_packet_header_array.append(curr_packet_def[j][0])
#                             var = curr_packet_raw_array[i][curr_decoded_array_index]
#                             curr_packet_decoded_array.append(var)
#                             curr_decoded_array_index += 1
#                     elif (type == 'C1920'):
#                         for p in range(0, 240, 1):
#                             # Collecting the 1st Row which has the variable name
#                             if (i == 0):
#                                 curr_packet_header_array.append(curr_packet_def[j][0])
#                             var = curr_packet_raw_array[i][curr_decoded_array_index]
#                             curr_packet_decoded_array.append(var)
#                             curr_decoded_array_index += 1
#                     elif (type == 'U1672'):
#                         for p in range(0, 209, 1):
#                             # Collecting the 1st Row which has the variable name
#                             if (i == 0):
#                                 curr_packet_header_array.append(curr_packet_def[j][0])
#                             var = curr_packet_raw_array[i][curr_decoded_array_index]
#                             curr_packet_decoded_array.append(var)
#                             curr_decoded_array_index += 1
#                     elif (type == 'U376'):
#                         for p in range(0, 23, 1):
#                             # Collecting the 1st Row which has the variable name
#                             if (i == 0):
#                                 curr_packet_header_array.append(curr_packet_def[j][0])
#                             var = curr_packet_raw_array[i][curr_decoded_array_index]
#                             curr_packet_decoded_array.append(var)
#                             curr_decoded_array_index += 1
#                     elif (type == 'U624'):
#                         for p in range(0, 78, 1):
#                             # Collecting the 1st Row which has the variable name
#                             if (i == 0):
#                                 curr_packet_header_array.append(curr_packet_def[j][0])
#                             var = curr_packet_raw_array[i][curr_decoded_array_index]
#                             curr_packet_decoded_array.append(var)
#                             curr_decoded_array_index += 1
#
#                 list_packets[curr_packet_decode_number][4].append(list(curr_packet_decoded_array))
#                 curr_decoded_array_index = 0
#                 curr_packet_decoded_array = []
#
#             # Store the level 1 data in CSV files
#             name_str_l1 = str(list_packets[curr_packet_decode_number][0]) + "_level_1.csv"
#             with open(path_new_l1 + "/" + name_str_l1, "w", newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(curr_packet_header_array)
#                 for row in list_packets[curr_packet_decode_number][4]:
#                     writer.writerow(row)
#
#     popupmsg("Success", "Done! Level 0 and Level 1 Packets Created")

#New Batch decode function

def batchDecodePackets():
    # Opening the file containing a list of different packets and their APIDs
    list_packets = []
    with open("packet_apids.csv", 'r') as f:
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

    raw_list = []
    # Opening multiple hydra log files
    root = Tk()
    root.withdraw()
    Path = filedialog.askdirectory()
    total_files = 0
    for path, subdirs, filelist in os.walk(Path):
        for name in filelist:
            total_files += 1
            with open(path + "/" + name, 'rb') as f:
                byte = f.read(1)
                while byte:
                    raw_list.append(int(ord(byte)))
                    byte = f.read(1)

    #If only one raw file is present, add filename as prefix to output
    if (total_files==1):
        out_file_prefix = filelist[0] + "_"
    else:
        out_file_prefix = ""

    # Scanning through the list to look for different types of packets
    array_index = 0
    pkt_cnt = 1
    actual_pckt_len = 0
    check_flag = 0


    while (array_index + 5 < len(raw_list)):
        packet_header = int(raw_list[array_index])
        packet_apid = int(raw_list[array_index + 1])
        packet_length = 256 * raw_list[array_index + 4] + raw_list[array_index + 5]

        if (packet_header != 8):
            array_index += 1
            continue

        for j in range(0, len(list_packets), 1):
            if ( packet_apid == int(list_packets[j][1]) and packet_length == int(list_packets[j][2])):
                print("Header", packet_header, " Number", pkt_cnt, "APID", packet_apid, "Length", packet_length)
                list_packets[j][3].append(list(raw_list[array_index:array_index + packet_length + 7])) #7
                actual_pckt_len = int(list_packets[j][2])
                check_flag = 0
                break
            else:
                check_flag = 1


        if (check_flag == 1):
            array_index += 1
            continue

        array_index = array_index + actual_pckt_len + 7  # 7
        pkt_cnt += 1

    # creating new level 0 and level 1 folders which would contain the decoded files
    l0_directory = "Level 0 Packets"
    path_new_l0 = os.path.join(Path, l0_directory)
    os.mkdir(path_new_l0)

    l1_directory = "Level 1 Packets"
    path_new_l1 = os.path.join(Path, l1_directory)
    os.mkdir(path_new_l1)

    # writing the raw different types of packets to level 0 csv files
    for j in range(0, len(list_packets), 1):
        if (len(list_packets[j][3]) > 0):
            name_str = out_file_prefix + str(list_packets[j][0]) + "_level_0.csv"
            with open(path_new_l0 +"/"+ name_str, "w") as f:
                writer = csv.writer(f)
                for row in list_packets[j][3]:
                    writer.writerow(row)


    # Arranging the definations as an array according to APIDs in the list_packets
    for m in range(0, len(packets_def), 1):
        #print((packets_def[m][0]))
        #print((packets_def[m][1]))
        curr_packet_apid = (int(packets_def[m][1]))
        for n in range(0, len(list_packets), 1):
            if (curr_packet_apid == int(list_packets[n][1])):
                list_packets[n][5].append(list(packets_def[m]))

    # Now implementing the level 1 conversions for all level 0 packets read
    for a in range(0, len(list_packets), 1):

        if (len(list_packets[a][3]) > 0):
            # Perform the level 1 conversions first
            cur_packet_decode_apid = int(list_packets[a][1])
            print("current APID is", cur_packet_decode_apid)
            curr_packet_actual_len = int(list_packets[a][2])+7
            curr_packet_raw_array = list_packets[a][3]
            curr_packet_def = list_packets[a][5]

            curr_packet_decode_number = a
            curr_packet_header_array = []
            curr_packet_decoded_array = []
            curr_decoded_array_index = 0

            for i in range(0, len(curr_packet_raw_array), 1):

                if (len(curr_packet_raw_array[i]) != curr_packet_actual_len):
                    continue

                for j in range(0, len(curr_packet_def), 1):
                    # Implementing decoding - combining bytes
                    type = curr_packet_def[j][2]
                    conversion = curr_packet_def[j][4:9]
                    #print(conversion)
                    endian = curr_packet_def[j][3]
                    if (type == 'U8' or type == 'D8' or type == 'I8' or type == 'F8' or type =='I6'):
                        var = curr_packet_raw_array[i][curr_decoded_array_index]
                        curr_packet_decoded_array.append(performConversion( performSignedValues(var,type ),conversion))
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

                        curr_packet_decoded_array.append(performConversion( performSignedValues(var,type ),conversion))

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

                        curr_packet_decoded_array.append(performConversion( performSignedValues(var,type ),conversion))

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
                        #curr_packet_decoded_array.append(performSignedValues(performConversion(var, conversion),type))

                        #Corrected code
                        curr_packet_decoded_array.append(performConversion(performSignedValues(var, type),conversion))

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
                    elif (type == 'U1672'):
                        for p in range(0, 209, 1):
                            # Collecting the 1st Row which has the variable name
                            if (i == 0):
                                curr_packet_header_array.append(curr_packet_def[j][0])
                            var = curr_packet_raw_array[i][curr_decoded_array_index]
                            curr_packet_decoded_array.append(var)
                            curr_decoded_array_index += 1
                    elif (type == 'U376'):
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

                list_packets[curr_packet_decode_number][4].append(list(curr_packet_decoded_array))
                curr_decoded_array_index = 0
                curr_packet_decoded_array = []

            # Store the level 1 data in CSV files
            name_str_l1 = out_file_prefix + str(list_packets[curr_packet_decode_number][0]) + "_level_1.csv"
            with open(path_new_l1 +"/"+ name_str_l1, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(curr_packet_header_array)
                for row in list_packets[curr_packet_decode_number][4]:
                    writer.writerow(row)

    popupmsg("Success","Done! Level 0 and Level 1 Packets Created")


# -------------- HELPER FUNCTIONS FOR THIS SATNOGS DOWNLOAD FUNCTION----------------------------------------------------
def parse_command_line_args():
    # Parsing command line arguments
    parser = argparse.ArgumentParser(description='Command Line Parser')

    parser.add_argument('-t', '--test', action="store_true", help="If present, program will be run in test mode")
    parser.add_argument('-d', '--debug', action="store_true", help="If present, program will be run in debug mode")
    parser.add_argument('-v', '--verbose', action="store_true", help="If present, program will be run in verbose mode")
    parser.add_argument('-m', '--mission', type=str, help="Specify specific mission using this parameter")
    parser.add_argument('-c', '--config', type=str,
                        help="Specifies what config file to use. If absent, cfg/example.cfg will be used")

    args = parser.parse_args()  # test bool will be stored in args.test
    return args

#Adding Support for downloading data from satnogs
def downloadSatnogsFile():
    args = parse_command_line_args()

    # Check if user set the config file command line argument. If so, extract it. This argument should
    # really always be used, unless "example.cfg" is changed to be something else.
    if args.config:
        config_file = args.config  # user specified config file
    else:
        config_file = 'cfg/default_config.yml'  # example config file

    # Load the config info from the file specified. Will get exception if file does not exist.
    config = cubeds.config.Config(file=config_file)

    # SETUP runtime parameters.
    if int(config.config['runtime']['verbose']):
        verbose = True
    elif args.verbose:
        verbose = True
    else:
        verbose = False

    if int(config.config['runtime']['test']):
        test = True
    elif args.test:
        test = True
    else:
        test = False

    if int(config.config['runtime']['debug']):
        debug = True
    elif args.debug:
        debug = True
    else:
        debug = False

    nogs = Satnogs(config)
    nogs.save_satnogs_data()

    popupmsg("Success", "Satnogs Data Downloaded")

def About():
    popupmsg("About","INSPIRE Telemetry Decoder Version 6, Created by: Anant "
                     "\nSource Code: https://github.com/anant-infinity/IS1_Temeletry_Decoding.git")

root = Tk()
root.iconbitmap(default='inspire_logo_icon.ico')
root.title("INSPIRE Telemetry Decoder v6")
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="Decode", menu=filemenu)
filemenu.add_command(label="Select Folder and Decode Files", command=batchDecodePackets)

downloadmenu = Menu(menu)
menu.add_cascade(label="Download Raw Files", menu=downloadmenu)
downloadmenu.add_command(label="Download Satnogs Raw File", command=downloadSatnogsFile)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)


text1 = Text(root, height=30, width=75)
photo = PhotoImage(file='./INSPIRE_logo.png')
text1.insert(END, '\n')
text1.image_create(END, image=photo)
text1.pack(side=LEFT)


text2 = Text(root, height=30, width=70)
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
Level 0 and Level 1 telemetry.Follow the 
following steps to decode the raw data files:

1. Click Decode-> Select Folder and Decode Packets
2. Open the folder (/directory) containing the Raw Log files

Done! Decoded Level 0 and Level 1 Packets will be
created in the same folder (as the raw files)

NOTE 1: The "packet_apids.csv" and the 
"beacon_pckt_def.csv"  must be present in the 
folder containing the decoder application.

Further instructions of setting up are
provided in the ReadMe.

"""
text2.insert(END, quote, 'color')
text2.pack(side=LEFT)
scroll.pack(side=RIGHT, fill=Y)
mainloop()















