import numpy as np
import os

def printAndSave(*string):
    #print(*string, end = '') #print to terminal
    resultFile = open('ResultFile.txt','a+') #open to append file
    print(*string, end = '',file=resultFile) #print to file 
    resultFile.close()                       #close file 
    
def finalPrint():
    array = np.array([[1,2,3,4,"initial",5]], dtype=object) #create an array with initial value
    totalConfidence = 0;
    #open file, get x,y coordinate of the top left corner of the word box and the word from result file
    directory = os.path.join(os.getcwd(), 'craft_pytorch', 'CropWords')
    file_directory = os.path.join(directory, 'te.pn_log_demo_result_vgg.txt')
    with open(file_directory) as file: # open file
        for line in file: # read line by line
            b = line.split("\t") #split file name, word, confident
            c = b[0] # file name
            word = b[1]  # get word
            totalConfidence += float(b[2]) # get confidence of each word
            word = word.strip() #strim word
            d = c.split("_") #split file name by underscore (FILE NAME MUST NOT HAVE UNDERSCORE)
            e = d[1]    #get x coordinate of the top left corner of the box
            f = d[2]    #get y coordinate of the top left corner of the box
            g = d[3]    #get x coordinate of the top right corner of the box
            h = d[6]    #get y coordinate of the bottom right corner of the box
            e = np.round_(float(e)) #round to int
            e = int(e)      #get int value
            f = np.round_(float(f))
            f = int(f)
            g = np.round_(float(g))
            g = int(g)
            h = np.round_(float(h))
            h = int(h)
            middleY = (f + h) / 2 #middle Y coordinate
            middleY = np.round_(float(middleY))
            middleY = int(middleY)
            lineArray = np.array([[e,f,g,h,word, middleY]], dtype=object) #create array for each line
            array = np.concatenate((array,lineArray)) #concate to the big array
    array = np.delete(array,0,0) #delete the initial value

    # normalize the x and y
    #(a ratio of width,height of image over those of word box??)
    yRatio = 15
    xRatio = 15
    for arrayElement in array:
        normYValue = arrayElement[1]/yRatio #divide by ratio
        normYValue = round(normYValue)    #round to int
        arrayElement[1] = normYValue
        
        normXValue = arrayElement[0]/xRatio #divide by ratio
        normXValue = round(normXValue)    #round to int
        arrayElement[0] = normXValue
        
        normrightXValue = arrayElement[2]/xRatio #divide by ratio
        normrightXValue = round(normrightXValue)    #round to int
        arrayElement[2] = normrightXValue
        
        normrightYValue = arrayElement[3]/yRatio #divide by ratio
        normrightYValue = round(normrightYValue)    #round to int
        arrayElement[3] = normrightYValue
        
        normMiddleYValue = arrayElement[5]/yRatio #divide by ratio
        normMiddleYValue = round(normMiddleYValue)    #round to int
        arrayElement[5] = normMiddleYValue
    array = array[array[:,0].argsort()] #sort by second column (x)
    array = array[array[:,5].argsort(kind='mergesort')] #sort by second column (y) #update: middle y


    index = 0
    #coeffectient of x and y to print (because space != newline (' ' != '\n'))
    xCoefficient = 2
    yCoefficient = 1
    for arrayElement in array:
        if index == 0:
            printAndSave('\n'* arrayElement[1]*yCoefficient)
            printAndSave(' ' * arrayElement[0]*xCoefficient,arrayElement[4])
        else:
            if arrayElement[5] == array[index-1,5]: #update: check middle y
                printAndSave(' ' * (arrayElement[0]-array[index-1,2])*xCoefficient,arrayElement[4])
            else:
                printAndSave('\n' * (arrayElement[5] - array[index-1,5])*yCoefficient) #update: print by middle y
                printAndSave(' ' * arrayElement[0]*xCoefficient,arrayElement[4])
        index+=1
    totalConfidence = totalConfidence / index # divide to get the whole text confidence
    totalConfidence = str(round(totalConfidence,2))
    return totalConfidence

