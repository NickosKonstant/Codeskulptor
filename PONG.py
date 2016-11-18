# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [3,4]

paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0 

score1 = 0
score2 = 0

# helper function that spawns a ball
def ball_init(right):
    ''' (bool) -> None

    Return a position vector and a velocity vector
    if right is True, spawn to the right, else spawn to the left
    '''
    global ball_pos, ball_vel 
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel =[0, 0]
    
    if right == True:
        ball_vel[0] = -random.randrange(2,4)
        ball_vel[1] = -random.randrange(1,3)
    else:
        ball_vel[0] = random.randrange(2,4)
        ball_vel[1] = -random.randrange(1,3) 
           
            
# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel 
    global score1, score2  
    
    ball_init(random.choice([True, False])) # Random choice of initial direction
    score1 = 0
    score2 = 0
        
    pass

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]    

    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

 
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    
    # draw paddles    
    c.draw_line([0,paddle1_pos],[PAD_WIDTH, paddle1_pos],PAD_HEIGHT,"Green")
    c.draw_line([WIDTH - PAD_WIDTH, paddle2_pos],[WIDTH - 1, paddle2_pos],PAD_HEIGHT,"Green")
     
    # update ball
    if ball_pos[0] <= BALL_RADIUS + HALF_PAD_WIDTH:
        if math.fabs(ball_pos[1] - paddle1_pos) <= PAD_HEIGHT:  
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] += 0.1 * ball_vel[0]	# ball speeds up a little 
            ball_vel[1] += 0.1 * ball_vel[1]           
        else:
            right = False						#ball spaws towards the scorer
            ball_init(right)					
            score2 += 1                        #Player 2 scores
            
    if ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - HALF_PAD_WIDTH:
        if math.fabs(ball_pos[1] - paddle2_pos) <= PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += 0.1 * ball_vel[0]
            ball_vel[1] += 0.1 * ball_vel[1]
        else:            
            right = True
            ball_init(right)
            score1 += 1                       #Player 1 scores 
            
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")   
    c.draw_text(str(score1),(200,100),52,"white")
    c.draw_text(str(score2),(350,100),52,"white")
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    acc = 5
    if key == simplegui.KEY_MAP["w"]:        
        paddle1_vel -= acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
              
    if key == simplegui.KEY_MAP["up"]:
         paddle2_vel -= acc
    elif key == simplegui.KEY_MAP["down"]:
         paddle2_vel += acc   
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel     
    
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0



# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)


# start frame
init()
frame.start()

