import numpy as np

#arr1 = np.array([[1, 2, "as"]])

#arr2 = np.array([[4, 5, "jgj"]])

#arr1 = np.concatenate((arr1, arr2))

#print(arr1)
array = np.array([[1,2,"initial"]], dtype=object) #create an array with initial value
#open file, get x,y coordinate of the top left corner of the word box and the word from result file
with open('te.pn_log_demo_result_vgg.txt') as file: # open file
    for line in file: # read line by line
        #print("new line  ")
        #print(line)
        b = line.split("\t") #split file name, word, confident
        c = b[0] # file name
        word = b[1]  # get word
        word = word.strip() #strim word
        d = c.split("_") #split by underscore
        e = d[1]    #get x coordinate of the top left corner of the box
        f = d[2]    #get y coordinate of the top left corner of the box
        #print(e)
        #print(f)
        #print(float(e))
        e = np.round_(float(e)) #round to int
        e = int(e)      #get int value
        f = np.round_(float(f))
        f = int(f)
        lineArray = np.array([[e,f,word]], dtype=object) #create array for each line
        array = np.concatenate((array,lineArray)) #concate to the big array
        #print(lineArray)
        #print(e, f, word)
        #print(f)
        #print(word)
array = np.delete(array,0,0) #delete the initial value
#array = array[array[:,0].argsort()] #sort by second column (y)
#array = array[array[:,1].argsort(kind='mergesort')] #sort by second column (y)
#array = np.sort(array)
print(array)

print("\narray after normalization:\n")

# normalize the x and y
for arrayElement in array:
    #print(arrayElement[1])
    normYValue = arrayElement[1]/20 #divide by 10
    normYValue = round(normYValue)    #round to int
    #print(normValue)
    arrayElement[1] = normYValue
    
    normXValue = arrayElement[0]/15 #divide by 10
    normXValue = round(normXValue)    #round to int
    #print(normValue)
    arrayElement[0] = normXValue
array = array[array[:,0].argsort()] #sort by second column (x)
array = array[array[:,1].argsort(kind='mergesort')] #sort by second column (y)
print(array)
print("\nFull text:\n")


#problem: not correct in the same line,
index = 0
for arrayElement in array:
    if index == 0:
        print('\n' * arrayElement[1], end = '')
        print(' ' * arrayElement[0],arrayElement[2], end = '')
        
    else:
        if arrayElement[1] == array[index-1,1]:
           print(' ' * (arrayElement[0]-array[index-1,0]),arrayElement[2], end = '')
        else:
           print('\n' * (arrayElement[1] - array[index-1,1]), end = '')
           print(' ' * arrayElement[0],arrayElement[2], end = '')
   #print(arrayElement[2])
    index+=1
    
#lineIndex = 0 #line index = y 
#currentLineIndex = 0 # current line index = previous y
#index = 0 #index of iteration
#for arrayElement in array:
#    if index == 0:
#        print('\n' * arrayElement[1], end = '')
#        print(' ' * arrayElement[0],arrayElement[2], end = '')
#        currentLineIndex=index
#    else:
#        if arrayElement[1] == array[currentLineIndex,1]:
#            print(' ' * (arrayElement[0]-array[index-1,0]),arrayElement[2], end = '')
#            #print(int(arrayElement[0]-array[currentLineIndex,0]))
#        else:
#            print('\n' * (arrayElement[1] - array[currentLineIndex,1]), end = '')
#            print(' ' * arrayElement[0],arrayElement[2], end = '')
#            currentLineIndex=index
#    #print(arrayElement[2])
#    index+=1
#    lineIndex=arrayElement[1]

