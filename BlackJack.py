# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
WIDTH = 600
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# Game
class Game:
    def __init__(self):
        self.in_play = False
        self.deck = Deck()
        self.player = Hand("Player")
        self.dealer = Hand("Dealer")
        self.score = 0
        self.deal()
        
    def __str__(self):
        return str(self.player) + "\n"  + str(self.dealer) + "\nScore " + str(self.score) + "\n" + self.outcome + "\n"

    def deal(self):
        if self.in_play:
            self.score -= 1
        self.deck.shuffle()
        self.player.clear()
        self.dealer.clear()
        self.player.add_card(self.deck.deal_card())
        self.player.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.outcome = ""
        self.in_play = True
    
    def hit(self):
        # if the hand is in play, hit the player
        if self.in_play:
            self.player.add_card(self.deck.deal_card())
            # if busted, assign an message to outcome, update in_play and score
            if self.player.busted():
                self.outcome = "You went bust and lose!"
                self.in_play = False
                self.score  -= 1
           
    def stand(self):
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        if self.in_play:
            while self.dealer.get_value() < 17:
                self.dealer.add_card(self.deck.deal_card())
            if self.dealer.busted():
                self.outcome = "Dealer has busted, you won!"
                self.in_play = False
                self.score  += 1
            else:
                if self.dealer.get_value() >= self.player.get_value():
                    self.outcome = "You lose!"
                    self.in_play = False
                    self.score  -= 1
                else:
                    self.outcome = "You won!"
                    self.in_play = False
                    self.score  += 1

    # draw handler    
    def draw(self, canvas):
        self.player.draw(canvas, [50, 400])
        pos = [50, 120]
        self.dealer.draw(canvas, pos)
        if self.in_play:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
            message = "Hit or Stand?"
        else:    
            canvas.draw_text("Dealer hand value: " + str(self.dealer.get_value()), (180, 260), 24, "White")
            message = "New deal?"

        canvas.draw_text("Dealer", (50, 100), 24, "Black")
        canvas.draw_text("Player", (50, 380), 24, "Black")
        canvas.draw_text(message, (250, 380), 24, "Black")
        canvas.draw_text(self.outcome, ((WIDTH - len(self.outcome) * 20) / 2, 330), 36, "Yellow")
        canvas.draw_text("Blackjack", (50, 50), 48, "Black")
        canvas.draw_text("Score: " + str(self.score), (360, 50), 36, "White")
        canvas.draw_text("Your hand value: " + str(self.player.get_value()), (180, 550), 24, "White")

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    BOUND = 21
    
    def __init__(self, name):
        self.name = name
        self.clear()

    def clear(self):
        self.cards = []
        
    def __str__(self):
        result = "Hand of " + self.name + ":"
        for card in self.cards:
            result += " " + str(card)
        result += ", value = " + str(self.get_value())
        return result

    def add_card(self, card):
        self.cards.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        has_ace = False
        result = 0
        for card in self.cards:
            result += VALUES[card.rank]
            if card.rank == 'A':
                has_ace = True
        if has_ace and (result + 10 <= Hand.BOUND):
            return result + 10
        else :
            return result

    def busted(self):
        return self.get_value() > Hand.BOUND
    
    def draw(self, canvas, p):
        pos = [p[0], p[1]]
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 20
 
        
# define deck class
class Deck:
    FULL_DESK = tuple([Card(s, r) for s in SUITS for r in RANKS])
    
    def __init__(self):
        self.shuffle()

    # add cards back to deck and shuffle
    def shuffle(self):
        self.current_deck = list(Deck.FULL_DESK)
        random.shuffle(self.current_deck)

    def deal_card(self):
        return self.current_deck.pop(0)
    
    def __str__(self):
        result = ""
        for card in self.current_deck:
            result += str(card) + " "
        return result

#define event handlers for buttons
game = Game()

# initialization frame
frame = simplegui.create_frame("Blackjack", WIDTH, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", game.deal, 200)
frame.add_button("Hit",  game.hit, 200)
frame.add_button("Stand", game.stand, 200)
frame.set_draw_handler(game.draw)

# get things rolling
frame.start()

# remember to review the gradic rubric