#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import sys
from MaxConnect4Game import *

#One Move Mode Game
def oneMoveGame(currentGame,depth):
    # To check whether the board full already or not
    if currentGame.pieceCount == 42:    
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)
    move = currentGame.aiPlay(currentGame,depth)
    result = currentGame.playPiece(move)
    newState(currentGame,move,'Human')
    currentGame.gameFile.close()

#Exploring the new state and writing the board on files(human.txt and computer.txt)
def newState(currentGame,move,player):
    print('\n\nMove no.%d: %s %d , Column = %d\n'%(currentGame.pieceCount,player,currentGame.currentTurn,move+1))
    if currentGame.currentTurn==1:
       currentGame.currentTurn = 2
    elif currentGame.currentTurn==2:
         currentGame.currentTurn = 1
    print'Game state after move:'
    currentGame.printGameBoard()
    currentGame.countScore()
    print('Points Scored:\nHuman :- %d\nComputer :- %d\n'%(currentGame.PlayerCount,currentGame.ComputerScore))
    currentGame.printGameBoardToFile()

#Interactive Mode Game
def interactiveGame(currentGame,depth):
   while not currentGame.pieceCount == 42:
    if currentGame.currentTurn == 1:
        userMove = input("To continue to play pick a column number from (1 to 7) or pick (8) to exit: ")
        if not 0 < userMove < 9:
            print"Its not a valid column number"
            continue
        if userMove == 8:
            print"\n PLAYER LEFT GAME OVER !!\n"
            currentGame.gameFile.close()
            sys.exit()
        if not currentGame.playPiece(userMove - 1):
            print"Please select another column, this column is complete!!"
            continue
        try:
            currentGame.gameFile=open("human_steps.txt",'w')
        except:
           sys.exit('Error in opening output file.')
        newState(currentGame,userMove - 1,'Human')


    elif not currentGame.pieceCount == 42:
        move = currentGame.aiPlay(currentGame,depth)
        result = currentGame.playPiece(move)
        try:
            currentGame.gameFile=open("computer_steps.txt",'w')
        except:
           sys.exit('Error in opening output file.')
        newState(currentGame,move,'Computer')
   currentGame.gameFile.close()

#Result of the game
   if currentGame.ComputerScore > currentGame.PlayerCount:
        print "The Winner is Computer "
   elif currentGame.PlayerCount > currentGame.ComputerScore:
        print "YOU are the Winner"
   else:
        print"Its a draw "
   

#Main function
def main(argv):
    # to check that the command-line arguments given is appropriate
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)
    game_mode, inFile = argv[1:3]
    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game

    # Try to open the input file
    try:
        currentGame.gameFile = open(inFile, 'r')
    except IOError:
        sys.exit("\nOpening file failed.\n")


    # Read the initial game state from the file and save in a 2D list
    file_lines = currentGame.gameFile.readlines()
    currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
    currentGame.currentTurn = int(file_lines[-1][0])
    currentGame.gameFile.close()

    print '\nMax Connect-4 game\n'
    print 'Game state before move:'
    currentGame.printGameBoard()


    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Points Scored:\nHuman :- %d\nComputer :- %d\n' % (currentGame.PlayerCount, currentGame.ComputerScore))

    if game_mode == 'interactive':
        if argv[3]== 'computer-next':
            currentGame.currentTurn = 2
        else:
            currentGame.currentTurn = 1
        interactiveGame(currentGame,argv[4])
    else: # The mode of the game selected is 'one-move'
     
        outFile = argv[3]
        try:
            currentGame.gameFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')
        
        oneMoveGame(currentGame,argv[4]) 


if __name__ == '__main__':
    main(sys.argv)
