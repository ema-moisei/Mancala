# Mancala
Implementation of a Mancala game using PyQt5


Mancala:
    1. Acces game -> prezentare mancala(imagine start)
    2. Menu: Game rules
             Short Hystory
             Sound : fundal, game sounds
             Scores: by player
             Start game: - Select players: - New player: -Select nickname
                                            - Human players list: - if None: Add player
                                            - Computer player
                                            - Continue: -select random who starts
                                                        -actual game
                                                        -show the winner/ tie
                                                        -play again/ change players/back to menu


Actual game: - Objective: collect as many rocks as you can in your bank (right side)
             - each player have: a row of 6 holes, each containing 4 rocks and an emplty banck
             - select a random player who will start the game -> players turns will be flagged by a sign on their's
               avatar
             - the first player will select a hole
             - you can only move the rocks on your side
             - that hole will be cleared and the rocks will be placed one in each of the following pits in sequence
               (counterclockwise), but it will skip the opponent bank
                - if the last rock ends in the bank:
                        - that player have an extra move
                - if the last rock ends in an empty hole in the current player's base and if in the parallel hole are
                      rocks:
                        - the current player will move in the bank that last rock and all the rocks in the parallel hole
             - if only one player is out of rock:
                - the game end's and all the other player's rock will go in their bank
             - when the game end's:
                - the score will be shown
                - the winer/ tie
                - the score will be saved in a file
                - play again/ change player/ menu
