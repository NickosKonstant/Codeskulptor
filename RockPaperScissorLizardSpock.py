# Mini-project  1 
# Rock-paper-scissors-lizard-Spock 


import random

def number_to_name(number):
    ''' (int) -> str

    Returns the name in which the number refers to,as
    described below:
    
    # 0 - rock
    # 1 - Spock
    # 2 - paper
    # 3 - lizard
    # 4 - scissor .

    >>>number_to_name(0)
        rock
    >>>number_to_name(3)
        lizard

    '''
    num = number % 5
    
    if num == 0:
        return "rock"
    elif num == 1:
        return "Spock"
    elif num == 2:
        return "paper"
    elif num == 3:
        return "lizard"
    else :
        return "scissors"


    
def name_to_number(name):
    ''' (str) -> int

    Returns the number assigned to the name,as
    described below:
    
    # 0 - rock
    # 1 - Spock
    # 2 - paper
    # 3 - lizard
    # 4 - scissor .

    >>>name_to_number("Spock")
        1
    >>>name_to_number("scissors")
        4
    '''
    
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    else :
        return 4
   

def rpsls(guess): 
    ''' (str) -> str
    
    Returns a brief of game's process.

    '''
    
    player_number = name_to_number(guess)
    computer_number = random.randrange(0,5)
    
    difference = (player_number - computer_number) % 5
    
    print "\n","Player chooses",guess,"\n","Computer chooses",number_to_name(computer_number)
      
        
    if difference == 1 or difference == 2:
        print("Player wins!")
    elif difference == 3 or difference == 4:
        print("Computer wins!")
    else:
        print("Tie!!!")
      

    
# test code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")



