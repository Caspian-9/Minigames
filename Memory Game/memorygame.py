from fltk import *
import os, random

def t():
    x = int(timer.value())
    x += 1
    y = str(x)
    timer.value(y)
    Fl.repeat_timeout(1.0, t)

def but_cb(wid): #button callback function
	idx = B.index(wid)
	wid.image(imgpics[idx])
	wid.redraw()
	if len(upturned) == 2 and imgnams[B.index(upturned[0])] == imgnams[B.index(upturned[1])]: #2 images are the same
		for x in upturned:
			x.deactivate()
		upturned.clear()
	elif len(upturned) == 3: #2 images are not the same
		for x in upturned:
			if x != wid:
				x.image(None)
	if len([x for x in B if x.active() == False]) == 16: #inactive clicked buttons, game over
		Fl.remove_timeout(t)
		fl_message('total time taken:' + timer.value() + ' secs')
	win.redraw()
	upturned.clear()
				
	upturned.append(imgnams[idx])
	wid.redraw()
	print(upturned)

def btncount():
    upturned = []
    for x in B:
        if x.image() != None and x.active() == True:
            upturned.append(x) 
    return upturned

win = Fl_Window(600, 50, 400, 500)

imgnams = []
for name in os.listdir():
	if name.endswith('.png'):
		imgnams.append(name)
imgnams = imgnams * 2 #doubles the string list
random.shuffle(imgnams)

imgpics = [Fl_PNG_Image(name).copy(90, 90) for name in imgnams]

upturned = []


B = []
win.begin()
for x in range(4): #4 rows
	for y in range(4): #4 buttons each row
		B.append(Fl_Button(x*100, y*100, 100, 100))
		B[-1].callback(but_cb)
win.end()

win.show()
Fl.run()
