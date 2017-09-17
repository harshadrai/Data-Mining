import sys
import math
my_list = []

for line in sys.stdin:
    my_list.append(list(line.strip().split(',')))


D_size=int(my_list[0][0])-1
del my_list[0]


classes={}
for i in my_list[1:]:
    if i[-1] in classes:
        classes[i[-1]]+=1
    else:
        classes[i[-1]]=1



Info_D = 0
for i in classes:
    pi=classes[i]/D_size
    Info_D += -pi*math.log2(pi)
    
def sum_of_Info_Dj(Info_Dj,value_sum):
    soidj=0
    for i in Info_Dj:
        pi=Info_Dj[i]/value_sum
        soidj += -pi*math.log2(pi)
    return soidj
    
def information_required_for_partitioning(atr_no,D_size, classes):
    attribute_values={}
    Info_A_D=0
    for i in my_list[1:]:
        if i[atr_no] in attribute_values:
            attribute_values[i[atr_no]]+=1
        else:
            attribute_values[i[atr_no]]=1
    for value in attribute_values:
        Info_Dj={}
        for i in my_list[1:]:
            if i[atr_no]==value:
                if i[-1] in Info_Dj:
                    Info_Dj[i[-1]]+=1
                else:
                    Info_Dj[i[-1]]=1
        soidj=sum_of_Info_Dj(Info_Dj,attribute_values[value])
        Info_A_D+=(attribute_values[value]/D_size)*soidj
    return Info_A_D

def split_information(atr_no,D_size):
    attribute_values={}
    Split_Info_A_D=0
    for i in my_list[1:]:
        if i[atr_no] in attribute_values:
            attribute_values[i[atr_no]]+=1
        else:
            attribute_values[i[atr_no]]=1
    for value in attribute_values:
        pi=attribute_values[value]/D_size
        Split_Info_A_D += -pi*math.log2(pi)
    return Split_Info_A_D
            
Gain=-1 
Gain_Ratio=-1

for atr_no, attribute in enumerate(my_list[0][:-1]):
    Info_A_D=information_required_for_partitioning(atr_no,D_size, classes)
    gain_A=Info_D-Info_A_D
    Split_Info_A_D=split_information(atr_no,D_size)
    gain_ratio_A=gain_A/Split_Info_A_D
    if gain_A>Gain:
        Gain=gain_A
        final_atr_no_for_info_gain=atr_no
    if gain_ratio_A > Gain_Ratio:
        Gain_Ratio=gain_ratio_A
        final_atr_no_for_gain_ratio=atr_no
        
print(my_list[0][final_atr_no_for_info_gain])
print(my_list[0][final_atr_no_for_gain_ratio])


    