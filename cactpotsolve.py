#The purpose of this tool is to determine the scratchcard row with the highest
#predicted payout for the Cactpot Scratchcard in Final Fantasy XIV, given an
#input of the four spaces the user has already scratched off


import statistics
import itertools

#Covers cases in which a square corner of the scratchcard is scratched
#TODO - switch input from command line to GUI, will make it easier to support
#any configuration of scratches
#TODO - compartmentalize pieces of main function into smaller ones
#TODO - generate testing function
#TODO - catch errors like duplicates/5 scratches
def scratchsolve():
    scratched = [1,2,3,4]
    for value in range(0,4):
        scratched[value] = int(input("Scratch " + str(value+1) + ": "))
    scoredict = {6:10000,7:36,8:720,9:360,10:80,11:252,12:108,13:72,
                 14:54,15:180,16:72,17:180,18:119,19:36,20:306,21:1080,
                 22:144,23:1800,24:3600}
    allnums = list(range(1,10))
    for num in scratched:
        allnums.remove(num)
    combolist = []
    sumlist = []

    #See what happens if you add an unknown number to two known ones
    for value in scratched:
        for value2 in scratched:
            if value != value2:
                if str(value)+ "+" + str(value2) not in combolist:
                    if str(value2)+ "+" + str(value) not in combolist:
                        avglist = []
                        for possibility in allnums:
                            avglist.append(scoredict[value+value2+possibility])
                        combolist.append(str(value)+ "+" + str(value2))
                        sumlist.append(statistics.mean(avglist))
    #See what happens for the triple unknown rows
    unknownlist = list(itertools.combinations(allnums,3))
    unknownscores = 0
    for combination in unknownlist:
        unknownscores += (scoredict[sum(combination)])
    unknownavg = unknownscores / len(unknownlist)
    if unknownavg >= max(sumlist):
        print("The best choice is 3 unknown, unscratched spaces.")
    else:
        print("The best choice is: " + str(combolist[sumlist.index(max(max(sumlist),unknownavg))]))
    return


scratchsolve()

