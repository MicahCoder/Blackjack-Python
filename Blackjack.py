import random
from time import sleep
suitStrings = ["♥","♦","♣","♠"]
cardStrings = ["K","A","2","3","4","5","6","7","8","9","10","J","Q"]
blankCard = "\33[48;5;m??\033[0m"
class Card:
    def __init__(*args):
        if(len(args)==3):
            args[0].suit = args[1]
            args[0].value = args[2]
            args[0].id = 13*args[1] + args[2] + 1
        elif(len(args) == 2):
            args[0].id = args[1]
            args[0].value = args[1]%13
            args[0].suit = int(args[1]/13)
        
    def getWorth(self):
        if(self.value == 0 or self.value >9):
            return 10
        elif(self.value==1):
            return 11
        else:
            return self.value
    def reevaluate(self):
        if(self.value==1):
            return 1
        else:
            return self.getWorth()
    def __str__(self):
        out = "\033[0;31m\033[47m" if self.suit<2 else "\033[0;30m\033[47m"
        out += cardStrings[self.value]+suitStrings[self.suit]+"\033[0m"
        return out
class Deck:
    def __init__(self):
        self.deck=[]
        for id in range(0,52):
            self.deck.append(Card(id))
        self.shuffle()
    def get(self,number):
        return self.deck[number]
    def shuffle(self):
        random.shuffle(self.deck)
    def __len__(self):
        return len(self.deck)
    def remove(self, number):
        out = self.deck[number]
        self.deck.pop(number)
        return out
    def putBottom(self,card):
        self.deck.append(card)
    def getBottom(self):
        return self.remove(len(self.deck)-1)
class Player:
    def __init__(self,deck):
        self.deck = deck
        self.cards = []
        self.hit()
    def hit(self):
        self.cards.append(self.deck.remove(0))
    def handValue(self):
        out = 0
        for i in self.cards:
            out += i.getWorth()
        count =0
        while(count<len(self.cards) and out>21):
            out -= self.cards[count].getWorth()
            out += self.cards[count].reevaluate()
            count+=1
        return out
    def worthNeeded(self):
        return 21-self.handValue()
    def getOddsOfWin(self):
        count = 0
        needed = self.worthNeeded()
        if(needed==1):
            for i in range(0,len(self.deck)):
                if(self.deck.get(i).getWorth() ==11):
                    count+=1
        else:
            for i in range(0,len(self.deck)):
                if(self.deck.get(i).getWorth() == needed):
                    count+=1
        #print("Card needed for BJ is " + str(Card(needed)))
        return count/len(self.deck)*100
    def getOddsOfBust(self):
        count = 0
        needed = self.worthNeeded()
        if(needed==1):
            for i in range(0,len(self.deck)):
                if(self.deck.get(i).getWorth() !=11):
                    count+=1
        elif(needed == 0):
            return 100
        else:
            for i in range(0,len(self.deck)):
                if(self.deck.get(i).getWorth() > needed and self.deck.get(i).getWorth()!=11):
                    count+=1
        return count/len(self.deck)*100
    def returnCard(self,card):
        self.deck.putBottom(self.cards[len(self.cards)-1])
        self.cards.pop(len(self.cards)-1)
    def getCardBack(self):
        self.cards.append(self.deck.getBottom())
    def __str__(self):
        out = ''
        for i in self.cards:
            out+= str(i)+" "
        return out
def play():
    deck = Deck()
    dealer = Player(deck)
    player = Player(deck)
    imperfectBJ = True
    player.hit()
    dealer.hit()
    if(player.handValue() == 21 or dealer.handValue() == 21):
        imperfectBJ = False
        print("Blackjack!")
    else:
        dealer.returnCard(1)
    while(imperfectBJ):
        playerHit = False
        print("\033[H\033[2J")
        print("Dealer: " +str(dealer)+ blankCard)
        print("Player: " +str(player))
        print("Odds of Blackjack: " + str(player.getOddsOfWin()))
        print("Odds of Bust: " + str(player.getOddsOfBust()))
        print("Hit(h) or Stay(s)?")
        if(input().lower()=='h'):
            player.hit()
            playerHit = True
        if(player.handValue()>20):
            break
        if(not playerHit):
            break
    if(imperfectBJ):
        dealer.getCardBack()
    while(player.handValue()<22 and imperfectBJ):
        dealerHit = False
        print("\033[H\033[2J")
        print("Dealer: " +str(dealer)+" ")
        print("Player: " +str(player)+" ")
        print("Dealer Thinking...")
        sleep(1.5)
        if(dealer.handValue()<17):
            dealer.hit()
            dealerHit = True
            print("Dealer Hit!")
        if(dealer.handValue()>20):
            sleep(1.5)
            break
        if(not dealerHit):
            print("Dealer Stayed")
            sleep(1.5)
            break
        sleep(1.5)
    print("\033[H\033[2J")
    print("Dealer: " +str(dealer)+" ")
    print("Player: " +str(player)+" ")
    if(player.handValue()>21):
        print("Player busted, Dealer wins!")
    elif(dealer.handValue()>21):
        print("Dealer busted, Player wins!")
    elif(player.handValue()>dealer.handValue()):
        print("Player wins!")
    elif(player.handValue()<dealer.handValue()):
        print("Dealer wins!")
    else:
        print("Push")
play()
while(input("Press (q) to quit, otherwise press enter to play again.\n").lower() != 'q'):
    play()