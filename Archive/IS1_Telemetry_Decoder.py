import csv


# defining the different APIDs
apid_beacon =	1
apid_des_hk =	11
apid_des_task =	14
apid_des_sched =	13
apid_des_time =	19
apid_mem_dump =	6
apid_fp_hk =	7
apid_lib_hk =	9
apid_tbl_hk =	8
apid_seq_hk =	5
apid_tlm_hk =	60
apid_cmd_hk =	12
apid_time_hk =	18
apid_sband_hk =	52
apid_sd_hk =	42
apid_uhf_hk =	40
apid_uhf_pass =	41
apid_cip_hk =	47
apid_cip_msg_hk =	51
apid_mode_hk =	53
apid_daxss_msg_hk =	46
apid_daxss_hk =	45
apid_ana_hk =	2
apid_adcs_msg_hk =	44
apid_adcs_hk =	43
apid_adcs_analogs =	215
apid_adcs_gps =	218
apid_adcs_clock_sync =	213
apid_adcs_tracker =	207
apid_adcs_refs =	203
apid_adcs_time =	202
apid_adcs_imu =	212
apid_adcs_cal =	219
apid_adcs_att_det =	204
apid_adcs_tracker_ctrl =	220
apid_adcs_att_ctrl =	208
apid_adcs_tables =	216
apid_adcs_general =	201
apid_adcs_att_cmd =	205
apid_adcs_tracker2 =	217
apid_adcs_tlm_proc =	214
apid_adcs_ext_tracker2 =	221
apid_adcs_rw_drive =	206
apid_adcs_momentum =	209
apid_adcs_css =	210
apid_adcs_mag =	211
apid_adcs_command_tlm =	200
apid_cip_soh =	50
apid_cip_sci1 =	48
apid_cip_sci2 =	49
apid_daxss_log =	176
apid_daxss_sci =	178
apid_adcs_l0 =	54

# Variable to store the number of packets in the data stream
num_beacon= 0
num_des_hk= 0
num_des_task= 0
num_des_sched= 0
num_des_time= 0
num_mem_dump= 0
num_fp_hk= 0
num_log_hk= 0
num_lib_hk= 0
num_tbl_hk= 0
num_seq_hk= 0
num_tlm_hk= 0
num_cmd_hk= 0
num_time_hk= 0
num_sband_hk= 0
num_sd_hk= 0
num_uhf_hk= 0
num_uhf_pass= 0
num_cip_hk= 0
num_cip_msg_hk= 0
num_mode_hk= 0
num_daxss_msg_hk= 0
num_daxss_hk= 0
num_ana_hk= 0
num_adcs_msg_hk= 0
num_adcs_hk= 0
num_adcs_analogs= 0
num_adcs_gps= 0
num_adcs_clock_sync= 0
num_adcs_tracker= 0
num_adcs_refs= 0
num_adcs_time= 0
num_adcs_imu= 0
num_adcs_cal= 0
num_adcs_att_det= 0
num_adcs_tracker_ctrl= 0
num_adcs_att_ctrl= 0
num_adcs_tables= 0
num_adcs_general= 0
num_adcs_att_cmd= 0
num_adcs_tracker2= 0
num_adcs_tlm_proc= 0
num_adcs_ext_tracker2= 0
num_adcs_rw_drive= 0
num_adcs_momentum= 0
num_adcs_css= 0
num_adcs_mag= 0
num_adcs_command_tlm= 0
num_cip_soh= 0
num_cip_sci1= 0
num_cip_sci2= 0
num_daxss_log= 0
num_daxss_sci= 0
num_adcs_l0= 0

# Arrays to store the packets
beacon_packets = []
des_hk_packets = []
des_task_packets = []
des_sched_packets = []
des_time_packets = []
mem_dump_packets = []
fp_hk_packets = []
log_hk_packets = []
lib_hk_packets = []
tbl_hk_packets = []
seq_hk_packets = []
tlm_hk_packets = []
cmd_hk_packets = []
time_hk_packets = []
sband_hk_packets = []
sd_hk_packets = []
uhf_hk_packets = []
uhf_pass_packets = []
cip_hk_packets = []
cip_msg_hk_packets = []
mode_hk_packets = []
daxss_msg_hk_packets = []
daxss_hk_packets = []
ana_hk_packets = []
adcs_msg_hk_packets = []
adcs_hk_packets = []
adcs_analogs_packets = []
adcs_gps_packets = []
adcs_clock_sync_packets = []
adcs_tracker_packets = []
adcs_refs_packets = []
adcs_time_packets = []
adcs_imu_packets = []
adcs_cal_packets = []
adcs_att_det_packets = []
adcs_tracker_ctrl_packets = []
adcs_att_ctrl_packets = []
adcs_tables_packets = []
adcs_general_packets = []
adcs_att_cmd_packets = []
adcs_tracker2_packets = []
adcs_tlm_proc_packets = []
adcs_ext_tracker2_packets = []
adcs_rw_drive_packets = []
adcs_momentum_packets = []
adcs_css_packets = []
adcs_mag_packets = []
adcs_command_tlm_packets = []
cip_soh_packets = []
cip_sci1_packets = []
cip_sci2_packets = []
daxss_log_packets = []
daxss_sci_packets = []
adcs_l0_packets = []


# Creating a list of integers from the raw output file from Hydra
int_list = []
with open("hydra_log", "rb") as f:
    while True:
        byte = f.read(1)
        if not byte:
            break
        int_list.append(int(ord(byte)))

# Scanning through the list to look for different types of packets
array_index = 0
while (array_index<len(int_list)):
    packet_apid = int_list[array_index+1]
    packet_length = 256*int_list[array_index+4] + int_list[array_index+5]
    if(packet_apid == apid_beacon):
        num_beacon = num_beacon + 1
        beacon_packets.append(list(int_list[array_index:array_index+packet_length+7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_des_hk):
        num_des_hk = num_des_hk + 1
        des_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_des_task):
        num_des_task = num_des_task + 1
        des_task_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_des_sched):
        num_des_sched = num_des_sched + 1
        des_sched_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_des_time):
        num_des_time = num_des_task + 1
        des_time_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_mem_dump):
        num_mem_dump = num_mem_dump + 1
        mem_dump_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_fp_hk):
        num_fp_hk = num_fp_hk + 1
        fp_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_lib_hk):
        num_lib_hk = num_lib_hk + 1
        lib_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_tbl_hk):
        num_tbl_hk = num_tbl_hk + 1
        tbl_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_seq_hk):
        num_seq_hk = num_seq_hk + 1
        seq_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_tlm_hk):
        tlm_hk_hk = num_fp_hk + 1
        tlm_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_cmd_hk):
        num_cmd_hk = num_cmd_hk + 1
        cmd_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_time_hk):
        num_time_hk = num_time_hk + 1
        time_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_sband_hk):
        num_sband_hk = num_sband_hk + 1
        sband_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_sd_hk):
        num_sd_hk = num_sd_hk + 1
        sd_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_uhf_hk):
        num_uhf_hk = num_uhf_hk + 1
        uhf_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_uhf_pass):
        num_uhf_pass = num_uhf_pass + 1
        uhf_pass_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_cip_hk):
        num_cip_hk = num_cip_hk + 1
        cip_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_cip_msg_hk):
        num_cip_msg_hk = num_cip_msg_hk + 1
        cip_msg_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_mode_hk):
        num_mode_hk = num_mode_hk + 1
        mode_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_daxss_msg_hk):
        num_daxss_msg_hk = num_daxss_msg_hk + 1
        daxss_msg_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_daxss_hk):
        num_daxss_hk = num_daxss_hk + 1
        daxss_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_ana_hk):
        num_ana_hk = num_ana_hk + 1
        ana_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_msg_hk):
        num_adcs_msg_hk = num_adcs_msg_hk + 1
        adcs_msg_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_hk):
        num_adcs_hk = num_adcs_hk + 1
        adcs_hk_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_analogs):
        num_adcs_analogs = num_adcs_analogs + 1
        adcs_analogs_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_gps):
        num_adcs_gps = num_adcs_gps + 1
        adcs_gps_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_clock_sync):
        num_adcs_clock_sync = num_adcs_clock_sync + 1
        adcs_clock_sync_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_tracker):
        num_adcs_tracker = num_adcs_tracker + 1
        adcs_tracker_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7
    #Add the remaining packets here from adcs_refs to the end

    elif(packet_apid == apid_adcs_refs):
        num_adcs_refs = num_adcs_refs + 1
        adcs_refs_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_time):
        num_adcs_time = num_adcs_time + 1
        adcs_time_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_imu):
        num_adcs_imu = num_adcs_imu + 1
        adcs_imu_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_cal):
        num_adcs_cal = num_adcs_cal + 1
        adcs_cal_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_att_det):
        num_adcs_att_det = num_adcs_att_det + 1
        adcs_att_det_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_tracker_ctrl):
        num_adcs_tracker_ctrl = num_adcs_tracker_ctrl + 1
        adcs_tracker_ctrl_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_att_ctrl):
        num_adcs_att_ctrl = num_adcs_att_ctrl + 1
        adcs_att_ctrl_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_tables):
        num_adcs_tables = num_adcs_tables + 1
        adcs_tables_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_general):
        num_adcs_general = num_adcs_general + 1
        adcs_general_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_att_cmd):
        num_adcs_att_cmd = num_adcs_att_cmd + 1
        adcs_att_cmd_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_tracker2):
        num_adcs_tracker2 = num_adcs_tracker2 + 1
        adcs_tracker2_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_tlm_proc):
        num_adcs_tlm_proc = num_adcs_tlm_proc + 1
        adcs_tlm_proc_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_ext_tracker2):
        num_adcs_ext_tracker2 = num_adcs_ext_tracker2 + 1
        adcs_ext_tracker2_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_rw_drive):
        num_adcs_rw_drive = num_adcs_rw_drive + 1
        adcs_rw_drive_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_momentum):
        num_adcs_momentum = num_adcs_momentum + 1
        adcs_momentum_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_css):
        num_adcs_css = num_adcs_css + 1
        adcs_css_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_mag):
        num_adcs_mag = num_adcs_mag + 1
        adcs_mag_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_command_tlm):
        num_adcs_command_tlm = num_adcs_command_tlm + 1
        adcs_command_tlm_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_cip_soh):
        num_cip_soh = num_cip_soh + 1
        cip_soh_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_cip_sci1):
        num_cip_sci1 = num_cip_sci1 + 1
        cip_sci1_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_cip_sci2):
        num_cip_sci2 = num_cip_sci2 + 1
        cip_sci2_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_daxss_log):
        num_daxss_log = num_daxss_log + 1
        daxss_log_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_daxss_sci):
        num_daxss_sci = num_daxss_sci + 1
        daxss_sci_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    elif(packet_apid == apid_adcs_l0):
        num_adcs_l0 = num_adcs_l0 + 1
        adcs_l0_packets.append(list(int_list[array_index:array_index + packet_length + 7]))
        array_index = array_index + packet_length + 7

    else:
        array_index = array_index + packet_length + 7


# writing the different types of packets to csv files
if num_beacon>0:
    with open('beacon_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in beacon_packets:
            writer.writerow(row)

if num_des_hk>0:
    with open('des_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in des_hk_packets:
            writer.writerow(row)

if num_des_task>0:
    with open('des_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in des_hk_packets:
            writer.writerow(row)

if num_des_sched>0:
    with open('des_task_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in des_task_packets:
            writer.writerow(row)

if num_des_time>0:
    with open('des_sched_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in des_sched_packets:
            writer.writerow(row)

if num_mem_dump>0:
    with open('des_time_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in des_time_packets:
            writer.writerow(row)

if num_des_hk>0:
    with open('mem_dump_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in mem_dump_packets:
            writer.writerow(row)

if num_fp_hk>0:
    with open('fp_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in fp_hk_packets:
            writer.writerow(row)

if num_log_hk>0:
    with open('log_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in log_hk_packets:
            writer.writerow(row)

if num_lib_hk>0:
    with open('lib_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in lib_hk_packets:
            writer.writerow(row)

if num_tbl_hk>0:
    with open('tbl_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in tbl_hk_packets:
            writer.writerow(row)

if num_seq_hk>0:
    with open('seq_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in seq_hk_packets:
            writer.writerow(row)

if num_tlm_hk>0:
    with open('tlm_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in tlm_hk_packets:
            writer.writerow(row)

if num_cmd_hk>0:
    with open('cmd_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in cmd_hk_packets:
            writer.writerow(row)

if num_time_hk>0:
    with open('time_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in time_hk_packets:
            writer.writerow(row)

if num_sband_hk>0:
    with open('sband_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in sband_hk_packets:
            writer.writerow(row)

if num_sd_hk>0:
    with open('sd_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in sd_hk_packets:
            writer.writerow(row)

if num_uhf_hk>0:
    with open('uhf_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in uhf_hk_packets:
            writer.writerow(row)

if num_uhf_pass>0:
    with open('uhf_pass_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in uhf_pass_packets:
            writer.writerow(row)

if num_cip_hk>0:
    with open('cip_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in cip_hk_packets:
            writer.writerow(row)

if num_cip_msg_hk>0:
    with open('cip_msg_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in cip_msg_hk_packets:
            writer.writerow(row)

if num_mode_hk>0:
    with open('mode_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in mode_hk_packets:
            writer.writerow(row)

if num_daxss_msg_hk>0:
    with open('daxss_msg_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in daxss_msg_hk_packets:
            writer.writerow(row)

if num_daxss_hk>0:
    with open('daxss_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in daxss_hk_packets:
            writer.writerow(row)

if num_ana_hk>0:
    with open('ana_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in ana_hk_packets:
            writer.writerow(row)

if num_adcs_msg_hk>0:
    with open('adcs_msg_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_msg_hk_packets:
            writer.writerow(row)

if num_adcs_hk>0:
    with open('adcs_hk_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_hk_packets:
            writer.writerow(row)

if num_adcs_analogs>0:
    with open('adcs_analogs_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_analogs_packets:
            writer.writerow(row)

if num_adcs_gps>0:
    with open('adcs_gps_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_gps_packets:
            writer.writerow(row)

if num_adcs_clock_sync>0:
    with open('adcs_clock_sync_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_clock_sync_packets:
            writer.writerow(row)

if num_adcs_tracker>0:
    with open('adcs_tracker_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_tracker_packets:
            writer.writerow(row)

if num_adcs_refs>0:
    with open('adcs_refs_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_refs_packets:
            writer.writerow(row)

if num_adcs_time>0:
    with open('adcs_time_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_time_packets:
            writer.writerow(row)

if num_adcs_imu>0:
    with open('adcs_imu_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_imu_packets:
            writer.writerow(row)

if num_adcs_cal>0:
    with open('adcs_cal_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_cal_packets:
            writer.writerow(row)

if num_adcs_att_det>0:
    with open('adcs_att_det_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_att_det_packets:
            writer.writerow(row)

if num_adcs_tracker_ctrl>0:
    with open('adcs_tracker_ctrl_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_tracker_ctrl_packets:
            writer.writerow(row)

if num_adcs_att_ctrl>0:
    with open('adcs_att_ctrl_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_att_ctrl_packets:
            writer.writerow(row)

if num_adcs_tables>0:
    with open('adcs_tables_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_tables_packets:
            writer.writerow(row)

if num_adcs_general>0:
    with open('adcs_general_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_general_packets:
            writer.writerow(row)

if num_adcs_att_cmd>0:
    with open('adcs_att_cmd_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_att_cmd_packets:
            writer.writerow(row)

if num_adcs_tracker2>0:
    with open('adcs_tracker2_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_tracker2_packets:
            writer.writerow(row)

if num_adcs_tlm_proc>0:
    with open('adcs_tlm_proc_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_tlm_proc_packets:
            writer.writerow(row)

if num_adcs_ext_tracker2>0:
    with open('adcs_ext_tracker2_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_ext_tracker2_packets:
            writer.writerow(row)

if num_adcs_rw_drive>0:
    with open('adcs_rw_drive_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_rw_drive_packets:
            writer.writerow(row)

if num_adcs_momentum>0:
    with open('adcs_momentum_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_momentum_packets:
            writer.writerow(row)

if num_adcs_css>0:
    with open('adcs_css_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_css_packets:
            writer.writerow(row)

if num_adcs_mag>0:
    with open('adcs_mag_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_mag_packets:
            writer.writerow(row)

if num_adcs_command_tlm>0:
    with open('adcs_command_tlm_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_command_tlm_packets:
            writer.writerow(row)

if num_cip_soh>0:
    with open('cip_soh_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in cip_soh_packets:
            writer.writerow(row)

if num_cip_sci1>0:
    with open('cip_sci1_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in cip_sci1_packets:
            writer.writerow(row)

if num_cip_sci2>0:
    with open('cip_sci2_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in cip_sci2_packets:
            writer.writerow(row)

if num_daxss_log>0:
    with open('daxss_log_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in daxss_log_packets:
            writer.writerow(row)

if num_daxss_sci>0:
    with open('daxss_sci_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in daxss_sci_packets:
            writer.writerow(row)

if num_adcs_l0>0:
    with open('adcs_l0_packets.csv', "w") as f:
        writer = csv.writer(f)
        for row in adcs_l0_packets:
            writer.writerow(row)



