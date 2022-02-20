import socket, sys
from fltk import *

#tcp
#python3 program.py server localhost 5555
#python3 program.py client localhost 5555

class Window (Fl_Window):
    
    def __init__(self, x, y, w, h, label):
        Fl_Window.__init__(self, x, y, w, h, label)
        self.begin()
        
        self.grid = []
        self.ships = []
        self.n = 9
        for i in range(self.n):    #9x9 grid
            for j in range(self.n):
                self.grid.append(Fl_Button(j*25+30, i*25+60, 25, 25))
                self.grid[-1].callback(self.placeships_cb)
                self.grid[-1].labelsize(24)
        
        self.lbUser = Fl_Box(60, 10, 150, 25, "My Battleships")
        for i in range(self.n):
            num_x = Fl_Box(30+i*25, 40, 25, 25, chr(i+65))  #A-J
        for i in range(self.n):
            num_x = Fl_Box(5, 60+i*25, 25, 25, str(i+1))  #1-10
            
        self.opponentGrid = []
        for i in range(self.n):    #opponent grid
            for j in range(self.n):
                self.opponentGrid.append(Fl_Button(j*25+300, i*25+60, 25, 25))
                self.opponentGrid[-1].callback(self.send_cb)
                self.opponentGrid[-1].deactivate()
                self.opponentGrid[-1].labelsize(24)
        
        self.lbOpponent = Fl_Box(330, 10, 150, 25, "Waiting for opponent")
        for i in range(self.n):
            num_x = Fl_Box(300+i*25, 40, 25, 25, chr(i+65))  #A-J
        for i in range(self.n):
            num_x = Fl_Box(275, 60+i*25, 25, 25, str(i+1))  #1-10
        
        self.ownShipsSunk = 0
        self.oppShipsSunk = 0
        self.lastOppClicked = 0

        self.ready = False
        self.opponentready = False
        self.btnStart = Fl_Button(95, 295, 80, 25, "Start")
        self.btnStart.callback(self.start_cb)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #using tcp
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.user = sys.argv[1]  #server or client
        self.host = sys.argv[2]  #localhost
        self.port = int(sys.argv[3])
        if self.user == "server":
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            self.conn, self.addr = self.sock.accept()    #blocked until client connects
            print("conn: ", self.conn)
            print("addr: ", self.addr)
            fd = self.conn.fileno()
        if self.user == "client":
            self.sock.connect((self.host, self.port))
            fd = self.sock.fileno()
        
        Fl.add_fd(fd, self.recv_data)
        #watches the fd file descriptor during the event loop. calls recv_data when socket receives something

        
    def placeships_cb(self, wid):
        ship = self.grid.index(wid)
        if ship not in self.ships:
            if len(self.ships) < 8:
                self.ships.append(ship)
                if self.user == "server":
                    wid.color(fl_rgb_color(240, 67, 29)) #red
                else:
                    wid.color(fl_rgb_color(50, 177, 227)) #blue
            else:
                fl_alert("You have reached the max number of ships")
        else:
            self.ships.remove(ship)
            wid.color(49)  #blank


    def start_cb(self, wid):    #opponent grid cb
        if len(self.ships) < 8:
            fl_alert("You must place 8 ships")
        else:
            self.ready = True
            if self.user == "server":
                self.conn.sendall("ready".encode())
            else: #client
                self.sock.sendall("ready".encode())
            if self.opponentready == True and self.ready == True:    #opponent is ready
                self.startgame()
    
    
    def send_cb(self, wid):
        self.lastOppClicked = self.opponentGrid.index(wid)   #idx of btn clicked
        print(self.lastOppClicked)
        if self.user == "server":
            self.conn.sendall(str(self.lastOppClicked).encode())
            self.switch_turn("client")
        else: #client
            self.sock.sendall(str(self.lastOppClicked).encode())
            self.switch_turn("server")
        self.check_for_winner()


    def recv_data(self, fd):
        if self.user == "server":
            data = self.conn.recv(1024)
            if data: print("receiving as server: ", data.decode())
        else:
            data = self.sock.recv(1024)
            if data: print("receiving as client: ", data.decode())
        data = data.decode()
        
        #check if data is int (idx of grid)
        try:
            hitidx = int(data)
        except ValueError:
            if data == '':  #prevents omega lag when either user disconnects
                return
            elif data == "ready":    #init
                self.opponentready = True
                if self.opponentready == True and self.ready == True: #opponent is ready
                    self.startgame()
            elif data == "hit":  #hit opponents ship
                self.opponentGrid[self.lastOppClicked].label('X')
                self.oppShipsSunk += 1
            else:  #missed opponents ship
                self.opponentGrid[self.lastOppClicked].label('O')        
        else:
            if self.user == "server":
                if hitidx in self.ships:
                    self.grid[hitidx].label('X')
                    self.conn.sendall("hit".encode())
                    self.ownShipsSunk += 1
                else:
                    self.grid[hitidx].label('O')
                    self.conn.sendall("miss".encode())
                self.switch_turn("server")
            else:
                if hitidx in self.ships:
                    self.grid[hitidx].label('X')
                    self.sock.sendall("hit".encode())
                    self.ownShipsSunk += 1
                else:
                    self.grid[hitidx].label('O')
                    self.sock.sendall("miss".encode())
                self.switch_turn("client")
        self.check_for_winner()
        

    def startgame(self):
        self.lbOpponent.label("Opponent's ships")
        self.lbOpponent.redraw()
        for a in self.opponentGrid:
            a.activate()
        for b in self.grid:
            b.deactivate()
        

    def switch_turn(self, currentPlayer):
        if self.user == currentPlayer:
            for b in self.opponentGrid:
                b.activate()
        else:
            for b in self.opponentGrid:
                b.deactivate()
            
    
    def check_for_winner(self):
        if len(self.ships) > 0:
            if self.oppShipsSunk == 8:  #win
                self.game_end(self.user)
            if self.ownShipsSunk == len(self.ships):  #lose
                if self.user == "server":
                    self.game_end("client")
                else:
                    self.game_end("server")
    
            
    def game_end(self, winner):
        for b in self.opponentGrid:
            b.deactivate()
        if winner == self.user:
            self.lbUser.label("you won")
        else:
            self.lbUser.label("you lost")        
        self.lbUser.redraw()
        

game = Window(50, 50, 540, 335, "Battleship " + sys.argv[1].upper())
game.show()
Fl.run()
