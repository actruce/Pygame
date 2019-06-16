#------------------------------------------------------
# Common Classes for Playig Game

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def GetRank(self):
        return self.rank

    def GetSuit(self):
        return self.suit

    def __str__(self):
        return '(suit:' + str(self.suit) + ', rank: ' + str(self.rank) + ')'

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.holecards = []
        self.round_result = None
        self.current_money = 100
        self.current_status = "Alive"

    def add_cards(self, aCard):
        self.holecards.append(aCard)

    def init_holecards(self):
        self.holecards = []

    # choose the best cards
    def choice_best_cards(self, community_cards):
        new_list = self.holecards + community_cards
        result = PokerHelper.GetBestChoise(new_list)
        self.round_result = result

    # betting & money related codes
    def bet_money(self, bet_amount):
        if(self.current_money >= bet_amount):
            return self.withdraw_money(bet_amount)


    def withdraw_money(self, withdraw_amount):
        if(self.current_money > withdraw_amount):
            self.current_money -= withdraw_amount
            return "normal"
        elif(self.current_money == withdraw_amount):
            self.current_money = 0
            return "allin"
        else:
            return "abnormal"

    def get_pot_money(self, pot_amount):
        return self.save_money(pot_amount)

    def save_money(self, save_amount):
        self.current_money += save_amount
        return "saved"

class Community:
    def __init__(self):
        self.community_cards = []

    def add_cards(self, aCard):
        self.community_cards.append(aCard)

import random
class Deck:
    def __init__(self):
        self.deck_cards = []

    def InitializeDeck(self):
        self.deck_cards = []

        # write some codes for initialize the deck
        for i in range(0, 4):
            for j in range(0, 13):
                self.deck_cards.append(Card(i, j))

    def ShuffleDeck(self):
        shuffled_cards = []

        #write some codes for shuffle deck
        for i in range(len(self.deck_cards)):
            if len(self.deck_cards) > 1:
                c = random.choice(self.deck_cards)
                shuffled_cards.append(c)
                self.deck_cards.remove(c)
            else:
                c = self.deck_cards.pop()
                shuffled_cards.append(c)
        self.deck_cards = shuffled_cards

    def Pop_card(self):
        return self.deck_cards.pop()

    def PrintDeck(self):
        for card in self.deck_cards:
            print (card)

        print (len(self.deck_cards))


class Pot:
    def __init__(self):
        self.pot_money = 0

class Result:
    def __init__(self, result_name, score, high_rank, high_suit, hands, kicker = None):
        self.result_name = result_name
        self.score = score
        self.high_rank = high_rank
        self.high_suit = high_suit
        self.hands = hands
        self.kicker = kicker

    def __str__(self):
        result_str = self.result_name + ', (' + str(self.high_suit) +', ' + str(self.high_rank)+')'
        result_str = result_str + '\n' + '\n'
        for card in self.hands:
            result_str = result_str + str(card) + '\n'
        return result_str


class PokerHelper:
    ROYAL_STRAIGHT_FLUSH = ['Royal-Straight-Flush!!!', 10000]
    BACK_STRAIGHT_FLUSH = ['Back-Straight-Flush', 5000]
    STRAIGHT_FLUSH = ['Straight-Flush', 3000]
    FOUR_CARDS = ['Four-Cards', 2000]
    FULL_HOUSE = ['Full-House', 1000]
    FLUSH = ['Flush', 800]

    MOUNTAIN = ['Mountain', 500]
    BACK_STRAIGHT = ['Back-Straight', 450]
    STRAIGHT = ['Straight', 400]

    TRIPLE = ['Triple', 300]
    TWO_PAIR = ['Two-Pair', 200]
    SINGLE_PAIR = ['Single-Pair', 100]

    HIGH_CARD = ['High-Card', 10]

    def __init__(self):
        pass

    # This is for python 3.0 porting
    @staticmethod
    def cmp_to_key(mycmp):
        # 'Convert a cmp= function into a key= function'
        class K:
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K

    @staticmethod
    def CompareTwoPlayerHands(p1, p2):
        r1 = p1.round_result
        r2 = p2.round_result

        if r1.score > r2.score:
            return 1
        elif r1.score == r2.score:
            print ("\n-------- Compare Two Players Cards ------------")
            print (p1.name)
            for card in r1.hands:
                print (card)
            print ('\n')
            print (p2.name)
            for card in r2.hands:
                print (card)

            if (r1.result_name == PokerHelper.ROYAL_STRAIGHT_FLUSH[0]) or (r1.result_name == PokerHelper.BACK_STRAIGHT_FLUSH[0]):
                return PokerHelper.CompareSuit(r1.high_suit, r2.high_suit)
            elif r1.result_name == PokerHelper.STRAIGHT_FLUSH[0]:
                return PokerHelper.CompareRankSuit(r1, r2)
            elif r1.result_name == PokerHelper.FOUR_CARDS[0]:
                return PokerHelper.CompareRankKicker(r1, r2)
            elif r1.result_name == PokerHelper.FULL_HOUSE[0]: # Special Function
                return PokerHelper.CompareFullHouseHands(r1.hands, r2.hands)
            elif r1.result_name == PokerHelper.FLUSH[0]:
                return PokerHelper.CompareRankSuit(r1, r2)
            elif (r1.result_name == PokerHelper.MOUNTAIN[0]) or (r1.result_name == PokerHelper.BACK_STRAIGHT[0]):
                return 0
            elif r1.result_name == PokerHelper.STRAIGHT[0]:
                return PokerHelper.CompareRankSuit(r1, r2)
            elif (r1.result_name == PokerHelper.TRIPLE[0]) or (r1.result_name == PokerHelper.SINGLE_PAIR[0]) or (r1.result_name == PokerHelper.HIGH_CARD[0]):
                print ('TRIPLE, SINGLE, HIGH')
                return PokerHelper.CompareRankKicker(r1, r2)
            elif r1.result_name == PokerHelper.TWO_PAIR[0]: # Special Function
                print ('TWO PAIR')
                return PokerHelper.CompareTwoPair(r1, r2)
            else:
                print ('Something Wrong')

        else:
            print ('score less than')
            return -1

    @staticmethod
    def CompareRank(r1, r2):
        if r1 == 0:
            r1 = 100

        if r2 == 0:
            r2 = 100

        if r1 > r2:
            return 1
        elif r1 == r2:
            return 0
        else:
            return -1

    @staticmethod
    def CompareRankSuit(r1, r2):
        r1_rank = r1.high_rank
        r2_rank = r2.high_rank

        r1_suit = r1.high_suit
        r2_suit = r2.high_suit

        if r1_rank == 0:
            r1_rank = 100

        if r2_rank == 0:
            r2_rank = 100

        if r1_rank > r2_rank:
            return 1
        elif r1_rank == r2_rank:
            if r1_suit < r2_suit:
                return 1
            elif r1_suit == r2_suit:
                return 0
            else:
                return -1
        else:
            return -1

    @staticmethod
    def CompareSuit(s1, s2):
        if s1 < s2:
            return 1
        elif s1 == s2:
            return 0
        else:
            return -1

    @staticmethod
    def CompareRankKicker(r1, r2):
        r1_rank = r1.high_rank
        r2_rank = r2.high_rank

        r1_kicker = sorted(r1.kicker, key = lambda x: x.rank)
        r2_kicker = sorted(r2.kicker, key = lambda x: x.rank)

        if r1_rank == 0:
            r1_rank = 100

        if r2_rank == 0:
            r2_rank = 100

        kicker_same = True
        if r1_rank > r2_rank:
            print ('r1_rank (' +str(r1_rank)+ ') > r2_rank (' + str(r2_rank) + ')')
            return 1
        elif r1_rank == r2_rank:
            if len(r1_kicker) != len(r2_kicker):
                print ('Abnormal')
                for card in r1_kicker:
                    print (card)
                for card in r2_kicker:
                    print (card)

                return -2 # Abnormal Case!

            for i in range(len(r1_kicker)-1, -1, -1):
                if r1_kicker[i].rank > r2_kicker[i].rank:
                    kicker_same = False
                    print ('kicker ' + str(i+1) + 'th r1 > r2')
                    return 1
                elif r1_kicker[i].rank == r2_kicker[i].rank:
                    continue
                else:
                    kicker_same = False
                    print ('kicker ' + str(i + 1) + 'th r1 < r2')
                    return -1
            if kicker_same:
                print ('all kickers are same')
                return 0
        else:
            print ('r1_rank (' + str(r1_rank) + ') < r2_rank (' + str(r2_rank) + ')')
            return -1

    @staticmethod
    def CompareFullHouseHands(h1, h2):
        h1_sorted = sorted(h1, key = lambda  x: x.rank)
        h2_sorted = sorted(h2, key = lambda  x: x.rank)

        h1_triple_rank = 0
        h1_pair_rank = 0

        h2_triple_rank = 0
        h2_pair_rank = 0

        first_card_cnt = 0
        second_card_cnt = 0
        bIsFirstCard = True

        # h1
        for i in range(len(h1_sorted)):
            if i == 0:
                h1_triple_rank = h1_sorted[i].rank
            if h1_triple_rank != h1_sorted[i].rank:
                h1_pair_rank = h1_sorted[i].rank
                bIsFirstCard = False

            if bIsFirstCard:
                first_card_cnt += 1
            else:
                second_card_cnt += 1

        if first_card_cnt < 3: #Swap
            tmp_pair_rank = h1_triple_rank
            h1_triple_rank = h1_pair_rank
            h1_pair_rank = tmp_pair_rank

        # h2
        for i in range(len(h2_sorted)):
            if i == 0:
                h2_triple_rank = h2_sorted[i].rank
            if h2_triple_rank != h2_sorted[i].rank:
                h2_pair_rank = h2_sorted[i].rank
                bIsFirstCard = False

            if bIsFirstCard:
                first_card_cnt += 1
            else:
                second_card_cnt += 1

        if first_card_cnt < 3:  # Swap
            tmp_pair_rank = h2_triple_rank
            h2_triple_rank = h2_pair_rank
            h2_pair_rank = tmp_pair_rank

        # Let's compare
        if h1_triple_rank == 0:
            h1_triple_rank = 100

        if h2_triple_rank == 0:
            h2_triple_rank = 100

        if h1_pair_rank == 0:
            h1_pair_rank = 100

        if h2_pair_rank == 0:
            h2_pair_rank = 100

        if h1_triple_rank > h2_triple_rank:
            return 1
        elif h1_triple_rank == h2_triple_rank:
            if h1_pair_rank > h2_pair_rank:
                return 1
            elif h1_pair_rank == h2_pair_rank:
                return 0
            else:
                return -1
        else:
            return -1

    @staticmethod
    def CompareTwoPair(r1, r2):
        h1_sorted = sorted(r1.hands, key=lambda x: x.rank)
        h2_sorted = sorted(r2.hands, key=lambda x: x.rank)

        r1_kicker = sorted(r1.kicker, key=lambda x: x.rank)
        r2_kicker = sorted(r2.kicker, key=lambda x: x.rank)

        h1_first_pair_rank = 0
        h1_second_pair_rank = 0

        h2_first_pair_rank = 0
        h2_second_pair_rank = 0

        bIsFirstCard = True

        # h1
        for i in range(len(h1_sorted)):
            if i == 0:
                h1_first_pair_rank = h1_sorted[i].rank
            if h1_first_pair_rank != h1_sorted[i].rank:
                h1_second_pair_rank = h1_sorted[i].rank
        # h2
        for i in range(len(h2_sorted)):
            if i == 0:
                h2_first_pair_rank = h2_sorted[i].rank
            if h2_first_pair_rank != h2_sorted[i].rank:
                h2_second_pair_rank = h2_sorted[i].rank

        # Let's compare
        if h1_first_pair_rank == 0:
            h1_first_pair_rank = 100

        if h1_second_pair_rank == 0:
            h1_second_pair_rank = 100

        if h1_first_pair_rank < h1_second_pair_rank:
            tmp_pair_rank = h1_second_pair_rank
            h1_second_pair_rank = h1_first_pair_rank
            h1_first_pair_rank = tmp_pair_rank

        if h2_first_pair_rank == 0:
            h2_first_pair_rank = 100

        if h2_second_pair_rank == 0:
            h2_second_pair_rank = 100

        if h2_first_pair_rank < h2_second_pair_rank:
            tmp_pair_rank = h2_second_pair_rank
            h2_second_pair_rank = h2_first_pair_rank
            h2_first_pair_rank = tmp_pair_rank

        print ('h1_first_rank: ' + str(h1_first_pair_rank) +', h1_second_pair_rank: ' + str(h1_second_pair_rank))
        print ('h2_first_rank: ' + str(h2_first_pair_rank) + ', h2_second_pair_rank: ' + str(h2_second_pair_rank))

        if h1_first_pair_rank > h2_first_pair_rank:
            print ('h1_first_pair_rank (' + str(h1_first_pair_rank) + ') > h2_first_pair_rank (' + str(h2_first_pair_rank) + ')')
            return 1
        elif h1_first_pair_rank == h2_first_pair_rank:
            if h1_second_pair_rank > h2_second_pair_rank:
                print ('h1_second_pair_rank (' + str(h1_second_pair_rank) + ') > h2_second_pair_rank (' + str(h2_second_pair_rank) + ')')
                return 1
            elif h1_second_pair_rank == h2_second_pair_rank:
                if len(r1.kicker) != len(r2.kicker):
                    print ('Something Wrong')
                    return -2
                else:
                    if r1_kicker[0].rank > r2_kicker[0].rank:
                        print ('r1 kicker rank ('+ str(r1_kicker[0].rank)+') > r2 kicker rank (' + str(r2_kicker[0].rank)+ ')')
                        return 1
                    elif r1_kicker[0].rank == r2_kicker[0].rank:
                        return 0
                    else:
                        return -1
            else:
                print ('h1_second_pair_rank (' + str(h1_second_pair_rank) + ') < h2_second_pair_rank (' + str(h2_second_pair_rank) + ')')
                return -1
        else:
            return -1

    @staticmethod
    def GetBestChoise(cards):
        straight_list = []
        flush_list = []
        straight_flush_list = []
        multi_bin_list = {}
        result = None

        straight_list = PokerHelper.GetStraightCards(cards)
        flush_list = PokerHelper.GetFlushCards(cards)
        multi_bin_list = PokerHelper.GetMultiBins(cards)

        if straight_list is not None:
            straight_flush_list = PokerHelper.GetFlushCards(straight_list)
            if straight_flush_list is not None:
                # Check "Straight-Flush"
                sorted_result = sorted(straight_flush_list, key = lambda x: x.suit)

                # Royal-Straight-Flush!!!
                if sorted_result[len(sorted_result)-1].rank == 12 \
                    and sorted_result[0].rank == 0:

                    #Becareful Here
                    if len(sorted_result) > 5:
                        for card in sorted_result:
                            if card.rank <= 8:
                                sorted_result.pop()

                    result = Result(PokerHelper.ROYAL_STRAIGHT_FLUSH[0], \
                                    PokerHelper.ROYAL_STRAIGHT_FLUSH[1], \
                                    0, \
                                    sorted_result[0].suit, \
                                    sorted_result)
                    return result

                # Back-Straight-Flush!!!
                elif sorted_result[0].rank == 0:
                    # Becareful Here
                    if len(sorted_result) > 5:
                        for card in sorted_result:
                            if card.rank >= 5:
                                sorted_result.pop()

                    result = Result(PokerHelper.BACK_STRAIGHT_FLUSH[0], \
                                    PokerHelper.BACK_STRAIGHT_FLUSH[1], \
                                    0, \
                                    sorted_result[0].suit, \
                                    sorted_result)

                    return result

                # Straight-Flush
                else:
                    # Becareful Here
                    new_list = []
                    if len(sorted_result) > 5:
                        for i in range(len(sorted_result)-1, len(sorted_result) - 5, -1):
                            new_list.append(sorted_result[i])
                    else:
                        new_list = sorted_result[:]

                    result = Result(PokerHelper.STRAIGHT_FLUSH[0], \
                                    PokerHelper.STRAIGHT_FLUSH[1], \
                                    new_list[len(new_list)-1].rank, \
                                    new_list[0].suit, \
                                    new_list)

                    return result

        # Check Four-Cards
        for item in multi_bin_list.values():
            if len(item) >= 4:
                result = Result(PokerHelper.FOUR_CARDS[0], \
                                PokerHelper.FOUR_CARDS[1], \
                                item[0].rank, \
                                item[0].suit, \
                                item, \
                                PokerHelper.GetKicker(item, cards, 1))
                return result


        # Check Full-House
        triple_list = []
        pair_list = []

        for item in multi_bin_list.values():
            if len(item) >= 3:
                for card in item:
                    triple_list.append(card)
            elif len(item) >= 2:
                for card in item:
                    pair_list.append(card)

        pair_list = sorted(pair_list, key=lambda x: x.rank)

        if len(triple_list) > 0 and len(pair_list) > 0:
            safe_triple_list = []

            if triple_list[0].rank == 0:
                safe_triple_list = triple_list[0:3:1]
            else:
                safe_triple_list = triple_list[len(triple_list) - 3: len(triple_list):1]

            new_list = safe_triple_list + pair_list[len(pair_list) - 2: len(pair_list):1]

            result = Result(PokerHelper.FULL_HOUSE[0], \
                            PokerHelper.FULL_HOUSE[1], \
                            safe_triple_list[0].rank, \
                            safe_triple_list[0].suit, \
                            new_list)

            return result

        if flush_list is not None:
            # Check normal Flush
            sorted_result = sorted(flush_list, key = lambda x:x.rank)

            # Becareful Here
            new_list = []
            if len(sorted_result) > 5:
                for i in range(len(sorted_result) - 1, len(sorted_result) - 5, -1):
                    new_list.append(sorted_result[i])
            else:
                new_list = sorted_result[:]

            result = Result(PokerHelper.FLUSH[0], \
                            PokerHelper.FLUSH[1], \
                            new_list[len(new_list) - 1].rank, \
                            new_list[0].suit, \
                            new_list)
            return result

        if straight_list is not None:
            # Check normal Straight
            sorted_result = sorted(straight_list, key=lambda x: x.rank)
            distinct_straight_list = PokerHelper.GetDistinctStraightCards(sorted_result)
            exact5_straight_list = PokerHelper.GetExact5_StraightCards(distinct_straight_list)

            # Moutain
            if sorted_result[len(sorted_result) - 1].rank == 12 \
                    and sorted_result[0].rank == 0:
                result = Result(PokerHelper.MOUNTAIN[0], \
                                PokerHelper.MOUNTAIN[1], \
                                exact5_straight_list[0].rank, \
                                exact5_straight_list[0].suit, \
                                exact5_straight_list) # return only distinct straight hands
                return result

            # Back-Straight!!!
            elif sorted_result[0].rank == 0:
                result = Result(PokerHelper.BACK_STRAIGHT[0], \
                                PokerHelper.BACK_STRAIGHT[1], \
                                exact5_straight_list[0].rank, \
                                exact5_straight_list[0].suit, \
                                exact5_straight_list) # return only distinct straight hands
                return result
            # normal Straight
            else:
                result = Result(PokerHelper.STRAIGHT[0], \
                                PokerHelper.STRAIGHT[1], \
                                exact5_straight_list[len(exact5_straight_list) - 1].rank, \
                                exact5_straight_list[len(exact5_straight_list) - 1].suit, \
                                exact5_straight_list) # return only distinct straight hands
                return result


        #Triple & Two-Pair & One-Pair
        triple_list = []
        pair_list = []

        for item in multi_bin_list.values():
            if len(item) >= 3:
                for card in item:
                    triple_list.append(card)
            elif len(item) >= 2:
                for card in item:
                    pair_list.append(card)

        pair_list = sorted(pair_list, key = lambda x:x.rank)

        if len(triple_list) > 0:
            if triple_list[0].rank == 0:
                safe_triple_list = triple_list[0:3:1]
            else:
                safe_triple_list = triple_list[len(triple_list)-3: len(triple_list):1]

            result = Result(PokerHelper.TRIPLE[0], \
                            PokerHelper.TRIPLE[1], \
                            safe_triple_list[0].rank, \
                            safe_triple_list[0].suit, \
                            safe_triple_list, \
                            PokerHelper.GetKicker(safe_triple_list, cards, 2))
            return result
        elif len(pair_list) >= 4:

            high_pair_list = []
            if pair_list[0].rank == 0:
                high_pair_list = pair_list[0:2:1]
            else:
                high_pair_list = pair_list[len(pair_list)-2: len(pair_list):1]

            safe_pair_list = PokerHelper.GetDistinctTwoPairs(pair_list)
            result = Result(PokerHelper.TWO_PAIR[0], \
                            PokerHelper.TWO_PAIR[1], \
                            high_pair_list[len(high_pair_list)-1].rank, \
                            high_pair_list[len(high_pair_list)-1].suit, \
                            safe_pair_list, \
                            PokerHelper.GetKicker(safe_pair_list, cards, 1))
            return result
        elif len(pair_list) == 2:

            result = Result(PokerHelper.SINGLE_PAIR[0], \
                            PokerHelper.SINGLE_PAIR[1], \
                            pair_list[len(pair_list)-1].rank, \
                            pair_list[len(pair_list)-1].suit, \
                            pair_list, \
                            PokerHelper.GetKicker(pair_list, cards, 3))
            return result

        #Check High-Card

        sorted_result = sorted(cards, key = lambda x:x.rank)

        suit_high = 0
        rank_high = 0

        if sorted_result[0].rank == 0:
            suit_high = sorted_result[0].suit
            rank_high = 0
        else:
            suit_high = sorted_result[len(sorted_result) -1].suit
            rank_high = sorted_result[len(sorted_result) -1].rank

        high_card = [Card(suit_high, rank_high)]

        result = Result(PokerHelper.HIGH_CARD[0], \
                        PokerHelper.HIGH_CARD[1], \
                        suit_high, \
                        rank_high, \
                        high_card, \
                        PokerHelper.GetKicker(high_card, cards, 4))

        return result

    @staticmethod
    def GetKicker(hands, cards, kicker_cnt):
        kicker = []
        sorted_cards = sorted(cards, key = lambda  x: x.rank)

        # Ace has the highest priority
        if sorted_cards[0].rank == 0:
            for hand_card in hands:
                if sorted_cards[0].rank != hand_card.rank \
                        and sorted_cards[0].suit != hand_card.suit:
                    if len(kicker) < kicker_cnt:
                        kicker.append(sorted_cards[0])

        for i in range(len(sorted_cards)-1, -1, -1):
            if len(kicker) < kicker_cnt:
                # add a card not belonged in the hands as a kicker
                bContained = False
                for hand_card in hands:
                    if sorted_cards[i].rank == hand_card.rank \
                        and sorted_cards[i].suit == hand_card.suit:
                        bContained = True

                if bContained == False:
                    kicker.append(sorted_cards[i])

        return kicker

    @staticmethod
    def GetDistinctStraightCards(newlist):
        sorted_result = sorted(newlist, key=lambda x: x.rank)

        result_list = []

        for card in sorted_result:
            dup_cnt = 0

            if len(result_list) == 0:
                result_list.append(card)
            else:
                for selected_card in result_list:
                    if card.rank == selected_card.rank:
                        dup_cnt += 1

                if dup_cnt == 0:
                    result_list.append(card)
        return result_list


    @staticmethod
    def GetDistinctTwoPairs(hands):
        sorted_result = sorted(hands, key=lambda x: x.rank)
        result_list = []

        for card in sorted_result:
            if card.rank == 0:
                result_list.append(card)

        for i in range(len(sorted_result)-1, -1, -1):
            if(len(result_list) < 4):
                result_list.append(sorted_result[i])

        return result_list

    @staticmethod
    def GetStraightCards(newlist):
        sorted_list = sorted(newlist, key=lambda x: x.rank)

        # Check Straight
        bStraight = False
        straight_list = []
        for i in range(len(sorted_list)):
            current_suit_no = sorted_list[i].rank
            straight_list = []
            straight_list.append(sorted_list[i])

            for j in range(i+1, len(sorted_list)):
                if sorted_list[j].rank == current_suit_no +1:
                    current_suit_no += 1
                    straight_list.append(sorted_list[j])
                # add duplicate cards
                elif sorted_list[j].rank == current_suit_no:
                    straight_list.append(sorted_list[j])
                # Very Important Here
                if sorted_list[j].rank == 12 and sorted_list[j-1].rank == 11:
                    # add aces for Back Straight
                    idx = 0
                    while 1:
                        if sorted_list[idx].rank == 0:
                            if sorted_list[idx] not in straight_list:
                                straight_list.append(sorted_list[idx])
                            idx += 1
                        else:
                            break

            # Get the distint list
            distinct_straight_cnt = 0
            dup_cnt = 0
            for i in range(len(straight_list)):
                distinct_straight_cnt += 1
                suit_no = straight_list[i].rank
                for j in range(i+1, len(straight_list)):
                    if suit_no == straight_list[j].rank:
                        dup_cnt += 1
                    else:
                        break

            if len(straight_list) - dup_cnt >= 5:
                bStraight = True
                PokerHelper.PrintCards(straight_list)
                return straight_list

        return None

    @staticmethod
    def GetExact5_StraightCards(newlist):
        sorted_list = sorted(newlist, key=lambda x: x.rank)
        result_list = []

        # check mountain
        if sorted_list[0].rank == 0 and sorted_list[len(sorted_list) -1].rank == 12:
            result_list.append(sorted_list[0])

            for i in range(len(sorted_list) -4, len(sorted_list), 1):
                result_list.append(sorted_list[i])

            return result_list

        else:
            for card in sorted_list:
                bContained = False

                for selected_card in result_list:
                    if card.rank == selected_card.rank:
                        bContained = True

                if bContained == False and len(result_list) < 5:
                    result_list.append(card)

            return result_list

    @staticmethod
    def GetFlushCards(newlist):
        sorted_list = sorted(newlist, key=lambda x: x.suit)
        #PokerHelper.PrintCards(sorted_list)  # print sorted list

        spade_cnt= 0
        diamond_cnt = 0
        heart_cnt = 0
        club_cnt = 0

        for card in sorted_list:
            current_rank = card.suit
            if current_rank == 0:
                spade_cnt += 1
            elif current_rank == 1:
                diamond_cnt += 1
            elif current_rank == 2:
                heart_cnt += 1
            elif current_rank == 3:
                club_cnt += 1

        collect_rank = 0
        bFlush = False

        # Flust - Spades
        if spade_cnt >= 5:
            collect_rank = 0
            bFlush = True
        elif diamond_cnt >= 5:
            collect_rank = 1
            bFlush = True
        elif heart_cnt >= 5:
            collect_rank = 2
            bFlush = True
        elif club_cnt >= 5:
            collect_rank = 3
            bFlush = True

        flush_list = []
        if bFlush:
            for card in sorted_list:
                if card.suit == collect_rank:
                    flush_list.append(card)

            PokerHelper.PrintCards(flush_list)

            return flush_list
        else:
            return None

    @staticmethod
    def GetMultiBins(newlist):
        sorted_list = sorted(newlist, key = lambda x : x.rank)

        multi_bin_array = {x: [] for x in range(13)}

        # put the card into the right bin
        for card in sorted_list:
            suit_no = card.rank
            list(multi_bin_array.values())[suit_no].append(card)

        return multi_bin_array

    @staticmethod
    def PrintCards(card_list):
        for card in card_list:
            print (card)

