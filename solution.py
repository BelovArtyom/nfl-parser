"""Case-study #4 Парсинг web-страниц
Разработчики:
Белов А. (100%)

"""

import urllib.request
import string

line = 0  # line is a counter of the inputfile line that is to be read
neededstats = [1, 2, 4, 6, 7]  # indexes of stats we need out of the NFL table
global inputlength
global url
inputlength = 0
url = 0

# getting the amount of repetitions that the script has to take
with open("input.txt", "r") as inp:
    global inputlength
    urlinputline = inp.readlines()
    inputlength = len(urlinputline)

# clearing out output.txt that might exist previously or creating it
with open("output.txt", "w") as makeorclean:
    makeorclean.close()

# declaring number string
numbers = "1234567890"
# declaring english letter string
engletters = string.ascii_lowercase

# starting the cycle on input.txt
while line <= inputlength:

    # taking "line" line out of input.txt
    with open("input.txt", "r") as inp:
        global url
        urlinputline = inp.readlines()
        url = urlinputline[line]

    # importing request from urllib, taking line from input.txt
    file = urllib.request.urlopen(url)
    text = str(file.read())

    # finding the player name
    playername = text.find('player-name')
    playernamelength = 1  # first letter is 13th after 'player-name' tag
    for i in range(14, 34):  # printing all next letters that make up the name max of 20
        if text[playername + i] == " " or text[playername + i].lower() in engletters:  # lower to not put in uppercase
            playernamelength += 1
        else:
            break

    # adjucting playername to take up 20 characters
    playername = text[playername: playername + playernamelength]
    if playernamelength < 20:
        playername = playername + " " * (20 - playernamelength)

    # finding player stats
    totalfind = text.find("TOTAL")
    text = text[totalfind::]

    stats = [0, 0, 0, 0, 0]  # an array for COMP, ATT, YDS, TD, INT
    statsindex = 0  # current index in stats[] that we're filling
    statcount = 1  # current index of stat we've found
    foundstat = 0  # value of the stat we've found
    numlength = 0  # counter for length of the number we're finding

    # starting it 4 times in order to stop it from gathering further numeral data
    while statsindex != 5:

        # finding number
        if text[i] in numbers:
            x = i

            # getting the length of the number
            while text[x] == "," or text[x] in numbers:
                numlength += 1
                x += 1
            numlength = 0  # resetting the value so that next passing doesn't add to the existing length
            foundstat = text[i:x]

            # removing pesky "," from our new stat and turning it into an int
            if foundstat.find(",") != -1:
                foundstat = foundstat[0:foundstat.find(",") - 1] + foundstat[foundstat.find(",") + 1::]
            print(foundstat)
            foundstat = int(foundstat)

            # shortening the list we're fishing information out of
            text = text[x::]
            # putting information into stats[] to later calculate passer rating
            if statcount == neededstats[statsindex]:
                stats[statsindex] = foundstat
                statsindex += 1

    # declaring formulaarray for a, b, c and d in passer rating formula
    formulaarray = [0, 0, 0, 0]

    # calculating passer rating subformulas for the player
    formulaarray[0] = (stats[0] / stats[1] - 0.3) * 5
    formulaarray[1] = (stats[2] / stats[1] - 3) * 0.25
    formulaarray[2] = (stats[3] / stats[1]) * 20
    formulaarray[3] = 2.375 - (stats[4] / stats[1] * 25)

    # checking results for >2.375 and <0  as per description of formula
    for x in range(0, 3):
        if formulaarray[x] > 2.375:
            formulaarray[x] = 2.375
        if formulaarray[x] < 0:
            formularray = 0

    # calculating the nfl passer rating for player
    nflpasser = (formulaarray[0] + formulaarray[1] + formulaarray[2] + formulaarray[3]) / 6 * 100

    # formatting stats
    for x in range(0, 3):
        if len(str(stats[x])) < 7:
            stats[x] = str(stats[x]) + " " * (7 - len(str(stats[x])))

    # outputting the entire line with playername and stats into the output.txt file
    with open("output.txt", "a") as outputfile:
        outputfile.write(playername, stats[0], stats[1], stats[2], stats[3], nflpasser)

"""
import urllib.request
url = 'http://www.nfl.com/player/brycepetty/2552369/profile'
f = urllib.request.urlopen(url)
s = f.read()
text = str(s)
part_name = text.find("player-name")
name = text[text.find('>',part_name)+1:text.find('&',part_name)]
print(name)

Пример файла output.txt

Bryce Petty         0      0      0      0      0      0.00   
Jimmy Garoppolo     20     31     188    1      0      102.69 
Matt Moore          453    769    5356   33     28     94.82  
AJ McCarron         79     119    854    6      2      106.37 
...
"""
