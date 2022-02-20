from fltk import *
import os, random
 
def generateBombs(wid):
    while len(Bombs) < 10:
        pos = random.randrange(81)
        if pos not in Bombs and pos != Buttons.index(wid):
            Bombs.append(pos)

def around(wid):
    idx = Buttons.index(wid)
    coord = coords[idx]
    x = coord[0]
    y = coord[1]
    
    neighbors = [(x-1,y), (x, y-1), (x, y+1), (x+1, y), (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
    realaround = []
    
    for loc in neighbors:
        if loc[0] < 0 or loc[1] < 0 or loc[0] > 8 or loc[1] > 8:
            continue
        a = coords.index(loc)
        realaround.append(a)
        
    return realaround


def countBombs(wid):
    A = around(wid)
    count = 0
    for a in A:
        if a in Bombs:
            count += 1
    return count


def showaround(wid):
    if wid.active() == 0:
        return
    
    else:
        wid.label(str(0))
        wid.deactivate()
        
        A = around(wid)
        for a in A:
            awid = Buttons[a]
            if countBombs(awid) == 0:
                showaround(awid)
            else:
                shownonzero(awid)
    

def shownonzero(wid):
    wid.label(str(countBombs(wid)))
    wid.deactivate()


def flagbutton(wid):
    idx = Buttons.index(wid)
    
    if idx in flagged:
        flagged.remove(idx)
        wid.image(None)
        wid.redraw()
    else:
        flagged.append(idx)
        wid.image(flagimg.copy(30,30))
        wid.redraw()
        

def hitbomb():
    for i in Bombs:
        Buttons[i].image(bombimg.copy(30,30))
        Buttons[i].redraw()

    for b in Buttons:
        b.deactivate()
    fl_message("ded")


def button_cb(wid):
    idx = Buttons.index(wid)
    coord = coords[idx]
    x = coord[0]
    y = coord[1]
    
    if len(Bombs) == 0:
        generateBombs(wid)
        print("Bombs: ", Bombs)
    
    if (Fl.event_button() == FL_RIGHT_MOUSE):
        flagbutton(wid)

    else:
        if idx in Bombs:
            hitbomb()
        else:
            if countBombs(wid) == 0:
                showaround(wid)
            else:
                shownonzero(wid)
            
    


#start
Buttons = []
Bombs = []
coords = []
flagged = []

bombimg = Fl_PNG_Image('bomb.png')
flagimg = Fl_PNG_Image('flag.png')

win = Fl_Window(700, 50, 330, 330, "minesweeper")
win.begin()

#generate 9x9 button grid
for x in range(9):
    for y in range(9):
        Buttons.append(Fl_Button(y*30+30, x*30+30, 30, 30))
        Buttons[-1].callback(button_cb)
        bcoord = (x,y)
        coords.append(bcoord)
    
#coords[Buttons.index(wid)] = coordinates of the button

win.end()


win.show()
Fl.run()
