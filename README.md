# ChessAI
For this project I programmed chess from scratch and made a rule based AI to play against. The goal was not to beat Magnus Carlson but to have a decent result and learn python.
The AI was supposed to avoid nonsensical moves. At the end of the day it even got kind of strong and hard to beat. The Youtube tutorial from Eddie Sharick was used as an orientation. 

## How to get started

Have a try against my AI and see how good you are in chess! The setup only takes a few seconds. Download the following directory and execute the Main.exe. Python is not required on your machine in order to do this. https://drive.google.com/drive/folders/1iXlsjQVMOBifXz56XBl5-XGC-f8YuQIP?usp=sharing

You will be playing as black and each player has a time limit of 5 minutes. Whoever gets checkmated or runs out of time loses!

## Controls

N - Start a new game

## Technology and Concepts

The Pygame library was used to display the game. 

![ChessAI](https://user-images.githubusercontent.com/50135757/132984649-34ddf0e4-6a29-45ca-a28e-b015d21ea65f.PNG)

To represent the chess board a two dimensional String array was used. This is not the optimal choice in terms of performance but it is intuative and easy to understand. 

            ["bR","bN", "bB", "bQ", "bK", "bB","bN", "bR"],
            ["bP","bP", "bP", "bP", "bP", "bP","bP", "bP"],
            ["--","--", "--", "--", "--", "--","--", "--"],
            ["--","--", "--", "--", "--", "--","--", "--"],
            ["--","--", "--", "--", "--", "--","--", "--"],
            ["--","--", "--", "--", "--", "--","--", "--"],
            ["wP","wP", "wP", "wP", "wP", "wP","wP", "wP"],
            ["wR","wN", "wB", "wQ", "wK", "wB","wN", "wR"]
            

Each turn the game determines the valid moves that can be made following the conventional chess rules. This requires the calculation of all possible moves as well as the consideration of possible checks. 

The AI is using multiprocessing to perform its tasks paralelly. To find good moves it evaluates the value of the pieces that each player has, as well as their position. The best move then gets choosen using a thechnique called NegaMax-Algorythm. This calculates future positions by assuming that the player will always choose the maximum advantage for himself and the opponent will always to minimize that. To increase efficiency a technique called alpha beta pruning was used which ignores scenarios that aren't relevant. Lastly move ordering was used to make the AI evaluate prommising moves first which brought another big boost of performance. The AI looks 4 Moves into the future which with all of the above mentioned improvements takes 5 seconds on average.

To round up the project move animation, sound effects, last move highlighting, square highlighting and an end screen have been added. 





