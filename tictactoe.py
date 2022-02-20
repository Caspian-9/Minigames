import socket, sys
from fltk import *

#udp
#python3 program.py server localhost 5555
#python3 program.py client localhost 5555

class Window (Fl_Window):
    
    def __init__(self, x, y, w, h, label):
        Fl_Window.__init__(self, x, y, w, h, label)  #create the window
        self.begin()
        self.grid = []
        self.n = 3
        for i in range(self.n):    #create a 3x3 grid of buttons
            for j in range(self.n):
                self.grid.append(Fl_Button(j*50+25, i*50+25, 50, 50))
                self.grid[-1].callback(self.send_cb)
                self.grid[-1].labelsize(36)
        self.statusLabel = Fl_Box(25, 200, 150, 25)
        self.user = sys.argv[1] #server or client
        self.host = sys.argv[2]
        self.port = int(sys.argv[3])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #using udp
        if self.user == "server":
            self.sock.bind((self.host, self.port))
            
        fd = self.sock.fileno()
        Fl.add_fd(fd, self.recv_data)
        #watches the fd file descriptor during the event loop. calls recv_data when socket receives something
        
    def send_cb(self, wid):
        buttonLocation = str(self.grid.index(wid))
        if self.user == "server":
            if hasattr(self, "addr"):    
                wid.label('O')
                wid.deactivate()    #server's turn finished
                self.switch_turn("client")    #is now client's turn
                self.sock.sendto(buttonLocation.encode(), self.addr) #server
            else:
                fl_alert("please wait for the client to move first")
        else: #client
            wid.label('X')
            wid.deactivate()    #client's turn finished
            self.switch_turn("server")    #is now server's turn
            self.sock.sendto(buttonLocation.encode(), (self.host, self.port))
        self.check_for_winner()
    
    def recv_data(self, fd):
        (buttonLocation, self.addr) = self.sock.recvfrom(1024)
        buttonLocation = int(buttonLocation.decode())
        if self.user == "server": #receiving as server
            self.grid[buttonLocation].label('X')
            self.switch_turn("server")
        else: #receiving as client
            self.grid[buttonLocation].label('O')
            self.switch_turn("client")
        self.grid[buttonLocation].deactivate()
        self.check_for_winner()


    def switch_turn(self, currentPlayer):
        if self.user == currentPlayer:    #my turn
            #activate all buttons with empty labels on my side
            for b in self.grid:
                if b.label() == None:
                    b.activate()
        else:
            #deactivate all buttons on my side
            for b in self.grid:
                b.deactivate()
            
    
    def check_for_winner(self):
        
        #check if each row has winner
        for i in range(self.n):    #get row indices
            indices = []
            for j in range(self.n):
                indices.append(i*self.n + j)
            winner = self.check_line(indices)
            if winner == 'O' or winner == 'X':
                #call game end with winner
                self.game_end(winner)
                return
        
        #check if each column has winner
        for i in range(self.n):    #get col indices
            indices = []
            for j in range(self.n):
                indices.append(j*self.n + i)
            winner = self.check_line(indices)
            if winner == 'O' or winner == 'X':
                #call game end with winner
                self.game_end(winner)
                return
        
        #check if each diagonal has winner
        indices = []
        for i in range(self.n):        #get top left to bottom right diagonal indices
            indices.append(i*self.n + i)
        winner = self.check_line(indices)
        if winner == 'O' or winner == 'X':
            #call game end with winner
            self.game_end(winner)
            return
        
        indices = []
        for i in range(1, self.n+1):  #get top right to bottom left diagonal indices
            indices.append(i * (self.n-1))
        winner = self.check_line(indices)
        if winner == 'O' or winner == 'X':
            #call game end with winner
            self.game_end(winner)
            return
        
        #check if all buttons have been clicked (label not empty)
        if len([b for b in self.grid if b.label() != None]) == len(self.grid):
            self.game_end('F')

    
    def check_line(self, indices):
        line = [self.grid[i].label() for i in indices]
        if line.count('O') == self.n:
            return('O')
        elif line.count('X') == self.n:
            return('X')
        else:
            return('F')
        
    
    def game_end(self, winner):
        for b in self.grid:
            b.deactivate()
        if winner == 'O':      #server win
            if self.user == "server":
                self.statusLabel.label("server wins")
            if self.user == "client":
                self.statusLabel.label("client loses")
        elif winner == 'X':    #client win
            if self.user == "client":
                self.statusLabel.label("client wins")
                self.statusLabel.redraw()
            if self.user == "server":
                self.statusLabel.label("server loses")
        else:                  #tie
            self.statusLabel.label("tie")
        
        self.statusLabel.redraw()
        


game = Window(50, 50, 200, 250, "Tic Tac Toe " + sys.argv[1].upper())
game.show()
Fl.run()
