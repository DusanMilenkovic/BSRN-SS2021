import sys
from random import randint # Bibliothek für Zufallszahlen

xaxis, yaxis = 10,10
shipSizes = {'2-2':2,'3-1':3,'4-1':4,'5-1':5}
# Das Grid erstellen
#  Wir erstellen ein Board in einem 2D array(Liste) mit dem wir spielen
def grid(xaxis, yaxis):
    player1Board = []
    player2Board = []
    for x in range(0, xaxis):
        tmpArry = ['-' for y in range(0, yaxis)] # List comprehension
        player1Board.append(tmpArry) # Wir fügen die Elemente der Liste hinzu
    for x in range(0, xaxis):# Zweites Board für den zweiten Spieler (man kann nicht sehen was der andere gemacht hat)
        tmpArry = ['-' for y in range(0, yaxis)] # List comprehension
        player2Board.append(tmpArry)

    return player1Board, player2Board

# die Funktion displayBoard wird das Board unseren Anforderungen nach Anzeigen
def displayBoard(gridArray,show='menu'): # menu ist hier default gesetzt
    for index1, i in enumerate(gridArray):  # ["a","b"] -> enumerate -> [(1,"a"),(2,"b")] Tupel von Elementen
        for index2, j in enumerate(i):
            # durch das enumerate wurden haben die einzelnen Bindestriche eine Nummer bekommen auf die man zugreifen kann
            # Durch den Index1&2 wird an der jeweiligen Koorodinate überprüft ob diese schon ein Hit oder Miss ist
            # um dieses im Nachhinein auf unser Board zu printen
            # Beim Auswählen von Menu wird durch den Input nix angezeigt
            if show == 'menu':
                print('_', end=' ')
            elif show == 'Show': # 'Show' um das Board anzuzeigen
                print(gridArray[index1][index2], end=' ')
            elif show == 'Hit': # 'Hit' um die Treffer anzuzeigen oder die Misses
                if gridArray[index1][index2] == 'X': # X = Hit
                    print('X', end=' ')
                elif gridArray[index1][index2] == '*': # * = Miss
                    print('*', end=' ')
                else:
                    print('_', end=' ')
        print('\n')


# Funktion um die Schiffe manuell zu plazieren durch user input
def placeShipsManually(playerBoard):
    ships = {}
    count = 1
    # erstellen von Schiffen und diese im Dictionary speichern
    for allShips, sizeOfShip in shipSizes.items():
        # .items() holt sich Elemente aus Dictionaries
        # allShips = Schlüßel von shipSizes
        # sizeOfShip = Wert von shipSizes (Zeile 19)

        allShip = int(allShips.split('-')[1]) # mit .split nimmt er das '-' aus dem Schlüsselpaaren raus
        for ship in range(allShip):
            tmpArr = []
            displayBoard(playerBoard,'Show') # Board wird mit show geprinted
            print('Platziere {} Schiff/e der länge {}'.format(allShip,sizeOfShip)) # hier wird durch format die Anzahl und laenge angezeigt im Print
            for size in range(sizeOfShip):
                while True:
                    x = int(input('Reihe : ')) # input Reihe
                    y = int(input('Spalte : '))  # input Spalte
                    if playerBoard[x][y] != '||': # überprüft ob die Postion bereits belegt ist
                        playerBoard[x][y] = '||'
                        tmpArr.append((x,y))
                        print('erfolgreich hinzugefügt\n')
                        break
            print('Schiff erfolgreich platziert')
            ships[count] = tmpArr # Jede Position des Schiffes wird im Dictionary abgespeichert
            count += 1
    displayBoard(playerBoard,'Show')  # in jedem Durchlauf der Schleife wird das Board neu geprinted
    return playerBoard,ships

# diese Funktion erstellt die Schiffe sowie das Board für den Computer
def createComputerShips(playerBoard,xaxis,yaxis):
    shipsSize = [2,2,3,4,5]
    ships = {}
    shipCounter = 1
    count = 0
    # es werden wieder 5 Schiffe erstellt wie in shipsSize gegeben

    for size in shipsSize:
        tmpArr = []
        for i in range(size):
            if count == 0: # Macht im ersten Durchgang (bis counter größer als 0)
                while True:
                    x = randint(0,xaxis-1)
                    y = randint(0,yaxis-1)
                    # hier werden zufalls Koordinaten erstellt
                    try:  # try, except und pass wurden eingebaut falls an der Stelle errors auftreten das diese ignoriert werden
                        if playerBoard[x][y] != '||': # diese werden genau wie davor überprüft
                            playerBoard[x][y] = '||'
                            tmpArr.append((x,y))
                            count += 1
                            break # falls erfolgreich wird die Schleife unterbrochen
                        else: # falls nicht erfolgreich wird dies solang wiederholt bis eine freiepostion gefunden wurde
                            x = randint(0,xaxis-1) # Zufallszahl zwischen 0 und 9
                            y = randint(0,yaxis-1)
                    except:
                        pass
            else:  # nimmt die xachsen postion und arbeitet mit ihr weiter
                y = y+1   # y wird um 1 erhöht, dass das Schiff in richtiger reihenfolge aufgestellt wird
                while True:
                    try:
                        if playerBoard[x][y] != '||':
                            playerBoard[x][y] = '||'
                            tmpArr.append((x,y))
                            count += 1
                            break
                        else:
                            y = y-1  # falls das schiff an der yachse besetzt ist versuchen wir mit der Schleife
                            # diese dann um 1 zu verringern sodass das Schiff richtig steht
                    except:
                        y = y-1
        ships[shipCounter] = tmpArr  # Schiffe werden pro Iteration hinzugefügt bsp ships = { 1: [2,4], 2: [5,8] }
        shipCounter += 1

        shipCounter += 1
        count = 0 # count wird auf 0 gesetzt und die Schleife fängt von neu

    return playerBoard, ships

# Funktion welche die Computer züge macht

def computerPlay(xaxis,yaxis,hitPosition,hit):
    # fängt mit zufälligen Koordinaten an

    if hit == 'Yes':  # falls Hit gleich Yes ist werden zufällige Koordinaten für den nächsten Hit bestimmt
        x = randint(0,xaxis-1)
        y = randint(0,yaxis-1)
        hitPosition = [x,y,'D'] # hitposition ist in dem Fall unsere Start Position und er prüft immer von D als erstes
        hit = 'No' # wenn hit nicht gleich Yes ist sondern No wird er durch den Code aufgefordert den nächsten Hit
        # in einem Umliegendem Feld zu setzen
    elif hitPosition[2] == 'D': # wenn das dritte Element gleich 'D' ist was in unserem Fall stimmt (zeile 133)
        if hitPosition[1]-1 < 0: # wenn y Wert kleiner 0 wenn wir uns am Rand befinden
            hitPosition[1] = hitPosition[1]+1 # wird dieser um plus 1 erhöht
        else:
            hitPosition[1] = hitPosition[1]-1 # falls nicht wird dieser um 1 verringert
        hitPosition[2] = 'L' # Hitpostions drittes Element wird 'L' gleichgesetzt
    elif hitPosition[2] == 'L':
        if hitPosition[0]-1 < 0: #falls der x Wert kleiner als Null ist
            hitPosition[0] = hitPosition[0]+1 # wird dieser um 1 erhöht
        else:
            hitPosition[0] = hitPosition[0]-1 # falls nicht wieder verringert
        hitPosition[2] = 'U' # drittes Element wird zu 'U'

    elif hitPosition[2] == 'U':
        if hitPosition[1]+1 > 10: # falls der y achsen Wert größer 10 ist wird um 1 verringert weil wir uns ausserhalb
            #des Spielfelds befinden
            hitPosition[1] = hitPosition[1]-1
        else:
            hitPosition[1] = hitPosition[1]+1  # der gleiche Prozess für die Restlichen
        hitPosition[2] = 'R'

    elif hitPosition[2] == 'R':
        if hitPosition[0]+1 > 10:
            hitPosition[0] = hitPosition[0]-1
        else:
            hitPosition[0] = hitPosition[0]+1
        hitPosition[2] = 'D' # dritte Element wird wieder D gesetzt, damit der Prozess beim nächsten Hit von vorne beginnen kann
    return hitPosition, hit


# Die Funktion überprüft ob es sich um einen Hit or Miss handelt
def checkHit(playerBoard, ships, cordinates, totalShipsDestroyed):
    x = cordinates[0] # Koordinaten die der Spieler eingibt (Reihe und Spalte)
    y = cordinates[1]
    # wenn sich an der Koordinaten Stelle ein Schiff befindet sagen wir dass es ein Hit ist
    if playerBoard[x][y] == '||':
        print('Hit')
        hit = 'No'
        playerBoard[x][y] = 'X' #an der Stelle wird das Schiff mit dem X ersetzt
        
        displayBoard(playerBoard,'Hit') # das Board wird abgerufen mit der Anzeige für einen Hit
        totalShipsDestroyed = 0 # Counter für die zerstörten Schiffe
        for key,value in ships.items(): # hier werden wieder die Schlüssel und Werte aus unseren playerboard entnommen (Koordinaten)
            # ships = { 1: [2,4], 2: [5,8] }
            # 2,5 => [2,5] nicht in cordinates
            # 2,4 => [2,4] in cordinates

            if cordinates in value:
                index = value.index(cordinates)  #index kriegt den Wert des Values
                value[index] = 'X' # Value prüft ob die Position gleich ein Hit ist
            if value.count('X') == len(value): # Hier wird dann geprüft ob value Count der länge vom Schiff entspricht
                # wenn dies der fall ist kann ein ganzes Schiff als zerstört angeben werden
                totalShipsDestroyed += 1

    # Hier wird überprüft ob die Stelle zuvor schon getroffen worden ist
    elif playerBoard[x][y] == 'X':
        print('bereits getroffen')
        hit = 'Yes'
    # otherwise its a miss
    else:
        playerBoard[x][y] = '*'  # falls die Stelle weder eins von beidem ist wird diese mit einem Miss '*' gekennzeichnet
        print('Miss')
        hit = 'Yes'
    print('Total Ship Destroyed:',totalShipsDestroyed)  # anezeige der Zerstörten Schiffe
    
    return playerBoard, ships, totalShipsDestroyed,hit


# Menü anzeige
def menu():
    print('''
    1 ====> Mehrspieler (1 vs 1)
    2 ====> Computer 
    ''')
# main Funktion hier wird unser Code abgerufen
def main():
    menu()
    # hier wird durch input gefragt gegen was unser User spielen will
    option = int(input('>>>>> '))
    # Die 1 steht für Mehrspieler
    if option == 1:
        # Hier wird das Feld für beide erstellt und das beide ihre Schiffe platzieren nacheinander
        player1Board, player2Board = grid(xaxis, yaxis)  #spielbrett wird initialisiert
        player1Board, player1Ships = placeShipsManually(player1Board) #platzieren der schiffe von P1
        player2Board, player2Ships = placeShipsManually(player2Board) # platzieren der schiffe von P2
        displayBoard(player1Board,'Show') #board wird von P1 angezeigt
        player = 'P1'
        totalShipsDestroyedP1 = 0 # counter der zerstörten schiffe beider Spieler
        totalShipsDestroyedP2 = 0
       # Ab hier wird abwechselnd gespielt
        while True:
            if player == 'P1':
                print(player, 'dein Zug') # player1 spielzug
                x = int(input('Reihe : ')) # User input für Reihe und Spalte
                y = int(input('Spalte : '))
                player2Board,player2Ships,totalShipsDestroyedP1,hit = checkHit(player2Board, player2Ships, (x,y),totalShipsDestroyedP1)
                # hier wurden durch die Funktionen player2board,ships und checkhit das Board vom Player2 angezeigt.
                
                if totalShipsDestroyedP1 == 5: # wenn alle zerstört wurden wird das Spiel beendet
                    print(player, 'hat alle Schiffe zerstört')
                    break
                player = 'P2' #player wird von P1 zu P2 gesetzt
                displayBoard(player1Board,'Hit')
            elif player == 'P2':  # der Gleiche Prozess wird für den zweiten Spieler auch durchgeführt
                print(player, 'dein Zug')
                x = int(input('Reihe : '))
                y = int(input('Spalte : '))
                player1Board,player1Ships,totalShipsDestroyedP2,hit = checkHit(player1Board, player1Ships, (x,y),totalShipsDestroyedP2)
                if totalShipsDestroyedP2 == 5:
                    print(player, 'hat alle Schiffe zerstört')
                    break
                player = 'P1'
                displayBoard(player2Board,'Hit')

    elif option == 2: # hier wird das Feld gegen den Computer vorbereitet bei option 2

        player1Board, player2Board = grid(xaxis, yaxis)
        player1Board, player1Ships = placeShipsManually(player1Board)
        player2Board, player2Ships = createComputerShips(player2Board,xaxis,yaxis) # hier wird die Funktion createComputerShips im vergleich zu vorher benutzt
        print(player1Ships) # hier werden die Koordinaten von Player1 angezeigt (zur Übersicht)
        print(player2Ships) # hier werden die Koordinaten von Computer angezeigt
        player = 'P1' #player wird default gesetzt
        totalShipsDestroyedP1 = 0
        totalShipsDestroyedP2 = 0
        computerHit = 'Yes' # wird yes gesetzt
        hitPosition = [] # aus unserer hitpostion ziehen wir uns die Elemente aus den Parametern die Returned wurden
        while True:
            if player == 'P1':
                print(player, 'dein Zug\n')
                x = int(input('Reihe : '))
                y = int(input('Spalte : '))
                player2Board,player2Ships,totalShipsDestroyedP1,hit = checkHit(player2Board, player2Ships, (x,y),totalShipsDestroyedP1)
                # Die Funktionen werden uns trotzdem angezeigt so damit wir sehen auf welchem Stand wir sind
                if totalShipsDestroyedP1 == 5:
                    print(player, 'hat alle Schiffe zerstört')
                    break # hier wird das Spiel beendet falls P1 alle Schiffe zerstört hat
                player = 'P2' # P1 wird zu P2 geändert um den Computerzug zu simulieren
                displayBoard(player2Board,'Hit')
            elif player == 'P2':
                print(player, 'dein Zug\n')
                
                hitPosition,computerHit = computerPlay(xaxis,yaxis,hitPosition,computerHit)
                cordinates = (hitPosition[0],hitPosition[1])
                player1Board,player1Ships,totalShipsDestroyedP2,computerHit = checkHit(player1Board, player1Ships, cordinates,totalShipsDestroyedP2)
                # hier wurden die Funktionen für den Computer einbebozen so das er seine Spielzüge sinngemäß durchführt
                if totalShipsDestroyedP2 == 5:
                    print(player, 'hat alle Schiffe zerstört')
                    break # hier wird das Spiel beendet falls P2 alle Schiffe zerstört hat
                player = 'P1'
                displayBoard(player1Board,'Hit')
main()