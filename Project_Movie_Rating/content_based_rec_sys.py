#Load packages
import numpy as np
import pandas as pd

#Load movie file as dataframe
df=pd.read_csv('movie.txt', sep='\t')

#Make columns for each genre in movie dataframe
df['Genre']=df['Genre'].astype(str)								#Convert Genre column in movie dataframe to string type

genre=[]														#Create an empty list to store list containing genres of different movies
for index, row in df.iterrows():								#Loop over all rows in movie dataframe
    genre.append(row['Genre'].strip().split('|'))				#Removie blank spaces from values in Genre and split them at | and append this list to genre
temp=[]															#Create an empty list temp to store the genres
for i in genre:													#Loop over the lists in the list genre
    for j in i:													#Loop over each value in this list
        temp.append(j.strip())									#Append these values to the list temp
genre=temp[:]													#Store the values in temp in the list genre
del temp														#Delete the list temp
genre=sorted(set(genre))										#Use set() to store only distinct genre names in genre
genre.remove('nan')												#Remove nan from genre

movies={}														#Create an empty dictionary called movies to store movie ids as the keys and the corresponding value as an array containing the genre values of that movie
for index, row in df.iterrows():								#Loop over the movie dataframe
    temp_list=[]												#Create an empty list called temp_list to store the genre values of the movies
    temp_list.append(1)											#Append 1 so that it represents x_0 which is 1
    for g in genre:												#Loop over the genre names in list genre
        if row['Genre']=='nan':									#If the value in column Genre in the current row is a 'nan' 
            temp_list.append('nan')								#Append nan to the temp_list
        elif g in row['Genre'].strip().split('|'):				#Else if the genre name from list genre is part of the genres of current row(movie)
            temp_list.append(1)									#We append one 
        else:													#Else
            temp_list.append(0)									#We append zero showing that this movie is not of this genre
    movies[int(row['Id'])]=np.array(temp_list)					#We make the movie id as key in movies and the value temp_list as an array

#Load train file as dataframe
df2=pd.read_csv('train.txt', sep='\t')

#Creating a dictionary to store keys as user ids and corresponding values as dictionaries containing keys as movie-ids and values as ratings given by the user
movie_rating_by_user={}											#Creating empty dictionary called movie_rting_by_user
for index,row in df2.iterrows():								#Loop over the rows of train dataframe
    if row['user-Id'] in movie_rating_by_user:					#If user-Id in movie_rating_by_user	
        movie_rating_by_user[row['user-Id']][row['movie-Id']]=float(row['rating'])		#Store movie id and the rating in the dictionary corresponding to this key 
    else:														#Else if user id not in movie_rating_by_user
        movie_rating_by_user[row['user-Id']]={row['movie-Id']:float(row['rating'])}		#Store user id as key in movie_rating_by_user and movie id and the rating in the dictionary corresponding to this key

#Set theta values for each user to random integers between 1 and 5
#Load package
import random

user_theta={}													#Create empty dictionary to store user id as key and corrsponding values astheta values as lists
for key, values in movie_rating_by_user.items():				#Loop over key value pairs in movie_rating_by_user dictionary
    user_theta[key]=[0]											#Set the first theta value i.e. theta_0 as 0
    user_theta[key].extend(random.randint(1,5) for i in range(len(genre)))		#Extend this list with number of genres of random integers between 1 and 5

#Load the test file as a dataframe
df3=pd.read_csv('test.txt', sep='\t')

#Create a column called Rating and set values to 0
df3['Rating']=0   

#Creating empty dictionary called users_that_rated_movie which contains movie ids as keys and the user ids of the users that rated that movie as values
users_that_rated_movie={}
for index,row in df2.iterrows():                                            #Looping over rows of the train dataframe
    if row['movie-Id'] in users_that_rated_movie:                           #If the movie id is in the dictionary 
        users_that_rated_movie[row['movie-Id']].append(row['user-Id'])      #Append the user id to the list of users that rated that movie
    else:                                                                   #Else 
        users_that_rated_movie[row['movie-Id']]=[row['user-Id']]            #Add the movie id as the key and the user id in a list as value

#Import package to generate uniform random numbers
import numpy.random as npr

#Creating a dictionary called movie_feature to store movie ids that have no genre for them as keys and corresponding values as arrays containing random uniform numbers between 0 and 1 to have features for genres
movie_feature={}
for key, values in users_that_rated_movie.items():                          #Looping over keys (movie ids) in users_that_rated_movie
    if isinstance(movies[key][0], str):                                     #If genre of movie is a string (i.e. its nan)
        movie_feature[key]=[1]                                              #Append 1 first to represent x_0
        movie_feature[key].extend(npr.uniform() for i in range(len(genre))) #Then append uniform numbers between 0 and 1 as many as the genres
        movie_feature[key]=np.asarray(movie_feature[key])                   #Convert the list into an array

#Defining function to do linear regression using gradient descent to update theta values for user such that the error between the predicted and actual rating is reduced
def func1():
    for user in movie_rating_by_user.keys():                                #Looping over the user_ids
        alpha=0.0003                                                        #Taking a learning rate of 0.0003
        counter=0                                                           #Setting counter to zero
        x_movie=[]                                                          #Creating empty list to store features of movies
        rating=[]                                                           #Creating list to store ratings
        for i in movie_rating_by_user[user].keys():                         #Looping over the movie ids for this user_id
            if i in movies.keys() and not isinstance(movies[i][0], str):    #If movie id in movies dictionary and the value corresponding to this movie id is not a list of nans (i.e. movie does have genres) 
                x_movie.append(movies[i])                                   #Append the feature vector corresponding to the movie into the list x_movie
                rating.append(movie_rating_by_user[user][i])                #Append the rating corresponding to that movie and that user into rating
        x_movie=np.asarray(x_movie)                                         #Convert x_movie into an array
        rating=np.asarray(rating)                                           #Convert rating into an array
        while counter<2000:                                                 #Do the next part 2000 times so that error is reduced
            theta=np.array(user_theta[user])                                #Make an array called theta that stores theta values of the user
            user_theta[user]=theta-alpha*(np.dot(np.transpose(x_movie),(np.dot(x_movie, theta)-rating))) #Update the theta value using gradient descent
            counter+=1                                                      #Increase the counter

#Defining function to do linear regression using gradient descent to update feature vector for movies such that the error between the predicted and actual rating is reduced            
def func2():
    for movie in movie_feature.keys():                                      #Looping over the movie ids
        alpha=0.00003                                                       #Set learning rate to be 0.00003
        counter=0                                                           #Set counter to zero
        user_parameter=[]                                                   #Create an empty list user_parameter to store the theta values for the users
        rating=[]                                                           #Create an empty list to store the ratings
        for i in users_that_rated_movie[movie]:                             #Loop over the user ids of the users that rated this movie
            user_parameter.append(user_theta[i])                            #Append the theta values of the user into user_parameter
            rating.append(movie_rating_by_user[i][movie])                   #Append the corresponding rating into rating
        user_parameter=np.asarray( user_parameter )                         #Convert user_parameter into an array
        rating=np.asarray(rating)                                           #Convert rating into an array
        while counter<500:                                                  #Do the next part 500 times to reduce the error between the predicted and actual rating
            feature=np.array(movie_feature[movie])                          #Make an array called feature that stores feature vector of the movie
            movie_feature[movie]=feature-alpha*(np.dot(np.transpose(user_parameter),(np.dot( user_parameter, feature)-rating))) #Update the movie feature using gradient descent
            counter+=1                                                      #Increase the counter by 1
        movies[movie]=np.copy(movie_feature[movie])                         #Change the value corresponding to the movie in the movies dictionary to be this newly updated feature vector

#Calling the two functions alternatively 5 times to reduce as much error as possible 
counter=0                                                                   #Set counter as zero
while counter<5:                                                            #Do the next part 5 times
    func1()                                                                 #Call func1()
    func2()                                                                 #Call func2()
    counter+=1                                                              #Increment counter by 1

#The next part calculates the rating for the test data set using the updated values of theta for users and feature vectors for movies
for index, row in df3.iterrows():                                           #Loop over the rows of the test dataframe
    if isinstance(movies[row['movie-Id']][0], str):                         #If the movie has no genre and has not been rated by any user
        k=0                                                                 #Set k=0
        l=0                                                                 #Set l=0
        for i in movie_rating_by_user[row['user-Id']].keys():               #Loop over all the movies rated by this user
            k+= movie_rating_by_user[row['user-Id']][i]                     #Add the rating given by this user for this movie rated by the user to k
            l+=1                                                            #Add 1 to l
        row['Rating']=int(round(k/l))                                       #Set the rating for the movie as the average rating given by the corresponding user and round it off to the nearest integer
    else:                                                                   #Else
        row['Rating']=int(round(np.dot(np.transpose(user_theta[row['user-Id']]), movies[row['movie-Id']]))) #Rating for the movie given by user is dot product of theta values for user and feature vector of movie and round it to nearest integer
        if row['Rating']>5:                                                 #If the rating is going above 5 then 
            row['Rating']=5                                                 #Set that rating to 5

#Create a dataframe solution which contains only the Id and Rating column
solution=df3[['Id','Rating']]            

#Save the solution dataframe as a .txt file
solution.to_csv('Sol3.txt', index=False)