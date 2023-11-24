#phase 1

def createUserList():
    f = open('u.user')
    userList = []
    for users in f: 
        info = users.split('|')
        current = {} 
        current['age'] = int(info[1])
        current['gender'] = info[2]
        current['occupation'] = info[3]
        current['zip'] = info[4][:len(info[4])-1]
        userList.append(current)
    return userList
        
def createMovieList():
    f = open('u.item', encoding = "windows-1252")
    movieList = [] 
    for movies in f:
        info = movies.split('|')
        current = {}
        current['title'] = info[1]
        current['release date'] = info[2]
        current['video release date'] = info[3]
        current['IMDB url'] = info[4] 
        genreList = []
        i = 1
        while i < len(info):
            if str(info[i]).isdigit():
                genreList.append(int(info[i]))
            i += 1
        genreList.append(int(info[len(info)-1].replace('\n', '')))
        current['genre'] = genreList
        movieList.append(current)
    return movieList
        
def readRatings():
    f = open('u.data')
    ratingTuples = []
    for ratings in f:
        info = ratings.split()
        user = int(info[0])
        movie = int(info[1])
        rating = int(info[2])
        currentTuple = (user, movie, rating)
        ratingTuples.append(currentTuple)
    return ratingTuples

def createRatingsDataStructure(numUsers, numItems, ratingTuples):
    newTups = sorted(ratingTuples)
    rLu = []
    rLm = []
    ratings = {}
    user = 1
    for tuples in newTups:
        if tuples[0] == user:
            ratings[tuples[1]] = tuples[2]
        else:
            user += 1
            rLu.append(ratings)
            ratings = {}
            ratings[tuples[1]] = tuples[2]
    rLu.append(ratings)
    #reshape ratingTuples so we can sort by movie
    movieTuples = ratingTuples
    newTups = []
    for x in movieTuples:
        user = x[0]
        movie = x[1]
        rating = x[2]
        x = (movie, user, rating)
        newTups.append(x)
    movieTups = sorted(newTups)
    movie = 1
    ratings = {}
    for tuples in movieTups:
        if tuples[0] == movie:
            ratings[tuples[1]] = tuples[2]
        else:
            movie += 1
            rLm.append(ratings)
            ratings = {}
            ratings[tuples[1]] = tuples[2]
    rLm.append(ratings)
    res = [rLu, rLm]
    return res   

def createGenreList():
    f = open('u.genre')
    genreList = [] 
    for genres in f:
        info = genres.split('|')
        if info[0] != '\n':
            genreList.append(info[0])
    return genreList  
         

def demGenreRatingFractions(userList, movieList, rLu, gender, ageRange, ratingRange):
    
    #need the total number of ratings provided from the gender and ageRange/ the rating of the move in that genre 
    
    if ageRange[0] == ageRange[1]:
        return [None] * 19
    
    validRaters = [] 
    #make a list of potential candidates, get the length of that list 
    i = 0 
    for x in userList:
        if ((gender == 'A') or (x['gender'] == gender)) and (x['age'] < ageRange[1]) and (x['age'] >= ageRange[0]):
            validRaters.append(i)
        i += 1
    #check how many movies those people rated 
    denom = 0
    for x in validRaters:
        denom += len(rLu[x])
    if denom == 0:
        return [None] * 19
    #moviesRated consists of the movies that the validRaters rated 
    moviesRated = [] 
    #need to see what movies they rated 
    for x in validRaters:
        #print(rLu[x])
        sample = [] 
        for validMovies in rLu[x]:
            sample += [validMovies]
        moviesRated.append(sample)
    #use this list to get the movies that were rated 5 and above 
    validMoviesWithRatings = [] 
    i = 0
    while i < len(moviesRated):
        j = 0
        for x in moviesRated[i]:
            if (rLu[validRaters[i]][x] <= ratingRange[1]) and (rLu[validRaters[i]][x] >= ratingRange[0]):
                validMoviesWithRatings.append(moviesRated[i][j])
            j += 1
        i += 1
    #now, find the genre these movies have, and add it to it's genres total 
    genres = [0] * 19 
    for x in validMoviesWithRatings:
        i = 0
        for genreVals in movieList[x-1]['genre']:
            if genreVals == 1:
                genres[i] += 1
            i += 1
    res = [] 
    for numer in genres:
        res.append(numer/denom)
        
    return res 

#phase 2 
def randomPrediction(u, m):
    import random
    return random.randint(1,5)

def meanUserRatingPrediction(u, m, rLu):
    totalRanked = len(rLu[u-1])
    ratings = rLu[u-1].values()
    return sum(ratings)/totalRanked

def meanMovieRatingPrediction(u, m, rLm):
    totalRanked = len(rLm[m-1])
    ratings = rLm[m-1].values()
    return sum(ratings)/totalRanked

def demRatingPrediction(u, m, userList, rLu):
    
    '''     This could be wrong, haven't accounted for user u's ratings, not sure we need to tho       '''
    
    U = []
    i = 0
    gender = userList[u-1]['gender']
    ages = range((userList[u-1]['age'] - 5), (userList[u-1]['age'] + 6))
    while i < len(userList):
        if i == u-1:
            i += 1
            continue
        #this might need to be fixed once i get the answer to the user ID question, so like if u is 1, is that user 1, or at the index 1, meaning it would be user 1
        if (userList[i]['gender'] == gender) and (userList[i]['age'] in ages):
            U.append(i)
        i += 1
    if len(U) == 0:
        return None
    ratings = []
    for x in U:
        if m in rLu[x]:
            ratings.append(rLu[x][m])
    [ratings.remove(x) for x in ratings if x > 5]
    if len(ratings) == 0:
        return None
    return sum(ratings)/len(ratings)

def genreRatingPrediction(u, m, movieList, rLu):
    #get the genres of m
    mGenres = movieList[m-1]['genre']
    M = []
    #get the movies with a similar genre to m 
    for movies in range(len(movieList)):
        #the genre of the movies in movieList
        potential = movieList[movies]['genre']
        count = 0
        for i in range(len(potential)):
            #check to see if any of the genres in potential are also in m
            if (potential[i] == 1) and (mGenres[i] == 1):
                count += 1
        #if more than 1 genre is alike, add it to M
        if count >= 1:
            M.append(movies)
    if len(M) == 0:
        return None 
    M.remove(m-1)
    ratings = []
    thisHasBeenRated = []
    #check to see if a movie in M has been rated by u  
    for valid in M:
        if (valid + 1 in rLu[u-1]):
            #if m has been rated by u, append its rating to a list 
            thisHasBeenRated.append(valid)
            ratings.append(rLu[u-1][valid+1]) 
    if len(ratings) == 0:
        return None
    res = sum(ratings)/len(ratings)
    return res

def partitionRatings(rawRatings, testPercent):
    rawRatings = readRatings()
    testSet = []
    import random
    percent = int((testPercent/100)*len(rawRatings))
    testIndexes = [] 
    while len(testIndexes) < percent:
        randVal = random.randint(1,len(rawRatings)-1)
        if randVal not in testIndexes:
            testIndexes.append(randVal)
        else:
            0
    for x in testIndexes:
        testSet.append(rawRatings[x])
        rawRatings[x] = None
    
    trainingSet = [x for x in rawRatings if x != None]
    return [trainingSet, testSet]

def rmse(actualRatings, predictedRatings):
    import math 
    #ri - ri prime
    total = 0 
    T = 0
    for i in range(len(actualRatings)):
        if predictedRatings[i] == None:
            continue
        total += (actualRatings[i] - predictedRatings[i])**2
        T += 1
    val = total/T
    sqroot = math.sqrt(val)
    return sqroot

def partitionRatings(rawRatings, testPercent):
    rawRatings = readRatings()
    testSet = []
    import random
    percent = int((testPercent/100)*len(rawRatings))
    testIndexes = [] 
    while len(testIndexes) < percent:
        randVal = random.randint(1,len(rawRatings)-1)
        if randVal not in testIndexes:
            testIndexes.append(randVal)
        else:
            0
    for x in testIndexes:
        testSet.append(rawRatings[x])
        rawRatings[x] = None
    
    trainingSet = [x for x in rawRatings if x != None]
    return [trainingSet, testSet]

def rmse(actualRatings, predictedRatings):
    import math 
    #ri - ri prime
    total = 0 
    for i in range(len(actualRatings)):
        total += (actualRatings[i][2] - predictedRatings[i][2])**2
        T += 1
    val = total/T
    sqroot = math.sqrt(val)
    
def similarity(u, v, rLu):
    import math 
    #get movies that both of them have rated 
    #movies is the id 
    bothRated = []
    for movies in rLu[u-1]:
        if movies in rLu[v-1]:
            bothRated.append(movies)
    if len(bothRated) == 0:
        return 0
    #mean rating of u and v 
    meanU = sum(rLu[u-1].values())/len(rLu[u-1])
    meanV = sum(rLu[v-1].values())/len(rLu[v-1])
    numer = 0 
    for m in bothRated:
        rum = rLu[u-1][m]
        rvm = rLu[v-1][m]
        numer += ((rum - meanU) * (rvm - meanV))
    uSum = 0
    vSum = 0
    for m in bothRated:
        rum = rLu[u-1][m]
        rvm = rLu[v-1][m]
        uSum += (rum - meanU)**2
        vSum += (rvm - meanV)**2
    denom = math.sqrt(uSum) * math.sqrt(vSum)
    if denom == 0 :
        return 0
    return numer/denom
    
def kNearestNeighbors(u, rLu, k):
    sim = []
    for i in range(len(rLu)):
        if i == u-1:
            continue
        sim.append([similarity(u, i+1, rLu), i + 1])
    theBest = sorted(sim)[len(sim)-k:]
    for x in theBest:
        copy = x[0]
        x[0] = x[1]
        x[1] = copy
    return [tuple(x) for x in theBest]

def CFRatingPrediction(u, m, rLu, friends):
    meanU = sum(rLu[u-1].values())/len(rLu[u-1])
    potential = [x[0] for x in friends]
    real = []
    for x in potential:
        if m not in rLu[x-1]:
            continue
        real.append(x)
    numer = 0
    denom = 0
    for v in real:
        meanV = sum(rLu[v-1].values())/len(rLu[v-1])
        rvm = rLu[v-1][m]
        numer += ((rvm - meanV) * similarity(u, v, rLu))
        if similarity(u, v, rLu) < 0:
            denom += (similarity(u, v, rLu) * -1)
        else:
            denom += similarity(u, v, rLu)
    if denom == 0:
        return 0
    return meanU + (numer/denom)
    
#main program 
userList = createUserList()
movieList = createMovieList()
rawRatings = readRatings()
numUsers = len(userList)
numMovies = len(movieList)
[rLu, rLm] = createRatingsDataStructure(numUsers, numMovies, rawRatings)
genreList = createGenreList()
#main program for rmse
[trainingSet, testSet] = partitionRatings(rawRatings, 20)
[trainingRLu, trainingRLm] = createRatingsDataStructure(numUsers, numMovies, trainingSet)

'''algo1 = []
algo2 = []
algo3 = []
algo4 = []
algo5 = []

j = 0
while j < 10:
    
    [trainingSet, testSet] = partitionRatings(rawRatings, 20)
    [trainingRLu, trainingRLm] = createRatingsDataStructure(numUsers, numMovies, trainingSet)    
    
    #randomPrediction
    randomList = []
    meanUserList = []
    meanMovieList = []
    demRatingList = []
    genreRatingList = [] 

    for test in testSet:
        u = test[0]
        m = test[1]
        randomList.append(randomPrediction(u, m))
        meanUserList.append(meanUserRatingPrediction(u, m, rLu))
        meanMovieList.append(meanMovieRatingPrediction(u, m, rLm))
        demRatingList.append(demRatingPrediction(u, m, userList, rLu))
        genreRatingList.append(genreRatingPrediction(u, m, movieList, rLu))
    
    actualRatings = []
    
    for users in testSet:
        u = users[0]
        m = users[1]
        actualRatings.append(rLu[u-1][m])


    randomRmse = rmse(actualRatings, randomList)
    meanUserRmse = rmse(actualRatings, meanUserList)
    meanMovieRmse = rmse(actualRatings, meanMovieList)
    demRatingRmse = rmse(actualRatings, demRatingList)
    genreRatingRmse = rmse(actualRatings, genreRatingList)
    
    algo1.append(randomRmse)
    algo2.append(meanUserRmse)
    algo3.append(meanMovieRmse)
    algo4.append(demRatingRmse)
    algo5.append(genreRatingRmse)
    
    j +=1'''

[trainingSet, testSet] = partitionRatings(rawRatings, 20)

ten_friends = []
hundred_friends = []
fivehundred_friends = []
all_users = []

friendsList = [10, 100, 500, len(userList)]
tenList = []
hundredList = []
fivehundredList = []
allList = []

for test in testSet:
    u = test[0]
    m = test[1]
    tenfriends = kNearestNeighbors(u, rLu, 10)
    tenList.append(CFRatingPrediction(u, m, rLu, tenfriends))   
    
    hundredfriends = kNearestNeighbors(u, rLu, 100)
    hundredList.append(CFRatingPrediction(u, m, rLu, hundredfriends))    
    
    fivehundredfriends = kNearestNeighbors(u, rLu, 500)
    fivehundredList.append(CFRatingPrediction(u, m, rLu, fivehundredfriends))    
    
    allfriends = kNearestNeighbors(u, rLu, len(userList))
    allList.append(CFRatingPrediction(u, m, rLu, allfriends))

    
actualRatings = []
    
for users in testSet:
    u = users[0]
    m = users[1]
    actualRatings.append(rLu[u-1][m])
    
tenRmse = rmse(actualRatings, tenList)
hundredRmse = rmse(actualRatings, hundredList)
fivehundredRmse = rmse(actualRatings, fivehundredList)
allRmse = rmse(actualRatings, allList)
    
ten = []
hundred = []
fivehundred = []
allU = []

ten.append(tenRmse)
hundred.append(hundredRmse)
fivehundred.append(fivehundredRmse)
allU.append(allRmse)


import matplotlib.pyplot as plt
    
    
def draw_boxplot(data, labels):
    plt.boxplot(x=data, labels=labels)
    plt.title("Algorithm performance comparison")
    plt.ylabel("RMSE values")
    plt.show()
    plt.close()
    
# ---------------
# Data
    
'''data = [algo1, algo2, algo3, algo4, algo5, ten, hundred, fivehundredm allU]
labels = ["Algo1", "Algo2", "Algo3", "Algo4", "Algo5", "ten_friends", "hundred_friends", "fivehundred_friends", "all_users"]'''
data = [ten, hundred, fivehundred, allU]
labels = ["ten_friends", "hundred_friends", "fivehundred_friends", "all_users"]
    
draw_boxplot(data, labels)




