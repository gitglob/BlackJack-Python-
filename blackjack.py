from random import shuffle

class Table:
    def __init__(self, player_name):
        self.dealer = Dealer()
        self.player = Player(name=player_name)

        self.start_game()
        
    def start_game(self):        
        # check if both the player and the dealer have any money to start the game
        dc = self.dealer.check_money()
        pc = self.player.check_money()
        if (not dc) or (not pc):
            return
        
        print("New round! Dealing cards...")
        
        # initiate hand, score, bet variables for both dealer and player
        self.dealer.init_round()
        self.player.init_round()
        
        # deal first 2 cards
        card = self.dealer.draw_card()
        self.player.get_card(card)
        
        card = self.dealer.draw_card()
        self.dealer.get_card(card)
        
        # start the game with player's turn
        print ("\t\t\t\tPlayer's turn...")
        bet = self.player.make_bet(self.dealer.cash)
        self.dealer.accept_bets(bet)
        card = self.dealer.draw_card()
        self.player.get_card(card)
        
        # repeatedly ask player if he wants another card
        while(True):
            choice = self.player.continue_or_stop(self.dealer)
            if (choice=="stop"):
                break
        
        # dealer draws cards
        if self.player.score==21:
            print ("Congrats!! BlackJack!!")
        else:
            print ("\t\t\t\tDealer's turn...")
            self.dealer.draw_max()
               
        # check who wins this battle
        winner = self.check_who_won()
        
        # adjust cash according to who won
        self.adjust_cash(winner)
        
        # show player his money
        print ("Your current stash is: {}".format(self.player.cash))
        
        # check if player wants another turn
        answer = self.player.new_game()
        if answer=='y':
            self.start_game()
    
    # function to find out who won this turn
    def check_who_won(self):
        if self.dealer.score<=21 and self.player.score>21:
            winner = 'd'
            print ("\n\nDealer wins!!!")
        elif self.player.score<=21 and self.dealer.score>21:
            winner = 'p'
            print ("\n\nPlayer wins!!!")
        elif self.player.score>21 and self.dealer.score>21:
            winner = 't'
            print ("It's a tie!")
        elif self.dealer.score>=self.player.score:
            winner = 'd'
            print ("\n\nDealer wins!!!")
        elif self.player.score>self.dealer.score:
            winner = 'p'
            print ("\n\nPlayer wins!!!")
        return (winner)
    
    # function to adjust cash
    def adjust_cash(self, winner):
        if winner=='d':
            self.dealer.win()
        elif winner=='p':
            self.player.win()
        else:
            self.dealer.tie()
            self.player.tie()
    
    # check if a card is an 'A'
    @staticmethod
    def is_ace(card):
        if len(card)==2:
            return (False)
        else:
            return (True)
    
    # check if an 'A' counts as 1 or 11
    @staticmethod
    def one_or_eleven(score):
        if score<=10:
            return (11)
        else:
            return (1)
        
class Dealer:
    def __init__(self):
        self.deck = Deck()
        
        self.name = "Dealer"
        self.cash = 500000
        
    def init_round(self):
        self.score = 0
        self.hand = []
        
    def draw_card(self):
        card = self.deck.pop_card()
        return(card)
        
    def get_card(self, card):
        self.hand.append(card[0])
        
        if Table.is_ace(card):
            ace_score = Table.one_or_eleven(self.score)
            self.score += ace_score
        else:
            self.score += card[1]
        
        print ("Dealer's hand: {}".format(self.hand))
        print ("Dealer's score: {}".format(self.score))
        
    def draw_max(self):
        while(True):
            card = self.draw_card()
            self.get_card(card)
            if (self.score>=17):
                break
            
    def accept_bets(self, bet):
        self.bet = bet
        self.cash -= bet       
        
    def win(self):
        self.cash += (2*self.bet)
        
    def tie(self):
        self.cash += self.bet
        
    # check if Dealer has money
    def check_money(self):
        if self.cash>0:
            return(True)
        elif self.cash==0: 
            print ("You fucking won. There is no more money!!!")
            return(False)
        else:
            print ("HOW can the dealer have NEGATIVE money????")
            return (False)
        
class Player:
    def __init__(self, name):
        self.name = name
        self.cash = 10000
        
    def init_round(self):
        self.score = 0
        self.hand = []
        
    def get_card(self, card):
        self.hand.append(card[0])
        
        if Table.is_ace(card):
            ace_score = Table.one_or_eleven(self.score)
            self.score += ace_score
        else:
            self.score += card[1]
        
        print ("Player's hand: {}".format(self.hand))        
        print ("Player's score: {}".format(self.score))
        
    # function to ask the player if he wants to continue
    def continue_or_stop(self, dealer):
        option = 'x'
        if self.score<21:
            option = self.hit_or_stick()
        if option=='h':
            card = dealer.draw_card()
            self.get_card(card)
            return("continue")
        else:
            return ("stop")
    
    # function to ask the player how much money does the player bet
    def make_bet(self, dealer_cash):
        print ("You currently have {} slurpaks".format(self.cash))
        print ("The Dealer has {} slurpaks".format(dealer_cash))
        while (True):            
            while(True):
                try:
                    bet = int(input("How many slurpaks do you bet? \nAccepted range : [1, min(your cash/dealer's cash)] \n"))
                    break
                except:
                    print ("\tInsert an integer in the accepted range pliz")
                
            if bet<=self.cash and bet<=dealer_cash and bet>0:
                self.bet = bet
                break
        self.cash -= bet
        return (bet)
        
    # ask player is he wants to play another round
    def new_game(self):
        while(True):
            answer = input("Do you want to play another round?? (Y)es / (N)o \n")
            if answer.lower()=='y' or answer.lower()=='n':
                break
        return (answer)
    
    def win(self):
        self.cash += (2*self.bet)
        
    def tie(self):
        self.cash += self.bet
        
    # check if player has money
    def check_money(self):
        if self.cash>0:
            return(True)
        elif self.cash==0: 
            print ("You ran out of money. Go tell your family you disgusting addicted person that needs help...")
            return(False)
        else:
            print ("HOW can you have NEGATIVE money????")
            return (False)
        
    # function that prints hit/stick option message
    @staticmethod
    def hit_or_stick():
        while (True):
            option = input("Do you want to : (H)it / (S)tick ?\n")
            if (option=='h' or option=='H') or (option=='s' or option=='S'):
                break
            
        return (option.lower())
        
class Deck:
    def __init__(self):
        self.stack = [['A',1,11], ['2',2], ['3',3], ['4',4], ['5',5], ['6',6], 
                      ['7',7], ['8',8], ['9',9], ['10',10], ['J',10], ['Q',10], ['K',10]]*4
        self.shuffle()
        
    def shuffle(self):
        shuffle(self.stack)
        print ("\nShuffling...\n")
        
    def pop_card(self):
        # checking if deck is empty. If it is get a new one
        if not self.stack:
            print ("\t\t\t\t\tDeck is over. Getting a new one...")
            self.new_deck()
        
        card = self.stack.pop()
        print ("Drew a(n) {}!".format(card))
        return(card)     
        
    def new_deck(self):
        self.stack = [['A',1,11], ['2',2], ['3',3], ['4',4], ['5',5], ['6',6], 
                      ['7',7], ['8',8], ['9',9], ['10',10], ['J',10], ['Q',10], ['K',10]]*4
        self.shuffle()

def main():

    player_name = input("This is BlackJack (I think) and you are about to lose imaginary money!  What's your name?\n")
    Table(player_name=player_name)

if __name__ == '__main__':

    main()