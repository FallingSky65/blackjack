# play blackjack against a computer!
# author: dan
# reason for making this: i was bored on the car ride

from Poker65.card import Card
from random import shuffle
from time import sleep
from os import system, name

def clear() -> None:
    if name == "nt": 
        system("cls")
    else:
        system("clear")

def get_value(card: Card) -> int:
    return [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11][card.rank]

def make_deck() -> list[Card]:
    deck: list[Card] = []
    for suit in range(4):
        for rank in range(13):
            deck.append(Card(suit=suit, rank=rank))
    return deck

def get_sum(hand: list[Card]) -> int:
    num_aces: int = 0
    sum: int = 0
    for card in hand:
        if card.rank == Card.rank2int('A'):
            num_aces += 1
        sum += get_value(card)
    while sum > 21 and num_aces > 0:
        sum -= 10
        num_aces -= 1
    return sum

def blackjack() -> int:
    deck = make_deck()
    shuffle(deck)

    player_cards: list[Card] = []
    dealer_cards: list[Card] = []

    # deal initial cards
    player_cards.append(deck.pop())
    dealer_cards.append(deck.pop())
    player_cards.append(deck.pop())
    dealer_cards.append(deck.pop())

    print(f"Dealer cards: XX {dealer_cards[1].__str__()}")
    print(f"Your cards: {' '.join([c.__str__() for c in player_cards])}\n")
    
    sleep(1)

    # player plays
    while get_sum(player_cards) < 21:
        if len(player_cards) > 2:
            print(f"Your cards: {' '.join([c.__str__() for c in player_cards])}")
        player_choice = input('Hit or stand? (enter h or s): ')
        while player_choice != 'h' and player_choice != 's': 
            player_choice = input('Enter a valid input: ')

        if player_choice == 'h': 
            player_cards.append(deck.pop())
        else:
            break
    print(f"Your cards: {' '.join([c.__str__() for c in player_cards])}")
    player_sum = get_sum(player_cards)
    if player_sum > 21:
        print('Bust!')
    elif player_sum == 21 and len(player_cards) == 2:
        print('Blackjack!')
    else:
        print(f'Your card total is {player_sum}')

    sleep(1)

    print("\nDealer's turn:")
    # dealer plays
    print(f"Dealer cards: {' '.join([c.__str__() for c in dealer_cards])}")
    sleep(1)
    while get_sum(dealer_cards) < 16:
        dealer_cards.append(deck.pop())
        print(f"Dealer cards: {' '.join([c.__str__() for c in dealer_cards])}")
        sleep(1)
    dealer_sum = get_sum(dealer_cards)
    if dealer_sum > 21:
        print('Bust!')
    elif dealer_sum == 21 and len(dealer_cards) == 2:
        print('Blackjack!')
    else:
        print(f'Dealer card total is {dealer_sum}')
    
    sleep(1)

    # print result
    print('\nResult:')
    if player_sum > 21:
        if dealer_sum > 21:
            print('Both busted, tie.')
            return 0
        else:
            print('Dealer wins.')
            return -1
    else:
        if dealer_sum > 21:
            print('Dealer busted, you win.')
            return 1
        else:
            if player_sum == dealer_sum:
                if len(player_cards) == len(dealer_cards):
                    print('Tie.')
                    return 0
                elif len(player_cards) < len(dealer_cards):
                    print('You win.')
                    return 1
                else:
                    print('Dealer wins.')
                    return -1
            elif player_sum > dealer_sum:
                print('You win.')
                return 1
            else:
                print('Dealer wins.')
                return -1

def blackjack_with_gambling() -> None:
    try:
        with open("wallet.txt", "r") as wallet_file:
            wallet: int = int(wallet_file.readline().replace('\n', ''))
    except:
        print("Failed to read from wallet.txt :(")
        return
    
    clear()
    print("Welcome to Blackjack!")
    sleep(1)
    print(f"You have ${wallet}")

    while True:
        if wallet <= 0:
            print("You're too broke to play, come back with some money...")
            with open("wallet.txt", "w") as wallet_file:
                wallet_file.write(str(wallet))
            return
        sleep(1)
        user_input = input("Enter your bet to play, or 'quit' to quit: ")
        while user_input.lower() != 'quit' and (not user_input.isdigit() or int(user_input) < 0 or int(user_input) > wallet):
            user_input = input("Enter a valid integer bet or 'quit': ")
        if user_input == 'quit': 
            print('Bye!')
            with open("wallet.txt", "w") as wallet_file:
                wallet_file.write(str(wallet))
            return
        bet: int = int(user_input)
        print("Good luck!")
        sleep(1)
        clear()
        result = blackjack()
        sleep(3)
        clear()
        if result > 0:
            wallet += bet
        if result < 0:
            wallet -= bet
       
        print(f"You now have ${wallet}")

blackjack_with_gambling()
