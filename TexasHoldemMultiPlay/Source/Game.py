import pygame
import random
import time
import math
from CardCommon import PokerHelper

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def GetRank(self):
        return self.rank

    def GetSuit(self):
        return self.suit

    def __str__(self):
        return '(suit:' + str(self.suit) + ', rank: ' + str(self.rank) + ')'

class Pot():
    def __init__(self):
        self.pot_money = 0

    def withdraw_money(self):
        amount = self.pot_money
        self.pot_money = 0
        return amount

    def add_money(self, amount):
        self.pot_money += amount

class Deck():
    def __init__(self):
        self.deck_cards = []
        self.init_deck()
    
    def init_deck(self):
        self.deck_cards = []

        # write some codes for initialize the deck
        for i in range(0, 4):
            for j in range(0, 13):
                self.deck_cards.append(Card(i, j))

    def shuffle_deck(self):
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

    def pop_deck(self):
        return self.deck_cards.pop(0)

class Player():
    def __init__(self, name, id, money = 500):
        self.name = name
        self.id = id
        self.money = money
        self.IsDead = False

        self.IsDealer = False
        self.IsSmallBlind = False
        self.IsBigBlind = False
        self.IsAllIn = False
        self.IsFold = False
        self.IsChecked = False

        self.curr_bet_type = ""
        self.curr_bet_amount = 0
        self.card_list = []
        self.curr_raise_number = 0

        self.round_result = None

    def choice_best_cards(self, community_cards):
        new_list = self.card_list + community_cards
        result = PokerHelper.GetBestChoise(new_list)
        self.round_result = result
    
    def withdraw_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            
            if self.money == amount:
                self.IsAllIn = True
    
    def add_money(self, amount):
        self.money += amount

    def update_curr_bet(self, bet_type, bet_money):
        self.curr_bet_type = bet_type
        self.curr_bet_amount = bet_money
        #print("curr_bet_type:{0}, curr_bet_amount:{1}".format(self.curr_bet_type, self.curr_bet_amount))

        if self.curr_bet_type == "Raise":
            self.curr_raise_number += 1
    
    def fold(self):
        self.IsFold = True
        self.curr_bet_type = "Fold"

    def check(self):
        self.IsChecked = True
        self.curr_bet_type = "Check"

    def init_round_player(self):
        if not self.IsDead:
            self.card_list = []
            self.IsFold = False
            self.IsAllIn = False
            self.curr_bet = ""
            self.IsDealer = False
            self.IsSmallBlind = False
            self.IsBigBlind = False
            self.IsChecked = False

            self.curr_raise_number = 0
            self.round_result = None
    
    def add_card(self, card):
        if len(self.card_list) < 2:
            self.card_list.append(card)
            return True
        else:
            return False



class Game():
    MAX_PLAYER_CNT = 4

    def __init__(self):
        self.players = []
        self.community_cards = []
        
        self.pot = Pot()
        self.game_state = "BeforeGame"
        self.deck = Deck()

        self.dealer_idx = -1
        self.bet_order_list = []
        self.bet_list = []
        self.curr_fold_player_list = []
        self.curr_bet_idx = 0
        self.IsBetFinished = False

        # betting
        self.init_bet_amount = 1
        self.raise_ratio = 2
        self.raise_allow_number = 3
        self.call_amout = 0
        self.is_check_allowable = False
        self.is_call_allowable = False
        self.raise_amount = 0

        #showdown
        self.winner = None

        # for change the state
        self.start_game_request_pset = set()
        self.init_round_request_pset = set()
        self.preflop_request_pset = set()
        self.flop_request_pset = set()
        self.turn_request_pset = set()
        self.river_request_pset = set()
        self.showdown_request_pset = set()
        self.quitround_request_pset = set()

        self.InitRoundCnt = 0
        self.PreFlopCnt = 0
        self.FlopCnt = 0
        self.TurnCnt = 0
        self.RiverCnt = 0
        self.ShowDownCnt = 0
        self.QuitRoundCnt = 0

    def reply_to_client(self):
        # only small information via network
        game_dict = {}

        # game state
        game_dict["game_state"] = self.game_state

        # players information
        players_info_dict = self.make_player_infomation()
        game_dict["players_info"] = players_info_dict

        # player cards
        player_cards = {}
        for idx in self.bet_order_list:
            player_cards[idx] = self.players[idx].card_list

        game_dict["players_cards"] = player_cards

        # community cards
        game_dict["community_cards"] = self.community_cards

        # pot_money
        game_dict["pot_money"] = self.pot.pot_money

        # current_turn_pid
        game_dict["curr_turn_pid"] = self.curr_bet_idx

        # IsBetFinished
        game_dict["IsBetFinished"] = self.IsBetFinished

        # Betting Info
        game_dict["init_bet_amount"] = self.init_bet_amount
        game_dict["raise_ratio"] = self.raise_ratio
        game_dict["raise_allow_number"] = self.raise_allow_number

        game_dict["call_amout"] = self.call_amout
        game_dict["is_check_allowable"] = self.is_check_allowable
        game_dict["is_call_allowable"] = self.is_call_allowable
        game_dict["raise_amount"] = self.raise_amount

        game_dict["winner"] = self.winner

        return game_dict

    def make_player_infomation(self):
        players_info_dict = {}

        if len(self.players) == Game.MAX_PLAYER_CNT:
            for idx in range(Game.MAX_PLAYER_CNT):
                # dictionary of dictionary
                players_info_dict[idx] = {}
                player = self.players[idx]
                players_info_dict[idx]["name"] = player.name
                players_info_dict[idx]["money"] = player.money

                if player.IsFold:
                    players_info_dict[idx]["curr_bet_type"] = "Fold"
                else:
                    players_info_dict[idx]["curr_bet_type"] = player.curr_bet_type
                players_info_dict[idx]["curr_bet_amount"] = player.curr_bet_amount
                players_info_dict[idx]["curr_raise_number"] = player.curr_raise_number

                players_info_dict[idx]["IsFold"] = player.IsFold
                players_info_dict[idx]["IsDead"] = player.IsDead
                players_info_dict[idx]["IsAllIn"] = player.IsAllIn
                players_info_dict[idx]["IsDealer"] = player.IsDealer
                players_info_dict[idx]["IsSmallBlind"] = player.IsSmallBlind
                players_info_dict[idx]["IsBigBlind"] = player.IsBigBlind
                players_info_dict[idx]["IsChecked"] = player.IsChecked

                players_info_dict[idx]["card_list"] = player.card_list
                
        return players_info_dict

    def connect_player(self, player_idx, player_name):
        player = Player(str(player_name), player_idx)
        self.players.append(player)

        if len(self.players) == Game.MAX_PLAYER_CNT:
            print("Start Game")
            self.game_state = "StartGame"
            self.start_game()

    def disconnect_player(self, player_idx):
        self.players.pop(player_idx)

    def start_game(self, player_idx=-1):

        if player_idx == -1:
            pass
        elif self.game_state == "StartGame":
            self.start_game_request_pset.add(player_idx)

            # When the request player set is filled with Maximum number of Players
            # then go to the next step
            if len(self.start_game_request_pset) == Game.MAX_PLAYER_CNT:
                # go to the next step
                print("Go to Init Round")
                
                # to prevent the misorder in communication
                time.sleep(1)

                self.game_state = "InitRound"
                self.init_round()

    
    def init_round(self, player_idx= -1):
        #self.game_state = "InitRound"

        if player_idx == -1 and self.InitRoundCnt == 0:
            for player in self.players:
                player.init_round_player()
        
            self.community_cards = []
            self.bet_order_list = []
            self.bet_list = []
            self.curr_fold_player_list = []
            self.last_raise_idx = -1

            self.deck.init_deck()
            self.deck.shuffle_deck()

            self.update_dealer_idx()
            self.calculate_bet_order()
            self.init_bet_list()
            self.designate_roles()
            self.IsBetFinished = False

            self.winner = None

            self.InitRoundCnt += 1

        elif self.game_state == "InitRound" and player_idx != -1:
            self.init_round_request_pset.add(player_idx)
            
            if len(self.init_round_request_pset) == Game.MAX_PLAYER_CNT:
                # go to the next step
                print("Go to Pre Flop")

                # to prevent the misorder in communication
                time.sleep(1)

                self.game_state = "PreFlop"
                self.init_turn()
                self.preflop()

    def make_undead_idx_list(self):
        tmp_idx_list = []
        for idx in range(len(self.players)):
            if not self.players[idx].IsDead:
                tmp_idx_list.append(idx)
        
        return tmp_idx_list

    def init_bet_list(self):
        bet_cnt = len(self.bet_order_list)

        self.bet_list = []

        for i in range(bet_cnt):
            self.bet_list.append('')
                    

    def update_dealer_idx(self):
        if self.game_state == "InitRound":

            if len(self.players)-1 <= self.dealer_idx:
                self.dealer_idx = 0

            else:
                self.dealer_idx += 1
            
            # next dealer might not be alive, then increase index
            while True:
                if self.players[self.dealer_idx].IsDead:
                    self.dealer_idx += 1
                else:
                    break

    def calculate_bet_order(self):
        small_blind_idx = 0
        
        if self.game_state == "InitRound":

            # make idx list who is not dead
            tmp_idx_list = self.make_undead_idx_list()

            #print(tmp_idx_list)
            
            if tmp_idx_list.index(self.dealer_idx) == len(tmp_idx_list) - 1:
                small_blind_idx = 0
            else:
                sb_idx  = tmp_idx_list.index(self.dealer_idx) + 1
                #print(sb_idx)
                small_blind_idx = tmp_idx_list[sb_idx]

            if small_blind_idx == 0:
                self.bet_order_list = tmp_idx_list
            else:
                self.bet_order_list = tmp_idx_list[sb_idx:] + tmp_idx_list[:sb_idx]
        
    def designate_roles(self):
        # to designate roles: dealer, sb, bb
        if self.game_state == "InitRound":
            dealer = self.players[self.dealer_idx]
            small_blind_idx = self.bet_order_list[0]
            small_blind = self.players[small_blind_idx]
            big_blind_idx = self.bet_order_list[1]
            big_blind = self.players[big_blind_idx]

            dealer.IsDealer = True
            small_blind.IsSmallBlind = True
            big_blind.IsBigBlind = True
            self.curr_bet_idx = self.bet_order_list[0]


    def preflop(self, player_idx= -1):
        # to go to next stage
        if player_idx == -1 and self.PreFlopCnt ==0:
            for i in range(2):
                for idx in self.bet_order_list:
                    card = self.deck.pop_deck()
                    if self.players[idx].add_card(card):
                        print('{0}, add card ({1})'.format(self.players[idx].name, card))

        elif self.game_state == "PreFlop" and player_idx != -1:
            self.preflop_request_pset.add(player_idx)

            # When the request player set is filled with Maximum number of Players
            # then go to the next step
            if len(self.preflop_request_pset) == Game.MAX_PLAYER_CNT:
                # go to the next step
                print("Go to Flop")

                # to prevent the misorder in communication
                time.sleep(1)

                self.game_state = "Flop"
                self.init_turn()
                self.flop()

    
    def flop(self, player_idx= -1):
        # to go to next stage
        if player_idx == -1 and self.FlopCnt ==0:
            # add three community cards
            if len(self.community_cards) == 0:
                for i in range(3):
                    self.community_cards.append(self.deck.pop_deck())
        elif self.game_state == "Flop" and player_idx != -1:
            self.flop_request_pset.add(player_idx)

            # When the request player set is filled with Maximum number of Players
            # then go to the next step
            if len(self.flop_request_pset) == Game.MAX_PLAYER_CNT:
                # go to the next step
                print("Go to Turn")

                # to prevent the misorder in communication
                time.sleep(1)

                self.game_state = "Turn"
                self.init_turn()
                self.turn()
                
    def turn(self, player_idx= -1):
        # to go to next stage
        if player_idx == -1 and self.TurnCnt == 0:
            # add three community cards
            if len(self.community_cards) == 3:
                self.community_cards.append(self.deck.pop_deck())
        elif self.game_state == "Turn" and player_idx != -1:
            self.turn_request_pset.add(player_idx)

            # When the request player set is filled with Maximum number of Players
            # then go to the next step
            if len(self.turn_request_pset) == Game.MAX_PLAYER_CNT:
                # go to the next step
                print("Go to River")

                # to prevent the misorder in communication
                time.sleep(1)

                self.game_state = "River"
                self.init_turn()
                self.river()

    def river(self, player_idx= -1):
        # to go to next stage
        if player_idx == -1 and self.RiverCnt ==0:
            # add three community cards
            if len(self.community_cards) == 4:
                self.community_cards.append(self.deck.pop_deck())
        elif self.game_state == "River" and player_idx != -1:
            self.river_request_pset.add(player_idx)

            # When the request player set is filled with Maximum number of Players
            # then go to the next step
            if len(self.river_request_pset) == Game.MAX_PLAYER_CNT:
                # go to the next step
                print("Go to Showdown")

                # to prevent the misorder in communication
                time.sleep(1)

                self.game_state = "Showdown"
                self.showdown()

    def showdown(self, player_idx = -1):
        # 1. calc each players' best hands
        # 2. choose winner
        # 3. add money to winner from the pot
        # 4. vote from players to proceed next round

        # to go to next stage
        if player_idx == -1 and self.ShowDownCnt ==0:
            # 1. calc each players' best hands
            for player in self.players:
                player.choice_best_cards(self.community_cards)
                PokerHelper.PrintCards(player.round_result.hands)

            # 2. choose winner
            self.winner = self.GetWinner()

            # 3. add money to winner from the pot
            self.players[self.winner.id].add_money(self.pot.pot_money)
            self.pot.withdraw_money()


        elif self.game_state == "Showdown" and player_idx != -1:
            self.showdown_request_pset.add(player_idx)

            # When the request player set is filled with Maximum number of Players
            # then go to the next step
            if len(self.showdown_request_pset) == Game.MAX_PLAYER_CNT:
                # go to the next round
                print("Go to Init Round")

                # to prevent the misorder in communication
                time.sleep(3)

                self.clear_round()
                self.game_state = "InitRound"
                self.init_round()

    def quitround(self, player_idx = -1):
        # 1. add money to winner from the pot
        # 2. vote from players to proceed next round

        # to go to next stage
        if player_idx == -1 and self.QuitRoundCnt ==0:
            print("Quit Round Entered Inside")

            # 1. choose winner
            self.winner = self.GetWinnerQuit()

            # 2. add money to winner from the pot
            self.players[self.winner.id].add_money(self.pot.pot_money)
            self.pot.withdraw_money()


        elif self.game_state == "QuitRound" and player_idx != -1:
            self.quitround_request_pset.add(player_idx)

            # When the request player set is filled with Maximum number of Players
            # then go to the next step
            if len(self.quitround_request_pset) == Game.MAX_PLAYER_CNT:
                # go to the next round
                print("Go to Init Round")

                # to prevent the misorder in communication
                time.sleep(3)

                self.clear_round()
                self.game_state = "InitRound"
                self.init_round()

    def GetWinner(self):
        # winner selected among the only unfolded players
        unfold_players = []

        for player in self.players:
            if not player.IsFold:
                unfold_players.append(player)

        sorted_player = sorted(unfold_players, key = PokerHelper.cmp_to_key(PokerHelper.CompareTwoPlayerHands), reverse = True)

        print ('--------------------- sorted players ---------------------')
        for player in sorted_player:
            print (player.name)
            print (player.round_result)

        winner = sorted_player[0]

        print (winner.round_result)

        return winner

    def GetWinnerQuit(self):
        for player in self.players:
            bFold = False
            for idx in self.curr_fold_player_list:
                if player.id == idx:
                    bFold = True
            
            if not bFold:
                return player

        
    def IsMyTurn(self, player_idx):
        # Check the player's turn
        if self.curr_bet_idx == player_idx:
            return True
        else:
            return False

    def player_fold(self, player_idx):
        if self.game_state == "PreFlop" or self.game_state == "Flop" or self.game_state == "Turn" or self.game_state == "River":
            player = self.players[player_idx]
            player.fold()

            print("{0} has fold".format(player_idx))

            self.curr_fold_player_list.append(player_idx)

            # if fold_player is equal to total player -1, then quit round and go to the next round
            if len(self.curr_fold_player_list) == Game.MAX_PLAYER_CNT - 1:
                print("Quit Round")
                self.game_state = "QuitRound"
                self.quitround()
                return

            # update curr_bet_turn
            self.update_curr_bet_turn("Fold")

    def player_check(self, player_idx):
        if self.game_state == "PreFlop" or self.game_state == "Flop" or self.game_state == "Turn" or self.game_state == "River":
            if self.is_check_allowable:
                player = self.players[player_idx]
                player.check()

                print("{0} has checked".format(player_idx))

                # update curr_bet_turn
                self.update_curr_bet_turn("Check")
            else:
                print("Invalid Check")

    def player_bet(self, player_idx, bet):
        """
            bet ( tuple ) : (bet_type, amount)
        """
        if self.game_state == "PreFlop" or self.game_state == "Flop" or self.game_state == "Turn" or self.game_state == "River":
            if self.IsMyTurn(player_idx):
                player = self.players[player_idx]
                bet_type = bet[0]
                bet_amount = bet[1]
                print("{0}, {1}".format(bet_type, bet_amount))

                if bet_type == "Call":
                    if not self.is_call_allowable:
                        print("Invalid Call")
                        return

                if bet_type == "Raise":
                    self.update_call_amount(bet_amount)
                    self.update_raise_amount( round(bet_amount * self.raise_ratio))
              
                # to prevent the misorder in communication
                time.sleep(1)
                
                player.update_curr_bet(bet_type, bet_amount)
                player.withdraw_money(bet_amount) # withdraw money right after betting
                self.pot.add_money(bet_amount)
                self.update_curr_bet_turn(bet_type)

                #print(self.curr_bet_idx)
                #print(self.bet_order_list)
                #print(self.IsBetFinished)

    def update_call_amount(self, call_amount):
        self.call_amout = call_amount

    def update_raise_amount(self, raise_amount):
        self.raise_amount = raise_amount

    def update_curr_bet(self, bet_type):
        self.bet_list[self.curr_bet_idx] = bet_type

        if bet_type == "Raise":
            self.last_raise_idx = self.curr_bet_idx

    def update_check_allowable(self):
        # Check what if current bet is different from prev 'Check'
        #curr_bet = self.bet_list[self.curr_bet_idx]
        if self.last_raise_idx == -1:
            self.is_check_allowable = True
        else:
            self.is_check_allowable = False

    def update_call_allowable(self):
        if self.last_raise_idx == -1:
            self.is_call_allowable = False
        else:
            self.is_call_allowable = True

    def is_bet_end(self):
        if self.bet_list[self.curr_bet_idx] == 'Check' or self.bet_list[self.curr_bet_idx] == 'Fold' or self.bet_list[self.curr_bet_idx] == 'Call':
            print(self.bet_list)
            print(self.curr_bet_idx)
            print(self.last_raise_idx)

            next_idx = 0

            check_fold_cnt = 0
            for bet in self.bet_list:
                if bet == "Check" or bet == "Fold":
                    check_fold_cnt += 1
            
            if check_fold_cnt == len(self.bet_list):
                return True
            
            if self.curr_bet_idx == len(self.bet_list)-1:
                next_idx = 0
            else:
                next_idx = self.curr_bet_idx +1

            # to skip the folds
            next_idx = self.find_next_idx_skip_fold(self.bet_order_list, self.curr_fold_player_list, next_idx)
            
            if self.last_raise_idx == next_idx:
                return True
            else:
                return False

    def update_curr_bet_turn(self, bet_type):
        self.update_curr_bet(bet_type)
        self.update_check_allowable()
        self.update_call_allowable()
        
        if self.is_bet_end():
            self.IsBetFinished = True
            self.update_turn()
        else:
            # update self.curr_bet_idex
            curr_idx_in_bet = self.bet_order_list.index(self.curr_bet_idx)
            curr_idx_in_bet += 1

            if curr_idx_in_bet >= len(self.bet_order_list):
                curr_idx_in_bet = 0

            self.curr_bet_idx = self.bet_order_list[curr_idx_in_bet]
            
            # to skip the folds
            self.curr_bet_idx = self.find_next_idx_skip_fold(self.bet_order_list, self.curr_fold_player_list, self.curr_bet_idx)

    def find_next_idx_skip_fold(self, bet_order_list, curr_fold_player_list, curr_bet_idx):

        curr_bet_idx_in_bet_order = bet_order_list.index(curr_bet_idx)
        #print(curr_bet_idx_in_bet_order)

        loop_cnt = 0
        
        while True:
            if loop_cnt == len(bet_order_list):
                break

            for idx in curr_fold_player_list:
                if idx == bet_order_list[curr_bet_idx_in_bet_order]:
                    curr_bet_idx_in_bet_order += 1

                    if curr_bet_idx_in_bet_order == len(bet_order_list):
                        curr_bet_idx_in_bet_order = 0    

            loop_cnt += 1
        
        return bet_order_list[curr_bet_idx_in_bet_order]


    def init_turn(self, recalculate_bet_order = True):

        # change game_state
        #self.game_state = state
        #self.curr_fold_player_list = []
        self.IsBetFinished = False
        self.curr_bet_idx = self.bet_order_list[0]
        
        self.curr_bet_idx = self.find_next_idx_skip_fold(self.bet_order_list, self.curr_fold_player_list, self.curr_bet_idx)

        self.init_bet_list()
        self.update_fold_to_bet_list()
        self.last_raise_idx = -1
        self.update_check_allowable()
        self.update_call_allowable()

    def update_fold_to_bet_list(self):
        for idx in self.curr_fold_player_list:
            self.bet_list[idx] = "Fold"

    def update_turn(self):
        # change the who has no money to allin
        for player in self.players:
            if player.money <= 0:
                player.IsAllIn = True
            player.curr_bet_type = ""
            player.curr_bet_amount = 0
        
    def clear_round(self):
        # init variables
        self.start_game_request_pset = set()
        self.init_round_request_pset = set()
        self.preflop_request_pset = set()
        self.flop_request_pset = set()
        self.turn_request_pset = set()
        self.river_request_pset = set()
        self.showdown_request_pset = set()
        self.quitround_request_pset = set()

        self.InitRoundCnt = 0
        self.PreFlopCnt = 0
        self.FlopCnt = 0
        self.TurnCnt = 0
        self.RiverCnt = 0
        self.ShowDownCnt = 0
        self.QuitRoundCnt = 0

        # update pot

        # update players
        # - update no money to dead

        # update game status


    def get_game(self):
        pass    