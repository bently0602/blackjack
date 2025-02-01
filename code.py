import random

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
             'J', 'Q', 'K', 'A']
    deck = [{'suit': suit, 'rank': rank} for suit in suits
            for rank in ranks] * 6
    random.shuffle(deck)
    return deck

def deal_card(deck):
    if len(deck) < 15:
        deck.extend(create_deck())
    return deck.pop()

def calculate_hand(hand):
    value = 0
    aces = 0
    for card in hand:
        rank = card['rank']
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            aces += 1
            value += 11
        else:
            value += int(rank)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_hands(player_hand, dealer_hand, hide_dealer=False):
    print("\nDealer's hand:")
    if hide_dealer:
        print("  <hidden card>")
        print(f"  {dealer_hand[1]['rank']} of {dealer_hand[1]['suit']}")
    else:
        for card in dealer_hand:
            print(f"  {card['rank']} of {card['suit']}")
        print(f"Dealer's hand value: {calculate_hand(dealer_hand)}")
    print("\nYour hand:")
    for card in player_hand:
        print(f"  {card['rank']} of {card['suit']}")
    print(f"Your hand value: {calculate_hand(player_hand)}")

def get_player_choice(allowed):
    while True:
        choice = input("\nChoose an action: ").lower()
        if choice in allowed:
            return allowed[choice]
        else:
            print("Invalid input. Please choose a valid action.")

def get_bet(balance):
    while True:
        try:
            bet = int(input(f"\nYou have ${balance}. Enter your bet: "))
            if bet > 0 and bet <= balance:
                return bet
            else:
                print(f"Invalid bet. Enter a positive number up to ${balance}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_blackjack():
    deck = create_deck()
    balance = 1000
    print("Welcome to Blackjack!")
    while balance > 0:
        print(f"\nCurrent balance: ${balance}")
        bet = get_bet(balance)
        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]
        player_split = False
        split_hands = []
        current_hand = player_hand.copy()
        while True:
            display_hands(current_hand, dealer_hand, hide_dealer=True)
            player_total = calculate_hand(current_hand)
            if player_total == 21:
                print("Blackjack! You might win!")
                break
            actions = {'h': 'hit', 's': 'stand'}
            if len(current_hand) == 2 and balance >= bet:
                actions['d'] = 'double down'
                if current_hand[0]['rank'] == current_hand[1]['rank']:
                    actions['p'] = 'split'
            choice = get_player_choice(actions)
            if choice == 'hit':
                current_hand.append(deal_card(deck))
                player_total = calculate_hand(current_hand)
                if player_total > 21:
                    display_hands(current_hand, dealer_hand, hide_dealer=True)
                    print("You busted! Dealer wins.")
                    balance -= bet
                    break
            elif choice == 'stand':
                break
            elif choice == 'double down':
                additional_bet = bet
                if additional_bet > balance:
                    print("Insufficient balance to double down.")
                    continue
                bet += additional_bet
                current_hand.append(deal_card(deck))
                player_total = calculate_hand(current_hand)
                display_hands(current_hand, dealer_hand, hide_dealer=True)
                if player_total > 21:
                    print("You busted! Dealer wins.")
                    balance -= bet
                    break
                else:
                    break
            elif choice == 'split':
                split_hands = [
                    [current_hand[0], deal_card(deck)],
                    [current_hand[1], deal_card(deck)]
                ]
                balance -= bet
                player_split = True
                break
        if player_split:
            for hand in split_hands:
                current_hand = hand
                print("\nPlaying split hand:")
                while True:
                    display_hands(current_hand, dealer_hand, hide_dealer=True)
                    player_total = calculate_hand(current_hand)
                    if player_total == 21:
                        print("Blackjack!")
                        break
                    actions = {'h': 'hit', 's': 'stand'}
                    if len(current_hand) == 2 and balance >= bet:
                        actions['d'] = 'double down'
                    choice = get_player_choice(actions)
                    if choice == 'hit':
                        current_hand.append(deal_card(deck))
                        player_total = calculate_hand(current_hand)
                        if player_total > 21:
                            display_hands(current_hand, dealer_hand, hide_dealer=True)
                            print("You busted! Dealer wins.")
                            balance -= bet
                            break
                    elif choice == 'stand':
                        break
                    elif choice == 'double down':
                        additional_bet = bet
                        if additional_bet > balance:
                            print("Insufficient balance to double down.")
                            continue
                        bet += additional_bet
                        current_hand.append(deal_card(deck))
                        display_hands(current_hand, dealer_hand, hide_dealer=True)
                        player_total = calculate_hand(current_hand)
                        if player_total > 21:
                            print("You busted! Dealer wins.")
                            balance -= bet
                            break
                        else:
                            break
        if calculate_hand(player_hand) <= 21 and not player_split:
            display_hands(player_hand, dealer_hand, hide_dealer=False)
            while calculate_hand(dealer_hand) < 17:
                dealer_hand.append(deal_card(deck))
                display_hands(player_hand, dealer_hand, hide_dealer=False)
                if calculate_hand(dealer_hand) > 21:
                    print("Dealer busted! You win.")
                    balance += bet
                    break
            else:
                dealer_total = calculate_hand(dealer_hand)
                player_total = calculate_hand(player_hand)
                if dealer_total > player_total:
                    print("Dealer wins.")
                    balance -= bet
                elif dealer_total < player_total:
                    print("You win!")
                    balance += bet
                else:
                    print("It's a tie!")
        if balance <= 0:
            print("You have no more money! Game over.")
            break
        while True:
            replay = input("\nDo you want to play again? (y/n): ").lower()
            if replay in ['y', 'yes']:
                break
            elif replay in ['n', 'no']:
                print(f"You leave the game with ${balance}.")
                return
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == '__main__':
    play_blackjack()