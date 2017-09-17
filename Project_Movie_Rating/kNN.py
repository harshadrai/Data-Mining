#Load Packages
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances

#Load user, movie and train files as dataframes
movie_df = pd.read_csv('movie.txt', sep='\t' )
user_df = pd.read_csv('user.txt', sep='\t' )
train_df = pd.read_csv('train.txt', sep='\t' )

#We modify the movie dataframe to contain columns for each genre so that each genre is a feature by itself and we delete the original Genre column
movie_df['Genre']=movie_df['Genre'].astype(str)             #Convert the Genre column into string type

genre=[]                                                    #Create an empty list to store lists containing genre names for different movis
for index, row in movie_df.iterrows():                      #Loop over all the rows in the movie dataframe
    genre.append(row['Genre'].strip().split('|'))           #Remove blank spaces from the values in Genre and split it at | to form lists and append it to the genre list
temp=[]                                                     #Create and an empty list temp to store all genre names
for i in genre:                                             #Loop over the lists stores in genre
    for j in i:                                             #Loop over the values in these lists
        temp.append(j.strip())                              #Remove blank spaces if any and append it to temp
genre=temp[:]                                               #Store all values of temp in genre
del temp                                                    #Delete temp as it is no longer required
genre=sorted(set(genre))                                    #Use set() to store only unique genre names
genre.remove('nan')                                         #Remove nan values

for i in genre:                                             #Loop over all genre names stored in the list genre
    movie_df[i]=0                                           #Create a column for each of these genres in the movie dataframe and intialize to zero

for index, row in movie_df.iterrows():                      #Loop over each row of movie dataframe
    genre_name=[]                                           #Create an empty list genre_name to store genres for each movie
    genre_name.append(row['Genre'].strip().split('|'))      #Remove blank spaces from the values in Genre and split it at | to form lists and append it to the genre_name list
    for i in genre_name[0]:                                 #Loop over the genres in genre_name
        if i.strip() != 'nan':                              #If the name is not equal to nan
            movie_df.set_value(index,i.strip(),1)           #Set the value for the corresponding genre column in movie dataframe to 1

del movie_df['Genre']                                       #Delete the Genre column from movie dataframe

#Updating the user dataframe
user_df.replace('M', 1, inplace=True)                       #Changing M to 1 in Gender column of user dataframe
user_df.replace('F', 2, inplace=True)                       #Changing F to 2 in Gender column of user dataframe

#Changing column names in user and movie dataframe to better suit the merging with the tran dataframe
names = user_df.columns.tolist()                            #Add column names from user dataframe to a list called names
names[names.index('ID')] = 'user-Id'                        #Change the value at the index of value 'ID' to 'user-Id'
user_df.columns = names                                     #Update the column names in user_df to the updates names in the names list

names = movie_df.columns.tolist()                           #Add column names from movie dataframe to a list called names
names[names.index('Id')] = 'movie-Id'                       #Change the value at the index of value 'Id' to 'user-Id'
movie_df.columns = names                                    #Update the column names in movie_df to the updates names in the names list

#Merging user and train dataframe on 'user-Id' to form new dataframe called temp_df
temp_df=(pd.merge(user_df,train_df , on ='user-Id' ))

#Merging temp_df and movie_df on 'movie-Id' to form new dataframe called final_train_df
final_train_df = pd.merge(temp_df, movie_df, on ='movie-Id')

#Update final_train_df
del final_train_df['movie-Id']                              #Delete movie-Id column from final_train_df
del final_train_df['user-Id']                               #Delete user-Id from final_train_df
final_train_df.sort_values(by='Id', inplace=True)           #Sort the final_train_df dataframe by Id
final_train_df.set_index('Id',inplace=True)                 #Make Id as the index of final_train_df dataframe

#Normalizing the columns
cols_to_norm = ['Gender', 'Age', 'Occupation', 'Year']      #Make a list of the columns to normalize
final_train_df[cols_to_norm] = final_train_df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()) + 0.5)      
#The upper line normalizes the columns given in list cols_to_norm using a lambda function such that the range of the normalized values is from 0.5 to 1.5

final_train_df.replace('NaN', 0, inplace=True)              #Replace NaN values by 0 in final_train_df

#Make rating the last column in final_train_df
columns = list(final_train_df.columns.values)               #List of all the columns in final_train_df
columns.pop(columns.index('rating'))                        #Remove rating from the columns list
final_train_df = final_train_df[columns+['rating']]         #Create new dataframe with columns in the order you want

#Load the test dataframe
test_df = pd.read_csv('test.txt', sep='\t')

del temp_df                                                 #Delete the temp_df dataframe
temp_df=(pd.merge(user_df,test_df , on ='user-Id' ))        #Merge the user dataframe and test dataframe on 'user-Id' and create new dataframe called temp_df
final_test_df = pd.merge(temp_df, movie_df, on ='movie-Id') #Merge temp_df and movie_df on 'movie-Id' and store in final_test_df

final_test_df.sort_values(by='Id', inplace=True)            #Sort final_test_df by Id
del final_test_df['movie-Id']                               #Delete movie-Id column from final_test_df
del final_test_df['user-Id']                                #Delete user-Id column from final_test_df
final_test_df.set_index('Id',inplace=True)                  #Make Id as the index of final_test_df

del test_df                                                 #Delete test_df
del temp_df                                                 #Delete temp_df
del user_df                                                 #Delete user_df
del movie_df                                                #Delete movie_df
del train_df                                                #Delete train_df

final_test_df['rating']=0                                   #Create column rating in final_test_df and initialize it to zero


#Normalize the columns
cols_to_norm = ['Gender', 'Age', 'Occupation', 'Year']      #Make a list of the columns to normalize
final_test_df[cols_to_norm] = final_test_df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min())+ 0.5)
#The upper line normalizes the columns given in list cols_to_norm using a lambda function such that the range of the normalized values is from 0.5 to 1.5

final_test_df.replace('NaN', 0, inplace=True)               #Replace NaN in final_test_df by zero

#Creating arrays for final_train_df and final_test_df
train_data = final_train_df.values
test_data = final_test_df.values

#Finding 15 nearest neighbors and using majority vote to obtain ratings in final_test_df
test_cols , m = final_test_df.shape                         #Store number of rows in test_cols
for i in range(test_cols):
    cos_dist=pairwise_distances(train_data[:,:-1],test_data[i,:-1].reshape(1,-1), metric="cosine") 
    #The previous line finds the cosine distance of a row in the final_test_df with all the rows in the final_train_df
    closest_neighbors = cos_dist[:,0].argsort()[:15]     
    #The previous line gets the indices of the 15 closest neighbors and stores them in closest_neighbors
    final_test_df.iloc[i, final_test_df.columns.get_loc('rating')] = final_train_df.iloc[closest_neighbors]['rating'].value_counts().idxmax() 
    #The previous line gets the ratings of all the closest neighbors, then counts (.value_counts()) the number of times each value occurs
    #and then gives the value corresponding to maximum count (.idmax()) and stores it in k

final_test_df.reset_index(level=0, inplace=True)            #Resetting the Id as the index in the final_test_df

#Deleting all unnecessary columns from final_test_df
del final_test_df['Gender']
del final_test_df['Age']
del final_test_df['Occupation']
del final_test_df['Year']
del final_test_df['Action']
del final_test_df['Adventure']
del final_test_df['Animation']
del final_test_df["Children's"]
del final_test_df['Comedy']
del final_test_df['Crime']
del final_test_df['Documentary']
del final_test_df['Drama']
del final_test_df['Fantasy']
del final_test_df['Film-Noir']
del final_test_df['Horror']
del final_test_df['Musical']
del final_test_df['Mystery']
del final_test_df['Romance']
del final_test_df['Sci-Fi']
del final_test_df['Thriller']
del final_test_df['War']
del final_test_df['Western']

#Saving the final_test_df as a .txt file
final_test_df.to_csv('Final_kNN15_Sol.txt', index=False)