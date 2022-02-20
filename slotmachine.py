from fltk import *
import random, os

def foo(wid):
	if wid.label() == 'you CLICCED':
		wid.label('UNCLICC')
	else:
		wid.label('you CLICCED')
	oof()
	
def play_cb(wid):
	showfruit = []
	N = F[:] #full slice, refresh every callback
	fruit = random.choice(N)
	showfruit.append(fruit)
	for x in range(int(cheater.value())*2):
		N.append(fruit)
	print(N)
	
	for x in range(1, len(B)):
		fruit = random.choice(N)
		showfruit.append(fruit)
		
	if len(set(showfruit)) == 1:
		fl_message('You win')

F=[]
for f in os.listdir():
	if f.endswith('.png'):
		F.append(f)
I = [Fl_PNG_Image(f).copy(100,80) for f in N] #list comprehension

lis = ['badeline.png', 'calawot.png', 'ech.png', 'thelorde.png', 'uncomfortablemadeline,png']
showfruit
K = [Fl_PNG_Image(i).copy(100,80) for i in lis] #make 3 images, the ones to be shown

win=Fl_Window(800, 100, 400, 400, 'SlotMachine.py') #window, box, button, slider
win.begin()
B = []
for x in range(3):
	B.append(Fl_Box((30+(100*x)), 80, 100, 80))
	B[-1].box(FL_DOWN_BOX)
play = Fl_Return_Button(30,300,60,30, 'Click to win')
win.end()
#widget,tooltip() to display a message when the mouse is hovering over the widget, miniature help for the user

win.show()
Fl.run()
