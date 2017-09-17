import sys
from math import ceil, floor
import itertools

my_list = []

for line in sys.stdin:
    data=line.strip().split(' ')
    my_list.append(data)
    

partitions = int(my_list[0][0])
size = len(my_list[1])/partitions



final_array = []



if len(my_list[1])%partitions == 0:
    l=0
    for p in range(partitions):
        part_list2 = []
        for k in range(1, len(my_list)):
            part_list=[]
            for i in range(int(size)):
                part_list.append(my_list[k][l+i])
            part_list2.append(part_list)
        final_array.append(part_list2)
        l=l+int(size)
elif len(my_list[1])%partitions !=0:
    remainder=len(my_list[1])%partitions
    count=0
    l=0
    while remainder>0:
        count+=1
        part_list2 = []
        
        for k in range(1, len(my_list)):
            part_list=[]
            for i in range(int(ceil(size))):
                part_list.append(my_list[k][l+i])
            part_list2.append(part_list)
        l+=int(ceil(size))
        final_array.append(part_list2)
        remainder-=1


    for p in range(partitions-count):
        part_list2 = []
        for k in range(1, len(my_list)):
            part_list=[]
            for i in range(int(floor(size))):
                part_list.append(my_list[k][l+i])
            part_list2.append(part_list)
        final_array.append(part_list2)
        l=l+int(floor(size))


count=1

for parts in final_array:
    my_dict={}
    for i in range(len(parts[0])):
        for j in range(len(parts)):
            if parts[j][i] in my_dict:
                my_dict[parts[j][i]] += 1
            else:
                my_dict[parts[j][i]] = 1
    for i in range(len(parts[0])):
        temp_list=[]
        for j in range(len(parts)):
            temp_list.append(parts[j][i])
        for key in sorted(set(temp_list)):
            print(key , ':',my_dict[key])
    
    master_list=[] 
    for j in range(0,len(parts)):
        temp_list=[]
        for L in range(2, len(parts[0])+1):
            subset = list(itertools.combinations(parts[j], L))
            
            temp_list.append(subset)
        master_list.append(temp_list)
         
   
    my_dict={}
    final_list=[]
    for j in range(len(master_list[0])):
        
        for k in range(len(master_list[0][j])):
            temp_list=[]
            for l in range(len(master_list)):
                letter=''
                for m in range(len(master_list[l][j][k])):
                    letter += str(master_list[l][j][k][m]) + ' '
                if letter.strip() in my_dict:
                    my_dict[letter.strip()] += 1
                else:
                    my_dict[letter.strip()] = 1
                temp_list.append(letter.strip())
            final_list.append(sorted(set(temp_list)))

    for i in range(len(final_list)):
        for j in range(len(final_list[i])):
            print(final_list[i][j],':',my_dict[final_list[i][j]] )
    
    if count < partitions:
        print()
    count+=1