import csv
import numpy as np
import matplotlib.pyplot as plt
import random 

def readAndAppend(): 
    file = open("AvObsSwiss.csv")
    csvreader = csv.reader(file)
    
    n = 0
    valN = 0
    valH = 0
    forecastN = []
    naturalRaw = []
    forecastH = []

    bayesN = []
    bayesH = []

    freqH1 =0
    freqH2 =0
    freqH3 =0
    freqH4 =0

    freqN1 = 0 
    freqN2 = 0
    freqN3 = 0
    freqN4 = 0

    for row in csvreader:
        dRow = row[0].split(';')
        if((dRow[13]!='NA') and dRow[3] == "HUMAN"): 
            valH = int(dRow[13])               
            if(valH == 1):
                freqH1+=1
            elif(valH == 2):
                freqH2 +=1
            elif(valH ==3):
                freqH3 +=1
            else:
                freqH4 +=1
            n+=1
            forecastH.append(valH)

        elif((dRow[13]!='NA') and dRow[3] == "NATURAL"): 
            if(int(dRow[13])==5):
                valN = 4
            else:
                valN = int(dRow[13])
            naturalRaw.append(valN)
                

    forecastN = random.sample(naturalRaw,n)                     #Even number of samples...

    
    for num in forecastN: 
        if(num == 1):
            freqN1+=1
        elif(num == 2):
            freqN2 +=1
        elif(num == 3):
            freqN3 +=1
        else:
            freqN4 +=1
        
            
    bayesN = [freqN1/n,freqN2/n,freqN3/n,freqN4/n,n]
    bayesH = [freqH1/n,freqH2/n,freqH3/n,freqH4/n,n]

    return naturalRaw,forecastH,bayesH,bayesN,

def snowTypeHistogram(sForecast,triggerType):
    n, bins, patches = plt.hist(sForecast, bins=50, color='#0504aa', alpha=0.7, rwidth=0.85)
    plt.xticks([1,2,3,4],['Low (1) ','Moderate (2) ','Considerable (3)','High/Severe (4/5)'])
    plt.grid(axis='y', alpha=0.75)
    plt.ylabel('Frequency')
    if(triggerType == "HUMAN"):
        plt.title('Avalanche Frequency and forecast (Human Triggered)')
    else: 
        plt.title('Avalanche Frequency and forecast (Naturally Triggered) ')

    plt.show()

def naiveBayesian(bayesN,bayesH):
    arrNat = [] 
    arrHum = []
    arr =[]
    pCHuman = bayesH[4]/(bayesN[4]+bayesH[4])
    pCNatural = bayesN[4]/(bayesN[4]+bayesH[4])
    
    for i in range(len(bayesN)-1): 
        arrNat.append(pCNatural*bayesN[i])
        arrHum.append(pCHuman*bayesH[i])
    arr = [arrNat,arrHum]
    return arr


def main():
    forecastNaturalRaw,forecastHuman,bayesH,bayesN = readAndAppend()
    arr = naiveBayesian(bayesN,bayesH)
    severity = ['Low','Moderate','Considerable', 'High']
    
    userInput = int(input("What is the avalanche forecast rating for today (1-4): "))
    H = 100*round(arr[1][userInput-1],6)
    N = 100*round(arr[0][userInput-1],6)
    print("The probability of natural avalanches is: %f%%" % N)
    print("The probability of human triggered avalanches is: %f%%" % H)

    print('\n')
    severity = ['Low','Moderate','Considerable', 'High']
    print("Scores for naturally and human triggered avalanches: ")
    print("  Rating"+8*' '+'Human'+4*' '+2*' '+'Natural')
    for i in range(len(arr[0])):
        valN= str(round(arr[0][i],6))
        valH= str(round(arr[1][i],6))
        print('| '+severity[i] + ((12-len(severity[i]))*' ')+'| '+valH +((8-len(valH))*' ') + ' | '+valN+' |')

    snowTypeHistogram(forecastNaturalRaw,"NATURAL")
    snowTypeHistogram(forecastHuman,"HUMAN")

main()