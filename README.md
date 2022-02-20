# MiscSmallGames
Some small games written in Python3 or C++

The Python games require pyFLTK to run

To run the programs:
- Each folder or individual file in the MiscSmallGames folder is a separate game. Download everything in the individual game's folder, if applicable. The folder contains extra assets the program needs
- C++ files need to be compiled first
- Execute the .py file or compiled .o file in the command line


Instructions for battleship.py and tictactoe.py:
- These programs use TCP sockets to allow the server side and client side to communicate
- Currently can only run both server and client on 1 computer
- Must run server side first, and then connect the client to the server
- Execute in command line: 
  - $python3 program.py server localhost 5555
  - $python3 program.py client localhost 5555
