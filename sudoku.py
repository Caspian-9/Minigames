from fltk import *
import sys

class sudoku(Fl_Window):
    
    def __init__(self, x=0, y=0, w=300, h=400, label = None):
        Fl_Window.__init__(self, x, y, w, h, label)
        self.readdata()
        self.G = []
        self.n = int(len(self.nums)**0.5)
        
        for i in range(len(self.nums)):
            self.G.append(Fl_Input(*self.location(i), 30, 30))
            if self.nums[i] != '0':
                self.G[-1].value(self.nums[i])
                self.G[-1].deactivate()
            self.G[-1].textsize(24)
            self.G[-1].callback(self.printsets, len(self.G)-1)
        
        self.btnSolve = (Fl_Button(75, 310, 150, 30, "Solve"))
        self.btnSolve.callback(self.solve)
    
    def readdata(self):
        f = open(sys.argv[1], 'r')
        self.nums = []
        for char in f.read():
            if char == "\n":
                continue
            self.nums.append(char)
        f.close()
        
    def location(self, x):
        row = x // (self.n)
        col = x % (self.n)
        hsep = x // (self.n * 3)
        vsep = col // (self.n / 3)
        
        row = int(row * 30 + (10 * hsep))
        col = int(col * 30 + (10 * vsep))
        return((col,row))
    
    
    def rowind(self, x):
        s = []
        for i in range((self.n) ** 2):
            if x // self.n == i // self.n:
                s.append(i)
        return(s)
        
    def colind(self, x):
        s = []
        for i in range((self.n) **2):
            if x % self.n == i % self.n:
                s.append(i)
        return(s)
        
    def box(self, x):
        boxrow = x // (self.n * 3)
        boxcol = (x % self.n) // (self.n / 3)
        box = 3 * boxrow + boxcol
        return(box)
    
    def boxind(self, x):
        s = []
        for i in range((self.n) **2):
            if self.box(x) == self.box(i):
                s.append(i)
        return(s)
    
    def rowset(self, x):
        row = []
        for i in self.rowind(x):
            row.append(self.G[i].value())
        return(set(row) - {0} - {''})
    
    def colset(self, x):
        col = []
        for i in self.colind(x):
            col.append(self.G[i].value())
        return(set(col) - {0} - {''})
    
    def boxset(self, x):
        box = []
        for i in self.boxind(x):
            box.append(self.G[i].value())
        return(set(box) - {0} - {''})
    
    def printsets(self, wid, x):
        print("horizontal set = {}".format(self.rowset(x)))
        print("vertical set = {}".format(self.colset(x)))
        print("box set = {}".format(self.boxset(x)))
        
    def solve(self, wid):
        
        for i in range(len(self.G)):
            if self.G[i].active():
                possibleValues = set(range(1, 10))
#                possibleValues -= (self.rowset(i) |
#                                   self.colset(i) | 
#                                   self.boxset(i) )
                possibleValues -= set(self.rowset(i))
                possibleValues -= set(self.colset(i))
                possibleValues -= set(self.boxset(i))
                print(possibleValues)
                if len(possibleValues) == 1:
                    self.G[i].value = possibleValues.pop()
        
        
s = sudoku(50, 50, 300, 360, "Sudoku Solver")
s.show()
Fl.run()
