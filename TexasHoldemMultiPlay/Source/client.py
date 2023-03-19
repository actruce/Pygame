import pygame
from network import Network
from Game import Game
from view import *

# width = 630
# height = 396
# width = 819
# height = 515
width = 756
height = 475

WHITE=(255,255,255)
DARK_RED=(153, 0, 76)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 153)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 102, 255)
PURPLE = (128,0,128)
PINK = (255, 102, 255)
GRAY = (160, 160, 160)
LIGHT_GRAY = (215, 215, 215)
DARK_GRAY = (96, 96, 96)
LIGHT_BLACK = (32, 32, 32)
CYAN = (0, 255, 255)

tmp_player_names_dict = {}
tmp_player_names_dict[3] = ['James','John','Charls',]
tmp_player_names_dict[4] = ['James','John','Charls','Tobias']
tmp_player_names_dict[5] = ['James','John','Charls','Tobias', 'Young',]

bg = pygame.image.load('../poker_table2.jpg')
bg = pygame.transform.scale(bg, (width, height))
CARD_SURFACE_LIST = []
empty_card = pygame.image.load('../classic-cards-v2/b2fv.png')
empty_card = pygame.transform.scale(empty_card, (54, 72))

#player_pos_dict = {}
# player_pos_dict[3] = [(80, 40), (500, 40), (305, 320), ]
# player_pos_dict[4] = [(70, 35), (510, 35), (430, 320), (200, 320), ]
# player_pos_dict[5] = [(80, 25), (510, 25), (480, 290), (305, 320), (130, 290), ]
player_pos_dict = {}
player_pos_dict[3] = [(160, 40), (500, 40), (355, 360), ]
player_pos_dict[4] = [(160, 40), (510, 40), (520, 320), (180, 320), ]
player_pos_dict[5] = [(160, 40), (510, 40), (570, 320), (350, 320), (140, 320), ]

# card_pos_dict = {}
# card_pos_dict[3] = [(80, 115), (500, 115), (305, 215), ]
# card_pos_dict[4] = [(80, 110), (510, 110), (430, 205), (200, 235), ]
# card_pos_dict[5] = [(80, 100), (510, 100), (480, 205), (305, 215), (130, 205), ]


#pygame.init()
#win = pygame.display.set_mode((width, height))
# win.blit(bg, (0,0))
# pygame.display.update()

def Get_All_Card_Surfaces():
    path = '../classic-cards-v2/'
    i = 0

    for suit in range(4):
        for rank in range(13):
            i += 1
            card_str = path + str(i) + ".png"
            img = pygame.image.load(card_str)
            #img = pygame.transform.scale(img, (54, 72))
            CARD_SURFACE_LIST.append(img)

def get_rid_list(my_rid):
    # to sync game player id with screen pos id
    # 1. CNT = 3, from my r.id make c.w. -> send the first item to the end
    # 2. CNT = 4, from my r.id make c.w. -> send the two items to the end
    # 3. CNT = 5, from my r.id make c.w. -> send the two items to the end                    
    cw_list = []
    rid_list = []

    if my_rid == 0:
        cw_list = list(range(Game.MAX_PLAYER_CNT))
    else:
        cw_list = list(range(my_rid, Game.MAX_PLAYER_CNT)) + list(range(my_rid))
    
    if Game.MAX_PLAYER_CNT == 3:
        rid_list = cw_list[1:] + cw_list[0:1]
    elif Game.MAX_PLAYER_CNT == 4:
        rid_list = cw_list[2:] + cw_list[0:2]
    elif Game.MAX_PLAYER_CNT == 5:
        rid_list = cw_list[2:] + cw_list[0:2]

    return rid_list

def redrawWindows():
    win.blit(bg, (0,0))

    wait_text.draw(win)
    stage_text.draw(win)
    # dealer_text.draw(win)
    # sb_text.draw(win)
    # bb_text.draw(win)

    # draw pot
    pot.draw(win)

    for player in players:
        player.draw(win)

    # draw cards
    for idx in range(Game.MAX_PLAYER_CNT):
        for card in players_cards_screen[idx]:
            card.draw(win)

    # draw community cards
    for card in community_cards:
        card.draw(win)

    # draw bet_readys
    for bet_ready in bet_readys:
        bet_ready.draw(win)

    # draw bets
    for bet in bets:
        bet.draw(win)

    # draw chip
    for chip in chips:
        chip.draw(win)

    # draw btns
    for btn in allbtns:
        btn.draw(win)
    
    # draw arrow
    arrow1.draw(win)

    # draw winner result
    winner_result_draw.draw(win)

    pygame.display.update()


def draw_players_hands(player_cards, pid, rid_list):
    for idx in range(Game.MAX_PLAYER_CNT):
        screen_id = rid_list.index(idx)

        if idx != pid:
            
            player_card = player_cards[idx]

            card1 = player_card[0]
            card2 = player_card[1]

            player_card1 = players_cards_screen[screen_id][0]
            pos_card1 = player_card1.get_pos()
            player_card1.set_pos(pos_card1[0] -10, pos_card1[1], pos_card1[2]-10, pos_card1[3])
            player_card1.set_image(CARD_SURFACE_LIST[ (13*card1.suit) + card1.rank])

            player_card2 = players_cards_screen[screen_id][1]
            pos_card2 = player_card2.get_pos()
            player_card2.set_pos(pos_card2[0] -10, pos_card2[1], pos_card2[2]-10, pos_card2[3])
            player_card2.set_image(CARD_SURFACE_LIST[ (13*card2.suit) + card2.rank])

            player_card1.set_visible(True)
            player_card2.set_visible(True)
    
    redrawWindows()

def draw_winner_result(winner):
    winner_name = winner.name
    winner_idx = winner.id
    winner_result = winner.round_result

    # draw winner_result
    result_text = "Winner: " +winner_name+"(" + str(winner_idx) + ") , " + winner_result.result_name + ', (' + str(winner_result.high_suit) +', ' + str(winner_result.high_rank)+')'
    result_cards = winner_result.hands

    img_list = []
    for card in result_cards:
        img = CARD_SURFACE_LIST[ (13*card.suit) + card.rank]
        img_list.append(img)
    
    winner_result_draw.set_card_imgs(img_list)
    winner_result_draw.set_result_text(result_text)
    winner_result_draw.set_visible(True)

    redrawWindows()

def draw_winner_quit_result(winner):
    if winner != None:
        winner_name = winner.name
        winner_idx = winner.id
        winner_result = "All other players QUIT"

        # draw winner_result
        result_text = "Winner: " +winner_name+"(" + str(winner_idx) + ") , " + winner_result
        print(result_text)
        winner_quit_result_draw.set_result_text(result_text)
        winner_quit_result_draw.set_visible(True)

        redrawWindows()

def init_bets(players_info_dict, rid_list):
    for idx in range(Game.MAX_PLAYER_CNT):
        screen_pid = rid_list.index(idx)
        
        if players_info_dict[idx]["IsFold"]:
            player_rect = players[screen_pid].get_rect()

            if player_rect[1] < height // 2: # on the upper half
                bets[screen_pid].set_pos(player_rect[0] + 60, player_rect[1] + player_rect[3] - 15)
            else: # on the lower half
                bets[screen_pid].set_pos(player_rect[0] + 60, player_rect[1] - 15)
            
            bets[screen_pid].set_bet("Fold", 0)
            bets[screen_pid].set_visible(True)
        else:
            bets[screen_pid].set_visible(False)

def draw_bet_things(prev_turn_pid, curr_turn_pid, rid_list, players_info_dict, IsBetFinished):
    # to draw bet_ready
    # we already knew the current bet pid from Game => curr_turn_pid

    screen_pid = rid_list.index(curr_turn_pid)
    #print("curr_turn_pid: {0}, screen_pid: {1}".format(curr_turn_pid, screen_pid))

    player_rect = players[screen_pid].get_rect()
    
    if player_rect[1] < height // 2: # on the upper half
        bet_readys[screen_pid].set_pos(player_rect[0], player_rect[1] + player_rect[3] + 12)
    else: # on the lower half
        bet_readys[screen_pid].set_pos(player_rect[0], player_rect[1] - 42)
    
    bet_readys[screen_pid].set_visible(True)

    if not prev_turn_pid == -1 and prev_turn_pid != curr_turn_pid:
        screen_pid = rid_list.index(prev_turn_pid)
        bet_readys[screen_pid].set_visible(False)

    # to draw bet & chip when it has changed curr_turn_pid
    if (not prev_turn_pid == -1 and prev_turn_pid != curr_turn_pid) or IsBetFinished:
        player_from_game = players_info_dict[prev_turn_pid]
        curr_bet_type = player_from_game["curr_bet_type"]
        curr_bet_amount = player_from_game["curr_bet_amount"]

        screen_pid = rid_list.index(prev_turn_pid)
        player_rect = players[screen_pid].get_rect()

        print("prev_turn_pid: {0}, curr_turn_pid: {1}, screen_pid: {2}".format(prev_turn_pid, curr_turn_pid, screen_pid))

        if player_rect[1] < height // 2: # on the upper half
            bets[screen_pid].set_pos(player_rect[0] + 65, player_rect[1] + player_rect[3] - 25)
        else: # on the lower half
            bets[screen_pid].set_pos(player_rect[0] + 65, player_rect[1] + 15)
        
        bets[screen_pid].set_bet(curr_bet_type, curr_bet_amount)
        bets[screen_pid].set_visible(True)

        if IsBetFinished:
            bet_readys[screen_pid].set_visible(False)

        # draw chip
        global chips

        if curr_bet_type == "Raise" or curr_bet_type == "Call" or curr_bet_type == "AllIn":
            # if player_rect[1] < height // 2: # on the upper half
            #     chips[screen_pid].set_pos(player_rect[0] + 30, player_rect[1] + player_rect[3] + 5, player_rect[1] + player_rect[3] + 45)
            # else: # on the lower half
            #     chips[screen_pid].set_pos(player_rect[0] + 30, player_rect[1] - 5, player_rect[1] - 45)

            # chips[screen_pid].set_text(str(curr_bet_amount))
            # chips[screen_pid].set_visible(True)

            new_chip_pos_x, new_chip_pos_y, new_chip_pos_y_end = 0, 0, 0

            if player_rect[1] < height // 2: # on the upper half
                new_chip_pos_y = player_rect[1] + player_rect[3] + 5
                new_chip_pos_y_end = new_chip_pos_y + 30
            else:
                new_chip_pos_y = player_rect[1] - 5
                new_chip_pos_y_end = new_chip_pos_y - 30

            len_chips = len(chips)
            chip_color = BLACK

            if len_chips <= len(chip_colors) - 1:
                chip_color = chip_colors[len_chips]

            new_chip = chip('', 100, 100, 24, 17, 50, width, height, chip_color, BLACK, BLACK)

            if len_chips >= 3:
                last_chip_sp_idx = (len_chips // 3 -1) * 3 + len_chips % 3
                last_chip_sp = chips[last_chip_sp_idx]

                # last_chip_sp pos_x has already changed so that just use player's pos

                if player_rect[1] < width // 2: # on the left half
                    new_chip_pos_x = player_rect[0] + 30 - (len_chips // 3) * 10
                else:
                    new_chip_pos_x = player_rect[0] + 30 + (len_chips // 3) * 10
            else:
                if player_rect[1] < width // 2: # on the left half
                    new_chip_pos_x = player_rect[0] + 30
                else:
                    new_chip_pos_x = player_rect[0] + 30

            new_chip.set_pos(new_chip_pos_x, new_chip_pos_y, new_chip_pos_y_end)
            new_chip.set_text(str(curr_bet_amount))
            new_chip.set_visible(True)

            chips.append(new_chip)
            
            print(chips[len(chips)-1].IsVisible)
            print("new chip ({0}, {1}, {2}) has created!".format(new_chip_pos_x, new_chip_pos_y, new_chip_pos_y_end))

    redrawWindows()

def init_player_cards():
    global players_cards_screen    
    global player_pos
    global empty_card

    players_cards_screen = {}
    
    idx = 0

    for pos in player_pos:
        card1 = card(pos[0] - 105, 0, pos[0] - 105, pos[1] - 4, empty_card)
        players_cards_screen[idx] = []
        players_cards_screen[idx].append(card1)
        card2 = card(pos[0] - 60, 0, pos[0] - 60, pos[1] - 4, empty_card)
        players_cards_screen[idx].append(card2)
        idx += 1

    
Get_All_Card_Surfaces()

wait_text = text(160, 195, 'Waiting for other players...', 28, color = (220, 220, 80))
stage_text = text(280, 190, '', 40, color = (220, 220, 200))
# dealer_text = text(0, 0, 'Dealer', 25, color = (244, 244, 244))
# sb_text = text(0, 0, 'Small Blind', 25, color = (244, 244, 244))
# bb_text = text(0, 0, 'Big Blind', 25, color = (244, 244, 244))

pot = pot(width - 100, 20)

players = []

# create players
player_pos = player_pos_dict[Game.MAX_PLAYER_CNT]

for pos in player_pos:
    new_player = player(pos[0], pos[1], "")
    players.append(new_player)

current_player_idx = round((Game.MAX_PLAYER_CNT + 0.1 )/2)

# create players_cards_screen
players_cards_screen = {}
init_player_cards()

# create community cards
community_cards = []

com_card_pos_x = 172
com_card_pos_y = 157

for i in range(5):
    community_cards.append(card(com_card_pos_x + i*80, 0, com_card_pos_x + i*80, com_card_pos_y, empty_card))

# create bet_readys
bet_readys = []

for pos in player_pos:
    new_bet_ready = bet_ready(pos[0], pos[1])
    bet_readys.append(new_bet_ready)

# create bets
bets = []

for pos in player_pos:
    new_bet = bet(pos[0], pos[1])
    bets.append(new_bet)

# create chips
chips = []
chip_colors = [RED, GREEN, YELLOW, PURPLE, BLUE, DARK_RED, BLACK, LIGHT_BLUE, PINK, GRAY, LIGHT_GRAY, LIGHT_BLACK, CYAN]

# winner result
winner_result_draw = winner_result(width //2 - 170, height // 2 - 53)

# winner_quit_result
winner_quit_result_draw = winner_quit_result(width //2 - 260, height // 2 - 15)

# idx = 0
# for pos in player_pos:
#     new_chip = chip('', pos[0], pos[1], 24, 17, 50, width, height, chip_colors[idx], BLACK, BLACK)
#     chips.append(new_chip)
#     idx += 1

# create btns
btn_pos_x, btn_pos_y = 300, 280
check_btn = btn('Check', btn_pos_x + 140, btn_pos_y, 30, LIGHT_BLACK, WHITE, LIGHT_YELLOW ,BLACK)
fold_btn = btn('Fold', btn_pos_x + 220, btn_pos_y, 30, RED, WHITE, LIGHT_YELLOW ,BLACK)
bet_btn = btn('Bet', btn_pos_x + 300, btn_pos_y, 30, CYAN, WHITE, LIGHT_YELLOW ,BLACK)

btns = []
btns.append(check_btn)
btns.append(fold_btn)
btns.append(bet_btn)

call_btn = btn('Call', btn_pos_x + 400, btn_pos_y - 70, 30, BLUE, LIGHT_BLUE, LIGHT_GRAY ,BLACK)
raise_btn = btn('Raise', btn_pos_x + 400, btn_pos_y, 30, RED, PINK, LIGHT_GRAY ,BLACK)
allin_btn = btn('AllIn', btn_pos_x + 400, btn_pos_y + 70, 30, GREEN, LIGHT_YELLOW, LIGHT_GRAY ,BLACK)

bet_btns = []
bet_btns.append(call_btn)
bet_btns.append(raise_btn)
bet_btns.append(allin_btn)

allbtns = []
allbtns = btns + bet_btns

arrow1 = arrow(btn_pos_x + 340, btn_pos_y - 10, 20, 0, BLACK)


def main(input_text):
    run = True
    n = Network()
    p = n.getP() # player no.

    win.blit(bg, (0,0))
    pygame.display.set_caption("Client ({0})".format(p))
    pygame.display.update()

    # update player's state (who participated in)
    #player_name = tmp_player_names_dict[Game.MAX_PLAYER_CNT][p]
    player_name = input_text
    print(player_name)
    game_reply = n.send({"connect_player":player_name})

    clock = pygame.time.Clock()
    
    rid_list = get_rid_list(p)

    not_entered_initround_stage = True
    not_entered_preflop_stage = True
    not_entered_flop_stage = True
    not_entered_turn_stage = True
    not_entered_river_stage = True
    not_entered_showdown_stage = True
    not_entered_quitround_stage = True

    sblind_bet = False
    bblind_bet = False

    prev_turn_pid = -1
    
    while run:
        clock.tick(10)
        global chips

        try:
            game_reply = n.send({"get_game":""})
            game_state = game_reply["game_state"]
            players_info_dict = game_reply["players_info"]
            curr_turn_pid = game_reply["curr_turn_pid"]
            IsBetFinished = game_reply["IsBetFinished"]
            pot_money = game_reply["pot_money"]

            # Betting Info
            init_bet_amount = game_reply["init_bet_amount"]
            #raise_allow_number = game_reply["raise_allow_number"]

            call_amount = game_reply["call_amout"]
            is_check_allowable = game_reply["is_check_allowable"]
            is_call_allowable = game_reply["is_call_allowable"]
            raise_amount = game_reply["raise_amount"]
            #players_info_dict[idx]["curr_raise_number"] = player.curr_raise_number
                        
            if game_state == "StartGame":
                wait_text.set_visible(False)

                stage_text.set_text("Start Game")
                stage_text.set_visible(True)
                
                redrawWindows()

                pygame.time.delay(1000)

                # player request
                game_reply = n.send({"start_game":""})

                # if start_tick_cnt > 60:
                #     # player request
                #     game_reply = n.send({"start_game":""})

            elif game_state == "InitRound":
                if not_entered_initround_stage:
                    not_entered_showdown_stage = True
                    not_entered_quitround_stage = True

                    stage_text.set_text("Init Round...")

                    sblind_bet = True
                    bblind_bet = True

                    pot.set_visible(True)
                    
                    # all visible false
                    winner_result_draw.set_visible(False)

                    chips = []

                    init_player_cards()

                    for card in community_cards:
                        card.set_visible(False)

                    for bet_ready in bet_readys:
                        bet_ready.set_visible(False)
                    
                    for btn in allbtns:
                        btn.set_visible(False)
                    
                    arrow1.set_visible(False)

                    not_entered_initround_stage = False

                tmp_idx = 0
                for player_screen in players:
                    # new player's dict
                    player_from_game = players_info_dict[rid_list[tmp_idx]]
                    name = player_from_game["name"]
                    money = player_from_game["money"]

                    tmp_idx += 1
                    player_screen.set_name(name)
                    player_screen.set_money(money)

                    # display dealer, small blind, big blind
                    isDealer = player_from_game["IsDealer"]
                    isSBlind = player_from_game["IsSmallBlind"]
                    isBBlind = player_from_game["IsBigBlind"]

                    # clear existing roles
                    player_screen.set_dealer(False)
                    player_screen.set_sblind(False)
                    player_screen.set_bblind(False)

                    if isDealer:
                        player_screen.set_dealer(True)
                    if isSBlind:
                        player_screen.set_sblind(True)
                    if isBBlind:
                        player_screen.set_bblind(True)

                # set current player visible
                for player in players:
                    player.set_visible(True)
                
                redrawWindows()

                pygame.time.delay(1000)
                
                # player request
                game_reply = n.send({"init_round":""})

                #if init_round_tick_cnt > 60:
                #     # player request
                #     game_reply = n.send({"start_game":""})

            elif game_state == "PreFlop":
                if not_entered_preflop_stage:
                    stage_text.set_text("Pre Flop")

                    prev_turn_pid = -1
                    chips = []
                    init_bets(players_info_dict, rid_list)
                    
                    not_entered_preflop_stage = False

                # player request if current stages' bet finished
                if IsBetFinished:
                    game_reply = n.send({"preflop":""})
                    continue

                # display the cards
                list_cards = game_reply["players_cards"][p]

                card1 = list_cards[0]
                card2 = list_cards[1]

                for idx in range(Game.MAX_PLAYER_CNT):
                    players_cards_screen[idx][0].set_visible(True)
                    players_cards_screen[idx][1].set_visible(True)

                player_card1 = players_cards_screen[current_player_idx][0]
                player_card1.set_image(CARD_SURFACE_LIST[ (13*card1.suit) + card1.rank])
                player_card1.set_player_card(True)

                player_card2 = players_cards_screen[current_player_idx][1]
                player_card2.set_image(CARD_SURFACE_LIST[ (13*card2.suit) + card2.rank])
                player_card2.set_player_card(True)

                # to draw bet_readys, bets, chips
                draw_bet_things(prev_turn_pid, curr_turn_pid, rid_list, players_info_dict, IsBetFinished)

                # SBlind & BBlind automatically "Raise"
                if curr_turn_pid == p:
                    if players_info_dict[p]["IsSmallBlind"] and sblind_bet:
                        game_reply = n.send({"player_bet": ("Raise", init_bet_amount)})
                        sblind_bet = False

                    elif players_info_dict[p]["IsBigBlind"] and bblind_bet:
                        game_reply = n.send({"player_bet": ("Raise", raise_amount)})
                        bblind_bet = False

                prev_turn_pid = curr_turn_pid

                #print("chips count = {}".format(len(chips)))
                redrawWindows()

            elif game_state == "Flop":
                if not_entered_flop_stage:
                    stage_text.set_text("Flop")

                    prev_turn_pid = -1
                    
                    # visible false the bet and chips and btns and arrow
                    chips = []

                    init_bets(players_info_dict, rid_list)

                    for bet_ready in bet_readys:
                        bet_ready.set_visible(False)
                    
                    for btn in allbtns:
                        btn.set_visible(False)
                    
                    arrow1.set_visible(False)

                    not_entered_flop_stage = False

                # player request if current stages' bet finished
                if IsBetFinished:
                    #print("IsBetFinished")
                    game_reply = n.send({"flop":""})
                    continue

                # display community cards
                list_cards = game_reply["community_cards"]

                community_cards[0].set_image(CARD_SURFACE_LIST[ (13*list_cards[0].suit) + list_cards[0].rank])
                community_cards[0].set_visible(True)

                community_cards[1].set_image(CARD_SURFACE_LIST[ (13*list_cards[1].suit) + list_cards[1].rank])
                community_cards[1].set_visible(True)

                community_cards[2].set_image(CARD_SURFACE_LIST[ (13*list_cards[2].suit) + list_cards[2].rank])
                community_cards[2].set_visible(True)

                # to draw bet_readys, bets, chips
                draw_bet_things(prev_turn_pid, curr_turn_pid, rid_list, players_info_dict, IsBetFinished)

                prev_turn_pid = curr_turn_pid

                redrawWindows()

            elif game_state == "Turn":
                if not_entered_turn_stage:
                    stage_text.set_text("Turn")

                    prev_turn_pid = -1
                    
                    # visible false the bet and chips and btns and arrow
                    chips = []
                    init_bets(players_info_dict, rid_list)

                    for bet_ready in bet_readys:
                        bet_ready.set_visible(False)
                    
                    for btn in allbtns:
                        btn.set_visible(False)
                    
                    arrow1.set_visible(False)

                    not_entered_turn_stage = False

                # player request if current stages' bet finished
                if IsBetFinished:
                    #print("IsBetFinished")
                    game_reply = n.send({"turn":""})
                    continue

                # display community cards
                list_cards = game_reply["community_cards"]

                community_cards[3].set_image(CARD_SURFACE_LIST[ (13*list_cards[3].suit) + list_cards[3].rank])
                community_cards[3].set_visible(True)

                # to draw bet_readys, bets, chips
                draw_bet_things(prev_turn_pid, curr_turn_pid, rid_list, players_info_dict, IsBetFinished)

                prev_turn_pid = curr_turn_pid

                redrawWindows()

            elif game_state == "River":
                if not_entered_river_stage:
                    stage_text.set_text("River")

                    prev_turn_pid = -1
                    
                    # visible false the bet and chips and btns and arrow
                    chips = []
                    init_bets(players_info_dict, rid_list)

                    for bet_ready in bet_readys:
                        bet_ready.set_visible(False)
                    
                    for btn in allbtns:
                        btn.set_visible(False)
                    
                    arrow1.set_visible(False)

                    not_entered_river_stage = False

                # player request if current stages' bet finished
                if IsBetFinished:
                    #print("IsBetFinished")
                    game_reply = n.send({"river":""})
                    continue

                # display community cards
                list_cards = game_reply["community_cards"]

                community_cards[4].set_image(CARD_SURFACE_LIST[ (13*list_cards[4].suit) + list_cards[4].rank])
                community_cards[4].set_visible(True)

                # to draw bet_readys, bets, chips
                draw_bet_things(prev_turn_pid, curr_turn_pid, rid_list, players_info_dict, IsBetFinished)

                prev_turn_pid = curr_turn_pid

                redrawWindows()

            elif game_state == "Showdown":
                if not_entered_showdown_stage:
                    stage_text.set_text("ShowDown")

                    # visible false the bet and chips and btns and arrow
                    chips = []

                    for bet in bets:
                        bet.set_visible(False)
                    
                    for btn in allbtns:
                        btn.set_visible(False)
                    
                    arrow1.set_visible(False)

                    not_entered_showdown_stage = False

                # draw each players' hands
                draw_players_hands(game_reply["players_cards"], p, rid_list)
                redrawWindows()
                pygame.time.delay(500)

                # draw winner
                draw_winner_result(game_reply["winner"])
                redrawWindows()
                pygame.time.delay(6000)
                #pygame.time.delay(10000)
                
                # to show the winner and result
                # send showdown to request next
                game_reply = n.send({"showdown":""})

                not_entered_initround_stage = True
                not_entered_preflop_stage = True
                not_entered_flop_stage = True
                not_entered_turn_stage = True
                not_entered_river_stage = True

            elif game_state == "QuitRound":
                if not_entered_quitround_stage:
                    stage_text.set_text("Quit Round")
                    print("Get into Quit Round")

                    # visible false the bet and chips and btns and arrow
                    chips = []

                    for bet in bets:
                        bet.set_visible(False)
                    
                    for btn in allbtns:
                        btn.set_visible(False)
                    
                    arrow1.set_visible(False)

                    not_entered_quitround_stage = False

                # draw winner_quit
                draw_winner_quit_result(game_reply["winner"])
                redrawWindows()
                pygame.time.delay(3000)
                
                # to show the winner and result
                # send showdown to request next
                game_reply = n.send({"quitround":""})

                not_entered_initround_stage = True
                not_entered_preflop_stage = True
                not_entered_flop_stage = True
                not_entered_turn_stage = True
                not_entered_river_stage = True
                
            else:
                wait_text.set_visible(True)
                redrawWindows()
        
            # to draw btns
            if game_state == "PreFlop" or game_state == "Flop" or game_state == "Turn" or game_state == "River":

                # display player
                tmp_idx = 0
                for player_screen in players:
                    # new player's dict
                    player_from_game = players_info_dict[rid_list[tmp_idx]]
                    name = player_from_game["name"]
                    money = player_from_game["money"]

                    tmp_idx += 1
                    player_screen.set_name(name)
                    player_screen.set_money(money)

                # display pot
                pot.set_money(pot_money)
                    
                # draw bet buttons
                if curr_turn_pid == p:
                    for btn in btns:
                        btn.set_visible(True)

                        if btn.is_equal("Check"):
                            if not is_check_allowable:
                                btn.set_visible(False)

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print("mouse down")
                            pos = pygame.mouse.get_pos()

                            bet_type = ""
                            bet_amount = 0

                            for btn in btns:
                                if btn.inside_pos(pos):
                                    if btn.is_equal("Check"):
                                        bet_type = "Check"
                                    elif btn.is_equal("Fold"):
                                        bet_type = "Fold"
                                    elif btn.is_equal("Bet"):
                                        arrow1.toggle_visible()
                                        
                                        for item in bet_btns:
                                            if not item.is_equal("Call"): # Call is visible when it is only call_allowable
                                                item.toggle_visible()
                                            else:
                                                if is_call_allowable:
                                                    item.toggle_visible()

                            for btn in bet_btns:
                                if btn.inside_pos(pos):
                                    if btn.is_equal("Call"):
                                        bet_type = "Call"
                                        bet_amount = call_amount
                                    elif btn.is_equal("Raise"):
                                        bet_type = "Raise"
                                        bet_amount = raise_amount
                                    elif btn.is_equal("AllIn"):
                                        bet_type = "AllIn"
                                        bet_amount = raise_amount # should be modified

                            if bet_type == "Check":
                                game_reply = n.send({"player_check": ""})
                            elif bet_type == "Fold":
                                game_reply = n.send({"player_fold": ""})
                            elif bet_type == "Call" or bet_type == "Raise" or bet_type == "AllIn":
                                game_reply = n.send({"player_bet": (bet_type, bet_amount)})
                                            
                        elif event.type == pygame.MOUSEMOTION:
                            pos = pygame.mouse.get_pos()
                            
                            for btn in allbtns:
                                if btn.inside_pos(pos):
                                    btn.set_ismousedown(True)
                                else:
                                    btn.set_ismousedown(False)

                else:
                    arrow1.set_visible(False)

                    for btn in allbtns:
                        btn.set_visible(False)

                redrawWindows()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
    
        except Exception as e:
                    run = False
                    print (str(e))

#main()

def menu_screen():
    pos_init_x, pos_init_y = 130, 100
    
    input_box = pygame.Rect(pos_init_x, pos_init_y + 40, 140, 32)
    color_inactive = pygame.Color('LIGHTSKYBLUE')
    color_active = pygame.Color('DODGERBLUE')
    color = color_inactive
    enter_btn = btn2('Join', 'Game', pos_init_x + 280, pos_init_y + 40, 33, pygame.Color('DARKTURQUOISE'), 
                     pygame.Color('WHITE'), pygame.Color('THISTLE') , pygame.Color('FIREBRICK'))
    enter_btn.set_visible(True)

    
    active = False
    input_text = ''
    done = False
    
    clock = pygame.time.Clock()

    while not done:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if enter_btn.inside_pos(pos):
                    print(input_text)
                    main(input_text)
                    
                
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
                
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()

                if enter_btn.inside_pos(pos):
                    enter_btn.set_ismousedown(True)
                else:
                    enter_btn.set_ismousedown(False)
                
                
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(input_text)
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        win.fill((30, 30, 30))
        
        font = pygame.font.Font(None, 28)
        txt = font.render("Please input your name", True, (255, 255, 255))
        win.blit(txt, (pos_init_x, pos_init_y))
        
        # Render the current text.
        txt_surface = font.render(input_text, True, color)
        # Resize the box if the text is too long.
        input_box_width = max(220, txt_surface.get_width()+10)
        input_box.w = input_box_width
        # Blit the text.
        win.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(win, color, input_box, 2)
        # Blit the Btn
        enter_btn.draw(win)

        pygame.display.update()

pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.update()

while True:
    menu_screen()
