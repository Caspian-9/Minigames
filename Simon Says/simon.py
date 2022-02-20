from fltk import *
import os, subprocess

def click(wid): 
	print("on")
	
#def showflash(seq):
	#going to call on() with the integers in seq
	
def on(fpos):
	B[fpos].value(1)
	Fl.add_timeout(0.5, off, fpos) #release 0.5s later
	
def off(fpos):
	B[fpos].value(0)
	

col = [fl_rgb_color(29, 183, 39), fl_rgb_color(236, 19, 19), fl_rgb_color(31, 140, 229), fl_rgb_color(255, 229, 49)]
coliter = iter(col)
flashseq = [] 

B = []
win = Fl_Window(500, 500, 500, 500, "reee")
win.begin()
start = Fl_Button(100, 250, 70, 30, "BRUH")

for x in range(2):
	for y in range(2):
		B.append(Fl_Button(y*200+50, x*200+25, 200, 200))
		B[-1].callback(click)
		B[-1].color(next(coliter))
		B[-1].deactivate()



win.end()

Fl.scheme("gtk+")
win.show()
Fl.run()

#play sound: subprocess.Popen("mpv", filename)
