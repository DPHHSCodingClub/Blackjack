import random

#a game has a board, and a hand
#for card games, both are populated by a deck

cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

#Our objective is to play the game multiple times with a rule
#First let's make a way to play the game

def playBlackjack():
    
    #Need a function to create a shuffled deck
    deck = shuffledDeck()
    
    #game starts with empty hands
    hand = []
    dealerHand = []
    
    #Dealing the initial hand
    #Need a hit function that deals a card out of the deck
    hit(hand, deck)
    hit(dealerHand, deck)
    hit(hand, deck)
    hit(dealerHand, deck)
    
    #Now that hands are dealt and game is initialized, we need to check if anyone has blackjack
    #Need a function that calculates value of hand
    if handCountHigh(hand) == 21:
        if handCountHigh(dealerHand) == 21:
            return 'draw'
        else:
            return 'win'
    elif handCountHigh(dealerHand) == 21:
        return 'lose'
        
    #Game is now initialized
    #Now we can allow the user to play until they bust or stay
    
    stay = False
    while (stay == False) and not bust(hand):
        #Show hands and ask user what they want to do
        print("Dealer Hand:\n")
        showHand(dealerHand, partial = True)
        print("Your Hand:\n")
        showHand(hand)
        
        print("hit or stay\n")
        decision = raw_input()
        if decision == 'hit':
            hit(hand, deck)
        elif decision == 'stay':
            stay = True
        else: print("hit or stay only\n")
        
    #if busting is the reason for exiting the loop, we lost
    if bust(hand):
        print("Your Hand:\n")
        showHand(hand)
        return 'loss'
        
    #dealer's turn to play
    #the dealer has no autonomy, they follow a rule so we can skip the play-by-play
    decision = decide(dealerHand, dealerHand, DEALERRULE)
    while decision == True:
        hit(dealerHand, deck)
        if bust(dealerHand): 
            print("Dealer Hand:\n")
            showHand(dealerHand)
            return 'win'
        decision = decide(dealerHand, dealerHand, DEALERRULE)
        
    #game is over, time to reveal results
    print("Dealer Hand:\n")
    showHand(dealerHand)
    print("Your Hand:\n")
    showHand(hand)
    
    #Now decide the results
    return results(hand, dealerHand)

#We need to populate the deck and shuffle it before we can play
def shuffledDeck():
    deck = (cards*4)*8 #Each deck is 4 of each card, and BJ in casinos is usually played with around 4 decks shuffled together
    random.shuffle(deck) #random.shuffle destructively modifies the list
    return deck
    
#The way I've used it, I want hit() to destructively modify hand and deck, removing a card from deck and adding it to hand
#Should return nothign        
def hit(hand, deck):
    hand.append(deck.pop())
    
#Calculates hand value using ace = 11, returns value
def handCountHigh(hand):
    cardValues = dict()
    cardValues['A'] = 11
    cardValues['2'] = 2
    cardValues['3'] = 3
    cardValues['4'] = 4
    cardValues['5'] = 5
    cardValues['6'] = 6
    cardValues['7'] = 7
    cardValues['8'] = 8
    cardValues['9'] = 9
    cardValues['10'] = 10
    cardValues['J'] = 10
    cardValues['Q'] = 10
    cardValues['K'] = 10
    
    value = 0
    for card in hand:
        value += cardValues[card]
    
    return value
    
#Calculates hand value using ace = 1, returns value
def handCountLow(hand):
    cardValues = dict()
    cardValues['A'] = 1
    cardValues['2'] = 2
    cardValues['3'] = 3
    cardValues['4'] = 4
    cardValues['5'] = 5
    cardValues['6'] = 6
    cardValues['7'] = 7
    cardValues['8'] = 8
    cardValues['9'] = 9
    cardValues['10'] = 10
    cardValues['J'] = 10
    cardValues['Q'] = 10
    cardValues['K'] = 10
    
    value = 0
    for card in hand:
        value += cardValues[card]
    
    return value

def bust(hand):
    if handCountLow(hand) > 21: return True
    return False

#Need to print something readable to the console
#I've added an optional argument so that this function can reveal the dealer's first card rather than writing a completely separate function to do almost the same thing    
def showHand(hand, partial = False):
    valH = handCountHigh(hand)
    valL = handCountLow(hand)
    
    text = ''
    if partial == True:
        text = hand[0]
        print(text)
        return
    for i in range(len(hand)):
        text += hand[i] + ' '
        
    print(text)
    print("value = {high}, {low}\n".format(high = valH, low = valL))
    
#decide needs to take your hand, the dealer's visible card, and your rule and return a decision on whether to hit or not   
def decide(hand, dealerHand, rule):
    visible = dealerHand[0]
    return rule(hand, visible)
#Here we've decided what rule is. It's a function that considers your hand, the visible card of the dealer, and returns a decision

def results(hand, dealerHand):
    handValue = handCountHigh(hand)
    if handValue > 21: handValue = handCountLow(hand)
    dealerHandValue = handCountHigh(dealerHand)
    if dealerHandValue > 21: dealerHandValue = handCountLow(dealerHand)
    
    if dealerHandValue == handValue: return 'draw'
    elif dealerHandValue < handValue: return 'win'
    else: return 'loss'

#prototypical rule for the dealer that never changes
#visible is irrelevant in this case
def DEALERRULE(dealerHand, visible):
    valHi = handCountHigh(dealerHand)
    valLo = handCountLow(dealerHand)
    assert(valLo > 0)
    assert(valHi > 0)
    if valHi < 17: return True
    if valHi >= 17 and valHi <= 21: return False
    if valLo >= 17: return False
    return True
    
#print(playBlackjack())

#lets make a function to keep playing, and count the wins

def playMultiple():
    play = True
    ws = 0
    ls = 0
    ds = 0
    while(play == True):
        result = playBlackjack()
        if result == 'win': ws += 1
        elif result == 'loss': ls += 1
        else: ds += 1
        print(result + '\n')
        
        print("Play another? (y/n)\n")
        inpt = input()
        if inpt == 'y': play = True
        else: play = False
        
    print("Ws    Ls    Ds\n")
    print("{W}    {L}    {D}".format(W = ws, L = ls, D = ds))

#playMultiple()
 
#Now that we're sattisfied our code can deal for us, let's make it play for us too
def playBlackjack(playerRule):
    
    #Need a function to create a shuffled deck
    deck = shuffledDeck()
    
    #game starts with empty hands
    hand = []
    dealerHand = []
    
    #Dealing the initial hand
    #Need a hit function that deals a card out of the deck
    hit(hand, deck)
    hit(dealerHand, deck)
    hit(hand, deck)
    hit(dealerHand, deck)
    
    #Now that hands are dealt and game is initialized, we need to check if anyone has blackjack
    #Need a function that calculates value of hand
    if handCountHigh(hand) == 21:
        if handCountHigh(dealerHand) == 21:
            return 'draw'
        else:
            return 'win'
    elif handCountHigh(dealerHand) == 21:
        return 'lose'
        
    #Game is now initialized
    #Now we can allow the user to play until they bust or stay
    
    stay = False
    while (stay == False) and not bust(hand):
        #Show hands and ask user what they want to do
        print("Dealer Hand:\n")
        showHand(dealerHand, partial = True)
        print("Your Hand:\n")
        showHand(hand)
        
        print("hit or stay\n")
        #playerRule decides if you want to hit, same as DEALERRULE
        if (playerRule(hand, dealerHand[0])):
            hit(hand, deck)
            print('hit\n')
        else:
            stay = True
            print('stay\n')
        
        #decision = input()
        #if decision == 'hit':
        #    hit(hand, deck)
        #elif decision == 'stay':
        #    stay = True
        #else: print("hit or stay only\n")
        
    #if busting is the reason for exiting the loop, we lost
    if bust(hand):
        print("Your Hand:\n")
        showHand(hand)
        return 'loss'
        
    #dealer's turn to play
    #the dealer has no autonomy, they follow a rule so we can skip the play-by-play
    decision = decide(dealerHand, dealerHand, DEALERRULE)
    while decision == True:
        hit(dealerHand, deck)
        if bust(dealerHand): 
            print("Dealer Hand:\n")
            showHand(dealerHand)
            return 'win'
        decision = decide(dealerHand, dealerHand, DEALERRULE)
        
    #game is over, time to reveal results
    print("Dealer Hand:\n")
    showHand(dealerHand)
    print("Your Hand:\n")
    showHand(hand)
    
    #Now decide the results
    return results(hand, dealerHand)
#Same thing, but remove input for determining what we want to do. Instead ask the function playerRule() to hit or stay  

def playerRule(hand, visible):
    valHi = handCountHigh(hand)
    valLo = handCountLow(hand)
    critVal = 15
    assumeValue = 10
    
    dealerVal = handCountHigh([visible]) + assumeValue
    
    if dealerVal >= 17: #play aggressively
        critVal = 18
        if valHi < critVal: return True
        if valHi >= critVal and valHi <= 21: return False
        if valLo >= critVal: return False
    
    assert(valLo > 0)
    assert(valHi > 0)
    if valHi < critVal: return True
    if valHi >= critVal and valHi <= 21: return False
    if valLo >= critVal: return False
    return True
    
#print(playBlackjack(playerRule))

#One more itteration, this time remove print statements so it can run many times without spaming
def playBlackjack(playerRule):
    
    #Need a function to create a shuffled deck
    deck = shuffledDeck()
    
    #game starts with empty hands
    hand = []
    dealerHand = []
    
    #Dealing the initial hand
    #Need a hit function that deals a card out of the deck
    hit(hand, deck)
    hit(dealerHand, deck)
    hit(hand, deck)
    hit(dealerHand, deck)
    
    #Now that hands are dealt and game is initialized, we need to check if anyone has blackjack
    #Need a function that calculates value of hand
    if handCountHigh(hand) == 21:
        if handCountHigh(dealerHand) == 21:
            return 'draw'
        else:
            return 'win'
    elif handCountHigh(dealerHand) == 21:
        return 'lose'
        
    #Game is now initialized
    #Now we can allow the user to play until they bust or stay
    
    stay = False
    while (stay == False) and not bust(hand):
        #Show hands and ask user what they want to do
        #print("Dealer Hand:\n")
        #showHand(dealerHand, partial = True)
        #print("Your Hand:\n")
        #showHand(hand)
        
        #print("hit or stay\n")
        #playerRule decides if you want to hit, same as DEALERRULE
        if (playerRule(hand, dealerHand[0])):
            hit(hand, deck)
            #print('hit\n')
        else:
            stay = True
            #print('stay\n')
        
        #decision = input()
        #if decision == 'hit':
        #    hit(hand, deck)
        #elif decision == 'stay':
        #    stay = True
        #else: print("hit or stay only\n")
        
    #if busting is the reason for exiting the loop, we lost
    if bust(hand):
        #print("Your Hand:\n")
        #showHand(hand)
        return 'loss'
        
    #dealer's turn to play
    #the dealer has no autonomy, they follow a rule so we can skip the play-by-play
    decision = decide(dealerHand, dealerHand, DEALERRULE)
    while decision == True:
        hit(dealerHand, deck)
        if bust(dealerHand): 
            #print("Dealer Hand:\n")
            #showHand(dealerHand)
            return 'win'
        decision = decide(dealerHand, dealerHand, DEALERRULE)
        
    #game is over, time to reveal results
    #print("Dealer Hand:\n")
    #showHand(dealerHand)
    #print("Your Hand:\n")
    #showHand(hand)
    
    #Now decide the results
    return results(hand, dealerHand)
    
#And a function to run it multiple times, and count the results
def winRate(n, rule):
    winCount = 0
    drawCount = 0
    lossCount = 0
    for i in range(n):
        result = playBlackjack(rule)
        if result == 'win':
            winCount = winCount + 1
        elif result == 'draw':
            drawCount = drawCount + 1
        else:
            lossCount = lossCount + 1
    return [winCount, drawCount, lossCount]
    
def printWR(n, rule):
    [w, d, l] = winRate(n, rule)
    print('W    D    L\n')
    print('{win}    {draw}    {loss}'.format(win = w, draw = d, loss = l))
    
#lets try some different rules

def playerRule2(hand, visible):
    valHi = handCountHigh(hand)
    valLo = handCountLow(hand)
    dealerVal = handCountHigh([visible])
    
    if valHi == 21 or valLo == 21: return False
    
    if valHi < 21 and valHi != valLo: #Soft case
        if valHi == 20: return False
        elif valHi == 19: return dealerVal == 6
        elif valHi == 18: return ((2 <= dealerVal) and (dealerVal <= 6)) or (9 <= dealerVal)
        else: return True
        
    else: #Ace's are 1, only valLo relevant
        if valLo >= 17: return False
        elif (13 <= valLo) and (valLo <= 16): return not ((2 <= dealerVal) and (dealerVal <= 6))
        elif valLo == 12: return not ((4 <= dealerVal) and (dealerVal <= 6))
        else: return True


printWR(100000, playerRule2)
