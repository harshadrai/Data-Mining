import sys
essay = open(sys.argv[1], 'r')                         #open the file as a read only file under variable name essay
essayread = essay.readlines()                           #convert essay into a list under variable name essayread
#essayread[:]                                            #check out what essayread has, a longlist of paragraphs as strings
wordlist = [word.strip().split() for word in essayread] #remove blank spaces at beginning and end using strip,
                                                        #and converting each paragraph into a list of words as objects 
                                                        #by split, and storing each list with words of the para as objects
                                                        #within a list named wordlist
wordlist[:]
wordfinal = []                                          #creating an empty list to store each word as a string object
                                                        #in a single list
for i in range(len(wordlist)):
    for j in range(len(wordlist[i])):
        wordfinal.append(wordlist[i][j])

V = sorted(list(set(wordfinal)))                        #using set function to store each word only once and then using 
                                                        #list function to convert into a list and finally sorting the 
                                                        #list alphabetically


C=[]                                                  #creating an empty list called C (short for corpus) to store
                                                      #dictionaries of different documents with each dictionary
                                                      #containing all words in V as keys with the number of occurences of
                                                      #that word in the document as corresponding value
for i in range(0,len(wordlist)):
    mydict = {}
    for values in V:
        mydict[values]=(wordlist[i].count(values))
    C.append(mydict)


#Term Frequency
Ctf = []                                                    #List to store dictionaries containing term frequencies of 
                                                            #each word in each document in corpus(Ctf = short for Corpus term frequency)
for i in range(len(wordlist)):
    mydict = {}
    for values in V:
        mydict[values]= ((C[i][values])/(len(wordlist[i])))
    Ctf.append(mydict)


#Inverse Document Frequency
No_of_documents_with_term_t = {}               #Dictionary that stores no. of documents that a term appears in
for value in V:
    no_of_docs_with_term_t=0
    for i in range(len(wordlist)):      
        if (wordlist[i].count(value))>0:
            no_of_docs_with_term_t+=1
    No_of_documents_with_term_t[value]=no_of_docs_with_term_t


from math import log
Inverse_document_frequency = {}                      #Dictionary that stores inverse document frequency for each term
for values in V:
    Inverse_document_frequency[values]= log((len(wordlist))/(No_of_documents_with_term_t[values]))


#tf-idf Vector
D = []                                              #Final list containing|V|dimensional vector d = (d1; d2; ::::; d|V|)
                                                    #di = tf (Vi;D)  idf(Vi)
                                                    #d is the tf-idf vector for D 
for i in range(len(wordlist)):
    d = {}
    for values in V:
        d[values]= ((Ctf[i][values])*(Inverse_document_frequency[values]))
    D.append(d)


#Minkowski h=1 distance
minkowskih1=[]
for i in range((len(wordlist))):
    result=0
    for value in V:
        result += abs((D[i][value])-D[(len(D)-1)][value])
    if int(result)-result==0.0:
        minkowskih1.append(result)
    else:
        minkowskih1.append(round(result,3))


#Minkowski h=2 distance
from math import pow
from math import sqrt
minkowskih2=[]
for i in range((len(wordlist))):
    result=0
    for value in V:
        result += pow(((D[i][value])-D[(len(D)-1)][value]),2)
    result=round(sqrt(result),3)
    if int(result)-result==0.0:
        minkowskih2.append(result)
    else:
        minkowskih2.append(round(result,3))


#Minkowski hinfinity distance
minkowskihinfinity=[]
for i in range((len(wordlist))):
    result=0
    x=0
    for value in V:
        x = abs((D[i][value])-(D[(len(D)-1)][value]))
        if x>result:
            result=x
    if int(result)-result==0.0:
        minkowskihinfinity.append(result)
    else:
        minkowskihinfinity.append(round(result,3))


#Cosine Similarity
cosine=[]
m=0
for value in V:
    m+=(pow((D[(len(D)-1)][value]),2))
for i in range((len(wordlist))):
    k=0
    l=0
    for value in V:
        k+=((D[i][value])*(D[(len(D)-1)][value]))
        l+=(pow((D[i][value]),2))
    result=(k)/(sqrt(l)*sqrt(m))
    if int(result)-result==0.0:
        cosine.append(result)
    else:
        cosine.append(round(result,3))


#5 min. distance documents for minkowski h1
minkowskih1min5=[]
for i in range(5):
    minkowskih1min5.append((minkowskih1.index(min(minkowskih1)))+1)
    minkowskih1[(minkowskih1.index(min(minkowskih1)))]=1e34


#5 min. distance documents for minkowski h2
minkowskih2min5=[]
for i in range(5):
    minkowskih2min5.append((minkowskih2.index(min(minkowskih2)))+1)
    minkowskih2[(minkowskih2.index(min(minkowskih2)))]=1e34


#5 min. distance documents for minkowski hinfinity
minkowskihinfinitymin5=[]                    #List to find the 5 min distance documents
for i in range(5):
    minkowskihinfinitymin5.append((minkowskihinfinity.index(min(minkowskihinfinity)))+1)   #adds doc. no. with min distance
    minkowskihinfinity[(minkowskihinfinity.index(min(minkowskihinfinity)))]=1e34       #replaces value of doc with min distance with a very high value so that it does not show up as the min. in next iteration


#5 min. distance documents for cosine
cosinemax5=[]
for i in range(5):
    cosinemax5.append((cosine.index(max(cosine)))+1)
    cosine[(cosine.index(max(cosine)))]=-1e34


#PCA and Euclidean distance
listofdocs = []                                              #Final list containing|V|dimensional vector d = (d1; d2; ::::; d|V|)
                                                    #di = tf (Vi;D)  idf(Vi)
                                                    #d is the tf-idf vector for D 
for i in range(len(wordlist)):
    doc = []
    for values in V:
        doc.append((Ctf[i][values])*(Inverse_document_frequency[values]))
    listofdocs.append(doc)


#PCA transformation using scikit learn
from sklearn.decomposition import PCA
abcd = PCA(n_components=2,svd_solver = 'full')
transformeddocs=abcd.fit_transform(listofdocs)


#Eucledian distance for transformed data
from math import pow
from math import sqrt
pcaeucledian=[]
for i in range((len(wordlist))):
    result=0
    for j in range(2):
        result += pow(((transformeddocs[i][j])-(transformeddocs[((len(transformeddocs))-1)][j])),2)
    result=sqrt(result)
    if int(result)-result==0.0:
        pcaeucledian.append(result)
    else:
        pcaeucledian.append(round(result,3))


#Docs with min distance after PCA
pcaeucledianmin5=[]
for i in range(5):
    pcaeucledianmin5.append((pcaeucledian.index(min(pcaeucledian)))+1)
    pcaeucledian[(pcaeucledian.index(min(pcaeucledian)))]=1e34


print(len(V),'\n')
print(minkowskih1min5[0],' ',minkowskih1min5[1],' ',minkowskih1min5[2],' ',minkowskih1min5[3],' ',minkowskih1min5[4],'\n')
print(minkowskih2min5[0],' ',minkowskih2min5[1],' ',minkowskih2min5[2],' ',minkowskih2min5[3],' ',minkowskih2min5[4],'\n')
print(minkowskihinfinitymin5[0],' ',minkowskihinfinitymin5[1],' ',minkowskihinfinitymin5[2],' ',minkowskihinfinitymin5[3],' ',minkowskihinfinitymin5[4],'\n')
print(cosinemax5[0],' ',cosinemax5[1],' ',cosinemax5[2],' ',cosinemax5[3],' ',cosinemax5[4],'\n')
print(pcaeucledianmin5[0],' ',pcaeucledianmin5[1],' ',pcaeucledianmin5[2],' ',pcaeucledianmin5[3],' ',pcaeucledianmin5[4],'\n')