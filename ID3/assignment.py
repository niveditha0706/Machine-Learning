'''
Created on Jun 8, 2016
@author: Niveditha
'''
import math
import re
import os
from Tools.Scripts.treesync import raw_input
'''
Function name: calculate_log
Description: calculates log value needed for entropy
'''
def calculate_log(tot_outcome, fav_outcome):
    if fav_outcome == 0:
        return 0
    else:
        return math.log(1 / (fav_outcome / tot_outcome), 2)
'''
Function name: cal_entropy
Description: calculates entropy
'''
def cal_entropy(tot_outcome, fav_outcome, count_0, count_1):
    entropy = (fav_outcome / tot_outcome) * (((count_0 / fav_outcome) * calculate_log(fav_outcome, count_0))
                                   + ((count_1 / fav_outcome) * calculate_log(fav_outcome, count_1)))
    return entropy
'''
Function name: calc_gain
Description: calculates F value for every partition and gain for every feature
'''
def calc_gain(array,n,sjn):
    entropy_T = 0.0
    target_attr = [item[size[1]] for item in array]

    cnt = [(i, target_attr.count(i)) for i in set(target_attr)]

    for i in range(len(cnt)):
        entropy_T += (cnt[i][1] / n) * calculate_log(n,cnt[i][1])
    entropy_features = []

    loop = 1;
    while loop <= size[1] - 1:
        temp_attr = [item[loop] for item in array]
        c = [(i, temp_attr.count(i)) for i in set(temp_attr)]
        innerloop = 0
        entropy_attr = 0.0
        while innerloop < len(c):
            target_count_0 = 0
            target_count_1 = 0
            for i in range(n):
                if (temp_attr[i] == c[innerloop][0]):
                    if (target_attr[i] == '0'):
                        target_count_0 += 1
                    elif (target_attr[i] == '1'):
                        target_count_1 += 1
            entropy_attr += cal_entropy(n, c[innerloop][1], target_count_0, target_count_1)
            innerloop += 1
        entropy_features.append([loop, entropy_attr])
        loop += 1
    gain_features = []
    gain = []
    for i in range(len(entropy_features)):
        gain_features.append([i + 1, entropy_T - entropy_features[i][1]])
    print (gain_features);
    for i in range(len(gain_features)):
        gain.append(gain_features[i][1])
    for i in range(len(gain_features)):
        if  gain_features[i][1] == max(gain):
            max_gain = gain_features[i]
    max_gain.append(sjn*max_gain[1])
    return max_gain

size = []
array = []
filename = []
i = 1
for s in raw_input('Enter names of the files dataset input-partition output-partition\n').strip('\n').split(' '):
    filename.append(str(s).strip('\s+'))
try:
    dataset = filename[0]
    input_partition = filename[1]
    output_partition = filename[2]
except IndexError:
    print ('Input not given in correct format.Please try again.\nFormat: dataset<space>input-partition<space>output-partition')
    exit(0)
if os.path.exists(dataset):
   with open(dataset, 'r') as fileobj1:
       try:
           header = fileobj1.readline().strip('\n')
           size.extend(re.split('\s+', header))
           size = [int(i) for i in size]
           while 1:
               line = fileobj1.readline().strip('\n')
               if not line: break
               line1 = str(i) + ' ' + line
               array.append(re.split('\s+', line1))
               i += 1
           fileobj1.close()
       except IOError:
           print("Could not read file:", dataset)
           exit(0)
else:
    print("The file name given for dataset does not exist")
    exit(0)
if os.path.exists(input_partition):
    with open(input_partition, 'r') as fileobj2:
        try:
            partition_file = [] #Entire data of partition file
            max_gain_f = []
            line = fileobj2.readline().strip('\n')
            while line:
                temp_array = []
                partition = []
                partition.extend(re.split('\s+', line))
                partition_file.append(partition)
                if not line: break
                for i in range(1, len(partition)):
                    for k in range(size[0]):
                        if partition[i] == array[k][0]:
                            temp_array.append(array[k])
                            break
                sjn = (len(partition) - 1) / size[0]
                max_gain = calc_gain(temp_array, len(partition) - 1, sjn)
                max_gain.append(partition[0])
                max_gain_f.append(max_gain) # contains the feature number with max gain, gain,F value, and the partition number with max F value
                line = fileobj2.readline().strip('\n')
            fileobj2.close()
            f = []
            for i in range(len(max_gain_f)):
                f.append(max_gain_f[i][2])
            for i in range(len(max_gain_f)):
                if max_gain_f[i][2] == max(f):
                    max_f_gain_attr = max_gain_f[i]
            if max_f_gain_attr[1] == 0:
                exit(0)
            else:
                partition_to_split = [] #partition to be split
                temp_array_to_split = [] #dataset to be used for split
                for m in range(len(partition_file)):
                    if (partition_file[m][0] == max_f_gain_attr[3]):
                        partition_to_split.extend(partition_file[m])
                        break
                for i in range(1, len(partition_to_split)):
                    for k in range(size[0]):
                        if partition_to_split[i] == array[k][0]:
                            temp_array_to_split.append(array[k])
                            break
                values_in_attr_to_split = [(i) for i in set([item[max_f_gain_attr[0]] for item in temp_array_to_split])]
                loop = 0
                fileobj3 = open(output_partition, "w+")
                for i in range(len(partition_file)):
                    if (partition_file[i][0] != partition_to_split[0]):
                        str_to_write = ''
                        for n in range((len(partition_file[i]))):
                            str_to_write = str_to_write + partition_file[i][n] + ' '
                        str_to_write = str_to_write.rstrip()
                        fileobj3.write(str_to_write)
                        fileobj3.write('\n')
                replacement_partition = []
                while loop < len(values_in_attr_to_split):
                    temp_partition = []
                    for i in range(len(temp_array_to_split)):
                        if (temp_array_to_split[i][max_f_gain_attr[0]] == values_in_attr_to_split[loop]):
                            temp_partition.append(temp_array_to_split[i][0])
                    partition_name = 'Z' + str(loop + 1)
                    replacement_partition.append(partition_name)
                    fileobj3.write(partition_name)
                    for i in range(len(temp_partition)):
                        fileobj3.write(' ' + temp_partition[i])
                    fileobj3.write('\n')
                    loop += 1
                fileobj3.close()
                print("Partition ", partition_to_split[0], " was replaced with partitions ", end='')
                for r in replacement_partition:
                    print(r, " ", end='')
                print("using Feature ", max_f_gain_attr[0])
        except IOError:
            print("Could not read file:", input_partition)
            exit(0)
else:
    print("The file name given for input-partition does not exist")
    exit(0)