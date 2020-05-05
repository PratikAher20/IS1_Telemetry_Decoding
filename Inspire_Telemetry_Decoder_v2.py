import csv
list_packets = []
# Opening the file containing a list of different packets and their APIDs
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
        list_packets.append(list(list_temp))

# Creating a list of integers from the raw output file from Hydra
raw_list = []
with open("hydra_log", "rb") as f:
    while True:
        byte = f.read(1)
        if not byte:
            break
        raw_list.append(int(ord(byte)))


# Scanning through the list to look for different types of packets
array_index = 0
while (array_index<len(raw_list)):
    packet_apid = raw_list[array_index+1]
    packet_length = 256*raw_list[array_index+4] + raw_list[array_index+5]
    for j in range(0, len(list_packets), 1):
        if (packet_apid == int(list_packets[j][1])):
            list_packets[j][2].append(list(raw_list[array_index:array_index + packet_length + 7]))
    array_index = array_index + packet_length + 7

# writing the raw different types of packets to level 0 csv files
for j in range(0, len(list_packets), 1):
    if (len(list_packets[j][2])>0):
        name_str = str(list_packets[j][0])+"_level_0.csv"
        with open(name_str, "w") as f:
            writer = csv.writer(f)
            for row in list_packets[j][2]:
                writer.writerow(row)

# Code to implement packet decoding
# Reading the packet telemetry defination from the csv file
# This csv file must be in a predefined format for the code to work
packet_def = []
with open("beacon_pckt_def.csv",'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        list_temp = []
        for key, value in row.items():
            list_temp.append(value)
        packet_def.append(list(list_temp))

# Reading the apid from the packet defination csv and finding the
# Corresponding level 2 data array created previously
packet_decode_apid = (int(packet_def[1][1]))
for j in range(0, len(list_packets), 1):
    if(packet_decode_apid == int(list_packets[j][1])):
        packet_raw_array = list_packets[j][2]
        packet_decode_number = j

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
        print("here")
        convertedVar = C0+C1*var+C2*var*var
        return convertedVar

packet_header_array = []
packet_decoded_array = []
decoded_array_index = 0

# This part of the code is used to decode the "type" of the
# Level 0 data to get the Level 1 variables
for i in range(0,len(packet_raw_array),1):
    for j in range(0,len(packet_def),1):
        # Collecting the 1st Row which has the variable name
        if(i==0):
            packet_header_array.append(packet_def[j][0])

        # Implementing decoding - combining bytes
        type = packet_def[j][2]
        conversion = packet_def[j][3]
        if(type=='U8' or type=='D8' or type=='I8' or type=='F8' ):
            var = packet_raw_array[i][decoded_array_index]
            if(conversion == ''):
                packet_decoded_array.append(var)
            else:
                packet_decoded_array.append(performConversion(var,conversion))
            decoded_array_index += 1

        elif(type=='U16' or type=='D16' or type=='I16' or type=='F16'):
            var = 256*packet_raw_array[i][decoded_array_index+1]+packet_raw_array[i][decoded_array_index]
            if (conversion == ''):
                packet_decoded_array.append(var)
            else:
                packet_decoded_array.append(performConversion(var,conversion))
            decoded_array_index += 2

        elif(type=='U32' or type=='D32' or type=='I32' or type=='F32'):
            var = 256*256*256*packet_raw_array[i][decoded_array_index+3] \
                                                        + 256*256*packet_raw_array[i][decoded_array_index + 2]\
                                                        + 256*packet_raw_array[i][decoded_array_index + 1] \
                                                        + packet_raw_array[i][decoded_array_index]
            if(conversion == ''):
                packet_decoded_array.append(var)
            else:
                packet_decoded_array.append(performConversion(var,conversion))
            decoded_array_index += 4
        #print(decoded_array_index)
    list_packets[packet_decode_number][3].append(list(packet_decoded_array))
    decoded_array_index=0
    packet_decoded_array=[]

# This writes the level 1 data to a csv file
name_str_l1 = str(list_packets[packet_decode_number][0])+"_level_1.csv"
with open(name_str_l1, "w") as f:
    writer = csv.writer(f)
    writer.writerow(packet_header_array)
    for row in list_packets[packet_decode_number][3]:
        writer.writerow(row)

