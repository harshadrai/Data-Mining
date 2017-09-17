import sys
import itertools
my_list = []

for line in sys.stdin:

    data=line.lower().strip().replace(' a ',' ').replace(' an ',' ').replace(' are ',' ').replace(' as ',' ').replace(' at ',' ').replace(' by ',' ').replace(' be ',' ').replace(' for ',' ').replace(' from ',' ').replace(' has ',' ').replace(' he ',' ').replace(' in ',' ').replace(' is ',' ').replace(' it ',' ').replace(' its ',' ').replace(' of ',' ').replace(' on ',' ').replace(' that ',' ').replace(' the ',' ').replace('the ','').replace(' to ',' ').replace(' was ', '').replace(' were ',' ').replace(' will ',' ').replace(' with ',' ').replace('.','').replace(', and ','$').replace(', ','$').replace(' and ','$').split(' ')
    my_list.append(data)

     
min_support = int(my_list[0][0])
del my_list[0]      


my_list1=[]
for i in my_list:
    temp_list=[]
    for j in i:
        temp_list.append(j.split('$'))
    my_list1.append(temp_list)
    
my_list=my_list1[:]
del my_list1
del temp_list


database={}
for sid in range(len(my_list)):
    for eid in range(len(my_list[sid])):

        if sid in database:
            database[sid][eid]=sorted([item for item in my_list[sid][eid]])
        else:
            database[sid]={eid:sorted([item for item in my_list[sid][eid]])}
        
#single frequent items
items=[]
for i in range(len(my_list)):
    for j in range(len(my_list[i])):
        for k in range(len(my_list[i][j])):
            items.append(my_list[i][j][k])
        
items=sorted(list(set(items)))


item_count={}

for key in items:
    for i in range(len(my_list)):
        for j in range(len(my_list[i])):
 
            if key in my_list[i][j]:
                if key in item_count:
                    item_count[key]+=1
                    break
                else:
                    item_count[key]=1
                    break
                    
shortlisted_items=[]
useless_items=[]
                
for key in item_count:
    if item_count[key] >= min_support:
        shortlisted_items.append(key)
    else:
        useless_items.append(key)
        
shortlisted_items.sort()
for item in useless_items:
    del item_count[item]
    items.remove(item)
    for sid in database:
        for eid in database[sid].keys():
            if item in database[sid][eid]:
                database[sid][eid].remove(item)


def frequent_single_items(min_support):
    singles_list=[]
    for perms in singles:
        for i in range(len(my_list)):
            for j in range(len(my_list[i])):
                check=True
                for things in perms:
                    if things not in my_list[i][j]:
                        check = False
                        break
                if check==True:
                    singles_list.append(perms)
                    break
            #if check==True:
                #break
        
    singles_count=[]
    for i in singles:
        if i in singles_list:
            singles_count.append((i,singles_list.count(i)))

    shortlisted_single_items=[]
    shortlisted_single_items_count=[]
    for i in singles_count:
        if i[1]>=min_support:
            shortlisted_single_items.append(i[0])
            shortlisted_single_items_count.append(i[1])
    return shortlisted_single_items,shortlisted_single_items_count
        
def frequent_multiple_items(min_support):
    multiples_list=[]
    for sequence in my_list:
        final_temp_list=[]
        for i in range(len(multiples)):

            temp_list=[]
            temp_list1=[]
            event=0
            for j in range(len(multiples[i])):

                check=True
                variable_so_that_item_without_while_is_not_added=0

                while event<len(sequence):
                    if set(multiples[i][j])<=set(sequence[event]):
                        check=True
                        variable_so_that_item_without_while_is_not_added=1
                        break
                    else:
                        check=False
                        event+=1
                event+=1
                if check==True and variable_so_that_item_without_while_is_not_added==1:
                    temp_list.append(event)
                    temp_list1.append(multiples[i][j])
                else:
                    break
            if temp_list1==multiples[i]:
                final_temp_list.append(temp_list1)
        multiples_list.extend(final_temp_list)


    multiples_count=[]
    for i in multiples:
        if i in multiples_list:
            multiples_count.append((i,multiples_list.count(i)))

    shortlisted_multiple_items=[]
    shortlisted_multiple_items_count=[]
    for i in multiples_count:
        if i[1]>=min_support:
            shortlisted_multiple_items.append(i[0])
            shortlisted_multiple_items_count.append(i[1])
    return shortlisted_multiple_items,shortlisted_multiple_items_count



    
singles=list(itertools.combinations(items,2))
multiples=list(itertools.product([[i] for i in items],repeat=2))

for i in range(len(singles)):
    singles[i]=list(singles[i])
for i in range(len(multiples)):
    multiples[i]=list(multiples[i])


a,a_count= frequent_single_items(min_support)   
b,b_count=frequent_multiple_items(min_support)
#print(a,a_count)
#print(b, b_count)
count=3
while a or b:
    if len(a)==0:
        final_frequent_items=b[:]
        final_frequent_count=b_count[:]
    elif len(b)==0:
        final_frequent_items=a[:]
        final_frequent_count=a_count[:]
    singles=[]
    multiples=[]
    if len(a)==0 and len(b)!=0:
        
        for i in b:
            for j in b:
                if i[1:]==j[:-1]:
                    
                    multiples.append(list(i[0:1]+i[1:]+j[-1:]))
    elif len(a)!=0 and len(b)!=0:
        
        for i in b:
            for j in b:
                if i[1:]==j[:-1]:
                    multiples.append(list(i[0:1]+i[1:]+j[-1:]))
        for i in b:
            for j in a:
                if list(i[0:1]+[j]) not in multiples: 
                    multiples.append(list(i[0:1]+[j]))
                if list([j]+i[1:]) not in multiples: 
                    multiples.append(list([j]+i[1:]))
        singles=list(itertools.combinations(items,count))
        for i in range(len(singles)):
            singles[i]=list(singles[i])
        count+=1        
        a,a_count= frequent_single_items(min_support) 
    elif len(a)!=0 and len(b)==0:
        
        singles=list(itertools.combinations(items,count))
        for i in range(len(singles)):
            singles[i]=list(singles[i])
        count+=1        
        a,a_count= frequent_single_items(min_support) 
    b,b_count=frequent_multiple_items(min_support)

    

#print(b,b_count)

for i, j in zip(final_frequent_count,final_frequent_items):
    k=''
    for m in j:
        
        k+=str(m[0]) + ' '
    k=k.strip()
    print(i, '['+k+']')