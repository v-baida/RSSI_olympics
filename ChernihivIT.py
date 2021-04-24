import csv
import re
import time
import datetime
import matplotlib.pyplot as plt

input_file_name = 'F:/GitHub/RSSI_olympics/data-2-1.csv'
output_file_name = input_file_name.split('/')
output_file_name = output_file_name[3].split('.')
output_file_name = output_file_name[0]
# print(output_file_name[3])

output_file = open(f'F:/GitHub/RSSI_olympics/{output_file_name}.txt', 'w')

def getSeconds(obj):
    time_list = obj.split(":")
    minutes = time_list[0]
    time_list = time_list[1].split(".")
    seconds = time_list[0]
    # milliseconds = time_list[1]
    return int(seconds) + int(minutes) * 60

def findTwoMaxIndices(obj):
    # print(len(obj))
    temp = obj.copy()
    max1 = temp.index(max(temp)) 
    temp[max1] = -1000
    max2 = temp.index(max(temp)) 
    return max1+1, max2+1

def checkMaxIndices(max1, max2, b1, b2):
    if (max1 == b1 and max2 == b2) or (max1 == b2 and max2 == b1):
        return True
    else:
        return False

with open(input_file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    data_list = []
    for row in csv_reader:
        data_list.append(row[3:])

    i = 0
    j = 0

    b_reserv = [0,0,0,0,0,0]
    room_number = 5
    line_to_write = ""
    line_to_write_prev = ""

    while i+j < len(data_list):

        secs_start = getSeconds(data_list[i][2])
        secs = getSeconds(data_list[i][2])
        j = 0
        
        i_jump = 0

        b_sum = [0, 0, 0, 0, 0, 0]
        b_cnt = [0, 0, 0, 0, 0, 0]
        b_avg = [0, 0, 0, 0, 0, 0]

        while i+j < len(data_list) and secs <= secs_start + 5:

            secs = getSeconds(data_list[i+j][2])

            if secs <= secs_start + 3:
                i_jump = j

            ID = int(data_list[i+j][0])

            b_cnt[ID-1] = b_cnt[ID-1] + 1
            b_sum[ID-1] = b_sum[ID-1] + int(data_list[i+j][1])
            j = j+1
        
        i = i + i_jump
        for k in range(6):
            if b_cnt[k] != 0:
                b_avg[k] = int(b_sum[k]/b_cnt[k])
            else: 
                b_avg[k] = b_reserv[k]
        b_reserv = b_avg.copy()
        max1, max2 = findTwoMaxIndices(b_avg)

        sensor_number = 0

        if checkMaxIndices(max1, max2, 3, 4):
            room_number = 1
        elif checkMaxIndices(max1, max2, 3, 6):
            room_number = 1
        elif checkMaxIndices(max1, max2, 5, 6):
            room_number = 2 
        elif checkMaxIndices(max1, max2, 1, 6):
            room_number = 3
        elif checkMaxIndices(max1, max2, 2, 1):
            room_number = 3
        elif checkMaxIndices(max1, max2, 2, 5):
            room_number = 3 

        b_max_ind = b_avg.index(max(b_avg))
        
        if b_avg[b_max_ind] > -52:
            sensor_number = b_max_ind + 1

        line_to_write = "C%d" % room_number
        # output_file.write("C%d" % room_number)

        print(b_avg)

        if sensor_number != 0:
            # output_file.write(" B%d\n" % sensor_number)
            line_to_write = "%s B%d\n" % (line_to_write, sensor_number) 
        else:
            # output_file.write("\n")
            line_to_write = "%s\n" % line_to_write

        if (line_to_write != line_to_write_prev):
            output_file.write("%s" % line_to_write)
        line_to_write_prev = line_to_write
   






      

   


