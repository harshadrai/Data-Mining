import sys
import itertools
my_list = []

for line in sys.stdin:
    data=line.strip().split(' ')
    my_list.append(data)
    
items=[]
min_support = int(my_list[0][0])
del my_list[0]

#single frequent items
for i in range(len(my_list)):
    for j in range(len(my_list[i])):
        items.append(my_list[i][j])
        
items=sorted(list(set(items)))

item_count={}

for key in items:
    for i in range(len(my_list)):
        if key in my_list[i]:
            if key in item_count:
                item_count[key]+=1
            else:
                item_count[key]=1

shortlisted_items=[]
useless_items=[]
                
for key in item_count:
    if item_count[key] >= min_support:
        shortlisted_items.append(key)
    else:
        useless_items.append(key)
        
shortlisted_items.sort()
for key in useless_items:
    del item_count[key]
    
#single frequent items end

#generating all possible combinations

master_list=[]
for j in range(0,len(my_list)):
    temp_list=[]
    for L in range(2, len(my_list[j])+1):
        subset = list(itertools.combinations(sorted(my_list[j]), L))      
        temp_list.append(subset)
    master_list.append(temp_list)
    
super_final_list=[]

for j in range(len(master_list)):
    for k in range(len(master_list[j])):
        temp_list=[]
        for l in range(len(master_list[j][k])):
            letter=''
            for m in range(len(master_list[j][k][l])):
                letter += str(master_list[j][k][l][m]) + ' '
            temp_list.append(letter.strip())
        super_final_list.append(sorted(set(temp_list)))

master_list=super_final_list[:]
del super_final_list

#generating all possible combinations end

def has_infrequent_subset(c,L):
    c=c.split(' ')
    if (len(c)==2):#c[i] in L[0] for i in range(len(c))):
        for i in range(len(c)):
            if str(c[i]) not in L:
                return True
        return False
    else:
        subset = list(itertools.combinations(sorted(c), len(c)-1))
        temp_list=[]

        for m in range(len(subset)):
            letter=''
            for j in range(len(subset[m])):
                letter += str(subset[m][j]) + ' '
            temp_list.append(letter.strip())
        for s in temp_list:
            if s not in L:
                return True
        return False
    
    
def apriori_gen(L):
    Ck=[]

    for i in range(len(L)):
        for j in range(i+1,len(L)):
            if len(L[i].split(' '))==1:#len(list(L[i]))==1:
                c=str(L[i])+' '+str(L[j])
                if has_infrequent_subset(c,L):
                    continue
                else:
                    Ck.append(c)
            else:
                if L[i].split(' ')[:-1]==L[j].split(' ')[:-1]:
                    c=''
                    for item in L[i].split(' '):
                        c+=item+' '
                    c+=L[j].split(' ')[-1]
                    if has_infrequent_subset(c,L):
                        continue
                    else:
                        Ck.append(c)
    return Ck

L=[]
L.append(shortlisted_items)
C=[]

for k in itertools.count(1,1):

    if not L[k-1]:
        break
    
    Ck=apriori_gen(L[k-1])

    temp_dict={}
    temp_list=[]
    for c in Ck:

        for i in range(len(master_list)):
            for j in range(len(master_list[i])):
                if c==master_list[i][j]:
                    if c in temp_dict:
                        temp_dict[c] += 1
                    else:
                        temp_dict[c] = 1
    for key in temp_dict:
        if temp_dict[key] >= min_support:
            temp_list.append(key)
            item_count[key]=temp_dict[key]
    L.append(sorted(temp_list))



count_list=[] 
for key, value in item_count.items():
    count_list.append(value)
count_list=sorted(list(set(count_list)),reverse=True)

segregated_item_list=[]
for j in count_list:
    temp_list=[]
    for key, value in item_count.items():
        if value==j:
            temp_list.append(key)
    segregated_item_list.append(sorted(temp_list))
    
for i in segregated_item_list:
    for j in i:
        print(item_count[j],'['+j.strip()+']')

        
print()

#Closed Pattern Mining

closed_patterns=[]
for key,value in item_count.items():
    closed_patterns.append(key.strip().split())


closed_patterns=sorted(closed_patterns, key=len, reverse=True)


i=0
while i<len(closed_patterns):
    x=''
    for v in closed_patterns[i]:
        x+=v+' '
    x=x.strip()


    for j in range(1,len(closed_patterns[i])):

        subset = list(itertools.combinations(sorted(closed_patterns[i]), j))

        temp_list=[]

        for m in range(len(subset)):
            letter=''
            for j in range(len(subset[m])):
                letter += str(subset[m][j]) + ' '
            temp_list.append(letter.strip())

        for item in temp_list:
            if item_count[item]==item_count[x]:
                if item.strip().split(' ') in closed_patterns:
                    closed_patterns.remove(item.strip().split(' '))
    i+=1    

closed_patterns=sorted(closed_patterns)
final_closed_patterns=[]
for itemset in closed_patterns:
    letter=''
    for item in itemset:
        letter+=item+' '
    final_closed_patterns.append(letter.strip())
    
closed_patterns=final_closed_patterns[:]
del final_closed_patterns

for i in segregated_item_list:
    for items in i:
        if items in closed_patterns:
            print(item_count[items],'['+items.strip()+']')

print()

#Max Pattern Minning            
 
max_patterns=[]
for key,value in item_count.items():
    max_patterns.append(key.strip().split())


max_patterns=sorted(max_patterns, key=len, reverse=True)

i=0
while i<len(max_patterns):
    for j in range(1,len(max_patterns[i])):
        subset = list(itertools.combinations(sorted(max_patterns[i]), j))

        temp_list=[]

        for m in range(len(subset)):
            letter=''
            for j in range(len(subset[m])):
                letter += str(subset[m][j]) + ' '
            temp_list.append(letter.strip().split())


        for item in temp_list:
            if item in max_patterns:
                max_patterns.remove(item)
    i+=1    

max_patterns=sorted(max_patterns)
final_max_patterns=[]
for itemset in max_patterns:
    letter=''
    for item in itemset:
        letter+=item+' '
    final_max_patterns.append(letter.strip())
        
        
max_patterns=final_max_patterns[:]
del final_max_patterns


for i in segregated_item_list:
    for items in i:
        if items in max_patterns:
            print(item_count[items],'['+items.strip()+']')