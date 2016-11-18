# Mini project 5 - Memory

import simplegui
import random


# helper function to initialize globals
def init():
    global deck, exposed, state, match, moves
    
    exposed = []
    deck = []
    match = []
    state = 0
    moves = 0
    
    for i in range(8):					#create deck
        deck.extend((i,i))
        exposed.extend((False, False))
        
    random.shuffle(deck)    			#shuffle deck

     
# define event handlers
def mouseclick(pos):
    global mouse, state, match, moves, exposed
    
    mouse = list(pos)
    index = mouse[0] // 50
    
    if not exposed[index]:          
        if state == 0:				# Game begins
            exposed[index] = True
            match.append(index)
            
            state =1	
        
        elif state == 1:			# One card exposed
            exposed[index] = True
            match.append(index)
            
            state = 2
   
        elif state == 2:			#  Two cards exposed
            # Match check
            if deck[match[0]] != deck[match[1]]:
                exposed[match[0]] = False
                exposed[match[1]] = False
            
            match = []
            exposed[index] = True
            match.append(index)
            state = 1
            
            moves += 1  		# Turn counter
            l.set_text("Moves = "+str(moves))

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global mouse, moves

    pos = [10, 70]
    i= 0

    for card in deck:
        if exposed[i]:
            canvas.draw_text(str(card), pos ,40, "White")    
        else:           
            canvas.draw_polygon([(i*50,0),(50 + i*50,0),(50 +i*50,100),(i*50,100)],2,"red","green")    
                       
        pos[0] += 50
        i += 1
        

    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")


# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()

