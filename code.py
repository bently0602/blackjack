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
        insurance_bet = 0
        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]
        # Check for insurance
        if dealer_hand[0]['rank'] == 'A':
            display_hands(player_hand, dealer_hand, hide_dealer=True)
            max_insur = bet / 2
            while True:
                insurance = input(
                    "\nDealer has an Ace. Do you want to take insurance? (y/n): "
                ).lower()
                if insurance in ['y', 'yes']:
                    while True:
                        try:
                            insur = float(input(
                                f"Enter insurance bet (up to ${max_insur}): "
                            ))
                            if 0 < insur <= max_insur:
                                insurance_bet = insur
                                balance -= insurance_bet
                                break
                            else:
                                print(
                                    f"Invalid bet. Enter up to ${max_insur}."
                                )
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    break
                elif insurance in ['n', 'no']:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        # Check for dealer blackjack
        dealer_blackjack = False
        if dealer_hand[0]['rank'] in ['A', '10', 'J', 'Q', 'K']:
            if calculate_hand(dealer_hand) == 21:
                dealer_blackjack = True
        # Check for player blackjack
        player_blackjack = calculate_hand(player_hand) == 21
        if dealer_blackjack:
            display_hands(player_hand, dealer_hand, hide_dealer=False)
            if insurance_bet > 0:
                print("Dealer has blackjack. Insurance bet pays 2:1.")
                balance += insurance_bet * 2
            if player_blackjack:
                print("Both dealer and player have blackjack. Push.")
            else:
                print("Dealer has blackjack. You lose.")
                balance -= bet
            continue
        if player_blackjack:
            display_hands(player_hand, dealer_hand, hide_dealer=False)
            print("Blackjack! You win 1.5x your bet.")
            balance += int(1.5 * bet)
            continue
        # Offer surrender
        if len(player_hand) == 2:
            while True:
                surrender = input(
                    "\nDo you want to surrender? (y/n): "
                ).lower()
                if surrender in ['y', 'yes']:
                    print("You surrendered. Half your bet is returned.")
                    balance -= bet / 2
                    break
                elif surrender in ['n', 'no']:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            if surrender in ['y', 'yes']:
                continue
        # Player's turn
        split_hands = []
        current_hand = player_hand.copy()
        current_bet = bet
        can_split = (
            len(current_hand) == 2 and
            current_hand[0]['rank'] == current_hand[1]['rank'] and
            balance >= bet
        )
        while True:
            display_hands(current_hand, dealer_hand, hide_dealer=True)
            player_total = calculate_hand(current_hand)
            if player_total > 21:
                print("You busted! Dealer wins.")
                balance -= current_bet
                break
            actions = {'h': 'hit', 's': 'stand'}
            if len(current_hand) == 2:
                actions['d'] = 'double down'
                if can_split:
                    actions['p'] = 'split'
            choice = get_player_choice(actions)
            if choice == 'hit':
                current_hand.append(deal_card(deck))
            elif choice == 'stand':
                break
            elif choice == 'double down':
                if balance < current_bet:
                    print("Insufficient balance to double down.")
                    continue
                balance -= current_bet
                current_bet *= 2
                current_hand.append(deal_card(deck))
                player_total = calculate_hand(current_hand)
                display_hands(current_hand, dealer_hand, hide_dealer=True)
                if player_total > 21:
                    print("You busted! Dealer wins.")
                    balance -= current_bet
                break
            elif choice == 'split':
                if not can_split:
                    print("Cannot split this hand.")
                    continue
                balance -= current_bet
                hand1 = [current_hand[0], deal_card(deck)]
                hand2 = [current_hand[1], deal_card(deck)]
                split_hands.append((hand1, current_bet))
                split_hands.append((hand2, current_bet))
                break
        # Handle split hands
        for hand, hand_bet in split_hands:
            current_hand = hand.copy()
            current_bet = hand_bet
            while True:
                display_hands(current_hand, dealer_hand, hide_dealer=True)
                player_total = calculate_hand(current_hand)
                if player_total > 21:
                    print("You busted! Dealer wins.")
                    balance -= current_bet
                    break
                actions = {'h': 'hit', 's': 'stand'}
                if len(current_hand) == 2 and balance >= current_bet:
                    actions['d'] = 'double down'
                choice = get_player_choice(actions)
                if choice == 'hit':
                    current_hand.append(deal_card(deck))
                elif choice == 'stand':
                    break
                elif choice == 'double down':
                    if balance < current_bet:
                        print("Insufficient balance to double down.")
                        continue
                    balance -= current_bet
                    current_bet *= 2
                    current_hand.append(deal_card(deck))
                    player_total = calculate_hand(current_hand)
                    display_hands(current_hand, dealer_hand, hide_dealer=True)
                    if player_total > 21:
                        print("You busted! Dealer wins.")
                        balance -= current_bet
                    break
        # Dealer's turn
        display_hands(player_hand, dealer_hand, hide_dealer=False)
        dealer_total = calculate_hand(dealer_hand)
        while dealer_total < 17:
            dealer_hand.append(deal_card(deck))
            dealer_total = calculate_hand(dealer_hand)
            display_hands(player_hand, dealer_hand, hide_dealer=False)
        if dealer_total > 21:
            print("Dealer busted! You win.")
            balance += bet
        else:
            player_total = calculate_hand(player_hand)
            if player_total > dealer_total:
                print("You win!")
                balance += bet
            elif player_total < dealer_total:
                print("Dealer wins.")
                balance -= bet
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