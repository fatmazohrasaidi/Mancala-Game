# Mancala Game: Minimax With Alpha-Beta Pruning

A Python implementation of the Mancala (Awalé) game using adversarial search.
This project models the Mancala board, the game logic, and an intelligent agent that plays using the Minimax algorithm with Alpha-Beta Pruning.  
This project is developed as part of Assignment 4 in the Problem Solving Module.
All class definitions and required functionalities are described in detail in the assignment PDF included in this repository.

# Features

- Full implementation of the Mancala board (6 pits per player + 2 stores).  
- Valid seed sowing mechanics (counter-clockwise movement).  
- Capture rule when the last seed lands in an empty pit.  
- Game-over rule: remaining seeds collected to the player's store.  
- Minimax with Alpha-Beta Pruning, configurable depth.  
- Human vs Computer gameplay.  
- AI vs AI mode included in the folder AI_vs_AI/, where two computer agents play against each other using minimax.  
- Game state evaluation based on store difference.  
- A simple graphical interface built with Pygame, allowing the user to visualize the board and interact with the game.

# How to run:  
- python main.py
