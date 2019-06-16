import pygame
from pygame.locals import *
from Events import *
from CardCommon import *

PLAYER_CARD = 'player_card'
COMMUNITY_CARD = 'community_card'

# ------------------------------------------------------
# Card Sources -> pygame.Surface
CARD_SURFACE_LIST = []

class Game:
    """..."""
    STATE_INITIAL = 'initial'
    STATE_PREPARING = 'preparing'
    STATE_PREFLOP = 'preflop'
    STATE_FLOP = 'flop'
    STATE_TURN = 'turn'
    STATE_RIVER = 'river'
    STATE_SHOWDOWN = 'showdown'


    def __init__(self, evManager):
        self.game_deck = Deck()
        self.players = []
        self.community_cards = []

        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.state = Game.STATE_INITIAL

    # Event Notify
    def Notify(self, event):
        if isinstance(event, GameStartRequest):
            if self.state == Game.STATE_INITIAL:
                self.Start()

        if isinstance(event, NextTurnEvent):
            if self.state == Game.STATE_PREPARING:
                self.deal_preflop()
            elif self.state == Game.STATE_PREFLOP:
                self.deal_flop()
            elif self.state == Game.STATE_FLOP:
                self.deal_turn()
            elif self.state == Game.STATE_TURN:
                self.deal_river()
            elif self.state == Game.STATE_RIVER:
                self.show_down()
            elif self.state == Game.STATE_SHOWDOWN:
                self.InitializeRound()


    def Start(self):
        print ('-------------------------------------------------------')
        print ('Initialize Game: ')
        self.community_cards = []
        self.InitializePlayers()
        self.InitializePot()
        self.InitializeRound()
        self.Get_All_Card_Surfaces()
        print ('InitializeRound')

    def InitializeRound(self):
        self.state = Game.STATE_PREPARING
        # Initialize Round
        self.game_deck.InitializeDeck()
        self.game_deck.ShuffleDeck()
        self.community_cards = []

        self.InitializePot()

        #Initialize Players's holecards
        for player in self.players:
            player.init_holecards()

        self.evManager.Post(InitializeRoundEvent())


    def InitializePlayers(self):
        self.players = []
        self.players.append(Player('Patrick', 0))
        self.players.append(Player('Gorge', 1))
        self.players.append(Player('Chen', 2))
        self.players.append(Player('Jason', 3))
        self.players.append(Player('Marie', 4))

    def InitializePot(self):
        self.pot = Pot()

    def Get_All_Card_Surfaces(self):
        for suit in range(4):
            for rank in range(13):
                card_str = self.GetCardImageName(Card(suit, rank))
                CARD_SURFACE_LIST.append(pygame.image.load(card_str))

    def GetCardImageName(self, card):
            suit = card.GetSuit()
            rank = card.GetRank()

            suit_str = ''
            rank_str = ''

            if suit == 0:
                suit_str = 'spades'
            elif suit == 1:
                suit_str = 'diamonds'
            elif suit == 2:
                suit_str = 'hearts'
            elif suit == 3:
                suit_str = 'clubs'

            if rank == 0:
                rank_str = 'ace'
            elif rank > 0 and rank < 10:
                rank_str = str(rank +1)
            elif rank == 10:
                rank_str = 'jack'
            elif rank == 11:
                rank_str = 'queen'
            elif rank == 12:
                rank_str = 'king'

            tmp_str = 'playing_cards/'+ rank_str + '_'+ suit_str + '.png'
            return tmp_str

    # pre-flop: deal 2 hold_cards to each players
    def deal_preflop(self):
        self.state = Game.STATE_PREFLOP
        print ('-------------------------------------------------------')
        print ('Pre-Flop Stage: Deal 2 Hold Cards for each players')
        player_count = len(self.players)

        # allocate card to players (2 per each)
        for i in range(player_count * 2):
            self.players[i%player_count].add_cards(self.game_deck.Pop_card())

        self.evManager.Post(PreFlopEvent(self.players))
        self.PrintCards()

    # flop : deal 3 community cards
    def deal_flop(self):
        self.state = Game.STATE_FLOP
        print ('-------------------------------------------------------')
        print ('Flop Stage: Deal 3 Community Cards')
        for i in range(3):
            self.community_cards.append(self.game_deck.Pop_card())

        self.evManager.Post(FlopEvent(self.community_cards))
        self.PrintCards()

    # turn : deal 1 community cards
    def deal_turn(self):
        self.state = Game.STATE_TURN
        print ('-------------------------------------------------------')
        print ('Turn Stage: Deal 1 Community Card')
        new_community_card = self.game_deck.Pop_card()
        self.community_cards.append(new_community_card)

        self.evManager.Post(TurnEvent(new_community_card))
        self.PrintCards()

    # river : deal 1 community cards
    def deal_river(self):
        self.state = Game.STATE_RIVER
        print ('-------------------------------------------------------')
        print ('River Stage: Deal 1 Community Card')
        new_community_card = self.game_deck.Pop_card()
        self.community_cards.append(new_community_card)

        self.evManager.Post(RiverEvent(new_community_card))

        self.PrintCards()

    # show_down : check winner
    def show_down(self):
        self.state = Game.STATE_SHOWDOWN
        print ('-------------------------------------------------------')
        print ('ShowDown Stage: Check BestCards and Choose Winner')
        for player in self.players:
            print ('Player ' + str(player.position) + ': \n')
            player.choice_best_cards(self.community_cards)
            PokerHelper.PrintCards(player.round_result.hands)

        winner = self.GetWinner()
        self.evManager.Post(ShowDownEvent(winner, self.community_cards, winner.round_result.hands))


    def GetWinner(self):
        players = self.players
        sorted_player = sorted(players, key = PokerHelper.cmp_to_key(PokerHelper.CompareTwoPlayerHands), reverse = True)

        print ('--------------------- sorted players ---------------------')
        for player in sorted_player:
            print (player.name)
            print (player.round_result)


        winner = sorted_player[0]

        print ('\nWinner => ' + winner.name + ', P'+ str (winner.position))
        print (winner.round_result)

        return winner


    def pot_to_winner(self):
        pass

    def PrintCards(self):
        #print hole cards
        print ('Hole Cards:')
        for player in self.players:
            for card in player.holecards:
                print ('player: ', player.name, card)

        print ('Community Cards:')
        for card in self.community_cards:
            print (card)


class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue = []
        self.listenersToAdd = []
        self.listenersToRemove = []

    # ----------------------------------------------------------------------
    def RegisterListener(self, listener):
        self.listenersToAdd.append(listener)

    # ----------------------------------------------------------------------
    def ActuallyUpdateListeners(self):
        for listener in self.listenersToAdd:
            self.listeners[listener] = 1
        for listener in self.listenersToRemove:
            if listener in self.listeners:
                del self.listeners[listener]

    # ----------------------------------------------------------------------
    def UnregisterListener(self, listener):
        self.listenersToRemove.append(listener)

    # ----------------------------------------------------------------------
    def Post(self, event):
        self.eventQueue.append(event)
        if isinstance(event, TickEvent):
            # Consume the event queue every Tick.
            self.ActuallyUpdateListeners()
            self.ConsumeEventQueue()

    # ----------------------------------------------------------------------
    def ConsumeEventQueue(self):
        i = 0
        while i < len(self.eventQueue):
            event = self.eventQueue[i]
            for listener in self.listeners:
                # Note: a side effect of notifying the listener
                # could be that more events are put on the queue
                # or listeners could Register / Unregister
                old = len(self.eventQueue)
                listener.Notify(event)
            i += 1
            if self.listenersToAdd:
                self.ActuallyUpdateListeners()
        # all code paths that could possibly add more events to
        # the eventQueue have been exhausted at this point, so
        # it's safe to empty the queue
        self.eventQueue = []
#------------------------------------------------------

#------------------------------------------------------
# Controllers
class CPUSpinnerController:
    """..."""

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.keepGoing = 1

    # ----------------------------------------------------------------------
    def Run(self):
        while self.keepGoing:
            event = TickEvent()
            self.evManager.Post(event)

    # ----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance(event, QuitEvent):
            # this will stop the while loop from running
            self.keepGoing = False

from pygame import *
class KeyboardController:
    """KeyboardController takes Pygame events generated by the
    keyboard and uses them to control the model, by sending Requests
    or to control the Pygame display directly, as with the QuitEvent
    """

    def __init__(self, evManager, playerName=None):
        '''playerName is an optional argument; when given, this
        keyboardController will control only the specified player
        '''
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.activePlayer = None
        self.playerName = playerName
        self.players = []

    # ----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance(event, TickEvent):
            # Handle Input Events
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                        and event.key == pygame.K_ESCAPE:
                    ev = QuitEvent()

                elif event.type == KEYDOWN \
                        and event.key == (K_DOWN or K_UP or K_LEFT or K_RIGHT):
                    #print 'key down up left right pressed'
                    ev = NextTurnEvent()

                elif event.type == pygame.KEYDOWN \
                        and event.key == K_SPACE:
                    ev = GameStartRequest()

                if ev:
                    self.evManager.Post(ev)



# ------------------------------------------------------
# Sprites

class CardSprite(pygame.sprite.Sprite):
    SPEED = 0.6

    def __init__(self, card, src_pos,  dest_pos, type, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        #Instead of loading image directly when CardSprite created, Use Preloaded Surfaces
        #self.src_image = pygame.image.load(self.GetCardImageName(card))
        self.src_image = CARD_SURFACE_LIST[card.suit*1 + card.rank]
        self.image = self.src_image
        self.pos = [0.0, 0.0]
        self.pos[0] = src_pos[0] * 1.0  # float
        self.pos[1] = src_pos[1] * 1.0  # float
        self.dest_pos = dest_pos
        self.src_pos = src_pos
        self.type = type
        self.rect = self.src_image.get_rect()

    def update(self, seconds):
        # updated position over the destination pos
        # calibrate the final pos not over the dest_pos
        if(self.type == PLAYER_CARD or self.type == COMMUNITY_CARD):
            if self.dest_pos[0] - self.src_pos[0] < 0 \
                and self.dest_pos[0] <= self.pos[0]:
                self.pos[0] += self.GetDelX(self.SPEED, seconds)
                if self.pos[0] <= self.dest_pos[0]:
                    self.pos[0] = self.dest_pos[0]
            if self.dest_pos[0] - self.src_pos[0] >= 0 \
                and self.dest_pos[0] >= self.pos[0]:
                self.pos[0] += self.GetDelX(self.SPEED, seconds)
                if self.pos[0] >= self.dest_pos[0]:
                    self.pos[0] = self.dest_pos[0]
            if self.dest_pos[1] - self.src_pos[1] < 0 \
                and self.dest_pos[1] <= self.pos[1]:
                self.pos[1] += self.GetDelY(self.SPEED, seconds)
                if self.pos[1] <= self.dest_pos[1]:
                    self.pos[1] = self.dest_pos[1]
            if self.dest_pos[1] - self.src_pos[1] >= 0 \
                and self.dest_pos[1] >= self.pos[1]:
                self.pos[1] += self.GetDelY(self.SPEED, seconds)
                if self.pos[1] >= self.dest_pos[1]:
                    self.pos[1] = self.dest_pos[1]

        self.rect.centerx = round(self.pos[0], 0)
        self.rect.centery = round(self.pos[1], 0)

    def GetDelX(self, speed, seconds):
        return (-1.0) *(self.src_pos[0] - self.dest_pos[0]) / seconds / speed

    def GetDelY(self, speed, seconds):
        return (-1.0) *(self.src_pos[1] - self.dest_pos[1]) / seconds / speed


    

import pygame
class TableSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        tableSurf = pygame.Surface((1300, 700))
        tableSurf = tableSurf.convert_alpha()
        tableSurf.fill((0, 0, 0, 0))  # make transparent
        pygame.draw.ellipse(tableSurf, (10, 100, 10), [195, 140, 910, 420])

        self.image = tableSurf
        self.rect = (0, 0)

    def update(self, seconds):
        pass

class TextSprite(pygame.sprite.Sprite):

    MAX_MOVE_X = 100
    MAX_FONT_SIZE = 60
    SPEED = 0.5

    def __init__(self, text, position, size, color, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.fontcolor = color
        self.fontsize = size
        self.text = text

        textSurf = self.writeSomething(self.text)
        self.image = textSurf
        self.rect = textSurf.get_rect()
        self.position = position
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

        # about font move animation
        self.canMove = False
        self.prev_x_pos = None

        # about font size animation
        self.canMakeBiggerFont = False
        self.repeat_cnt = 0
        self.prev_font_size = self.fontsize
        self.dest_font_size = self.MAX_FONT_SIZE

    def writeSomething(self, msg=""):

        # if float(self.fontsize).is_integer():
        #     myfont = pygame.font.SysFont("None", self.fontsize)
        #     print('integer')
        # else:
        #     myfont = pygame.font.SysFont("None", int(self.fontsize))
        #     print('no integer')

        myfont = pygame.font.SysFont("None", self.fontsize)
        mytext = myfont.render(msg, True, self.fontcolor)
        mytext = mytext.convert_alpha()
        return mytext

    def newcolor(self):
        # any colour but black or white
        return (random.randint(10, 250), random.randint(10, 250), random.randint(10, 250))

    def update(self, seconds):
        textSurf = self.writeSomething(self.text)
        self.image = textSurf
        self.rect = textSurf.get_rect()
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

        if self.canMove:
            self.rect.centerx += self.MAX_MOVE_X / seconds
            if self.rect.centerx >= self.prev_x_pos + self.MAX_MOVE_X:
                self.ChangeMoveTo()

        if self.canMakeBiggerFont:
            self.DoBiggerEffect(seconds)

    def ChangeMoveTo(self):
        if not self.canMove:
            self.canMove = True
            self.prev_x_pos = self.rect.centerx
        else:
            self.canMove = False
            self.prev_x_pos = None

    def ChangeMakeBigger(self):
        if not self.canMakeBiggerFont:
            self.canMakeBiggerFont = True
        else:
            self.canMakeBiggerFont = False

    def DoBiggerEffect(self, seconds):
        font_diff = self.dest_font_size- self.prev_font_size

        if self.repeat_cnt <= 2:
            if (font_diff >=0 and self.fontsize >= self.dest_font_size) \
                    or (font_diff <= 0 and self.fontsize <= self.dest_font_size):
                tmp_font_size = self.prev_font_size
                self.prev_font_size = self.dest_font_size
                self.dest_font_size = tmp_font_size
                font_diff = self.dest_font_size - self.prev_font_size
                self.repeat_cnt += 1

            del_f_size = font_diff / seconds / self.SPEED

            # if the delta font size is bigger than 5% of current font size
            # just use 5%
            if del_f_size > 0.1 * self.fontsize :
                del_f_size = 0.1 * self.fontsize

            self.fontsize += int(del_f_size)


        else:
            self.ChangeMakeBigger()

class RectSprite(pygame.sprite.Sprite):
    def __init__(self, position, width, height, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.width = width
        self.height = height
        self.position = position

        recSurf = pygame.Surface((1300, 700))
        recSurf = recSurf.convert_alpha()
        recSurf.fill((0, 0, 0, 0))  # make transparent
        pygame.draw.rect(recSurf, (250, 250, 100), [self.position[0], self.position[1], self.width, self.height], 5)
        self.image = recSurf
        self.rect = recSurf.get_rect()

    def update(self, seconds):
        pass


#------------------------------------------------------
# PygameView

class PygameView:
    DECK_POSITION = [750, 50]

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()
        self.window = pygame.display.set_mode((1300, 700))
        pygame.display.set_caption('Texas Holdem')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((25, 65, 25))

        self.window.blit(self.background, (0, 0))

        font = pygame.font.Font(None, 60)
        textSurf = font.render("""Press SPACE BAR to start""", True, (120, 120, 120))
        textSurf = textSurf.convert_alpha()
        self.window.blit(textSurf, (400, 270))

        teststr = """Press an Arrows to progress"""
        #teststr = u'\u2190'
        textSurf = font.render(teststr, True, (120, 120, 120))
        textSurf = textSurf.convert_alpha()
        self.window.blit(textSurf, (370, 350))

        pygame.display.flip()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.playerSprites = pygame.sprite.RenderUpdates()
        self.communitySprites = pygame.sprite.RenderUpdates()

    def ShowCommunityCards(self, card_list):
        i = 0
        for card in card_list:
            i += 1
            newSprite = CardSprite(card, self.DECK_POSITION, (350 + i * 100, 350), COMMUNITY_CARD, self.communitySprites)
            newSprite = None

    def ShowTurnCard(self, card):
        newSprite = CardSprite(card, self.DECK_POSITION, (750, 350), COMMUNITY_CARD, self.communitySprites)

    def ShowRiverCard(self, card):
        newSprite = CardSprite(card, self.DECK_POSITION, (850, 350), COMMUNITY_CARD, self.communitySprites)

    def ShowShowDownResult(self, player, community_cards, card_list):

        for aSprite in self.playerSprites:
            if isinstance(aSprite, TextSprite):
                if aSprite.text == player.name:
                    aSprite.ChangeMakeBigger()

        # Remove previouse community fileds
        for cardSprite in self.communitySprites:
            cardSprite.kill()

        #Redraw Comminity Card with small size above Winner Announcing
        newSprite = RectSprite((400, 140), 500, 120, self.communitySprites)
        newSprite = None

        i = 0
        for card in community_cards:
            i += 1
            newSprite = CardSprite(card, self.DECK_POSITION, (350 + i * 100, 200), COMMUNITY_CARD,
                                   self.communitySprites)
            newSprite = None

        i = 0
        for card in card_list:
            i += 1
            newSprite = CardSprite(card, self.DECK_POSITION, (350 + i * 100, 450), COMMUNITY_CARD, self.communitySprites)
            newSprite = None

        newSprite = TextSprite("The Winner is " + player.name, (550, 300), 60, (200, 30, 10), self.communitySprites)
        newSprite = None
        newSprite = TextSprite("\""+player.round_result.result_name+"\"", (550, 360), 50, (200, 40, 200), self.communitySprites)


    def ShowPreFlopCards(self, players):

        POS_LEFT = 0
        POS_TOP = 0

        for player in players:
            player_pos = player.position
            bottomMultiply = -1

            if player_pos == 0:
                POS_LEFT = 235
                POS_TOP = 160
            elif player_pos == 1:
                POS_LEFT = 170
                POS_TOP = 450
                bottomMultiply = 1
            elif player_pos == 2:
                POS_LEFT = 670
                POS_TOP = 590
                bottomMultiply = 1
            elif player_pos == 3:
                POS_LEFT = 1200
                POS_TOP = 450
                bottomMultiply = 1
            elif player_pos == 4:
                POS_LEFT = 1100
                POS_TOP = 160

            newSprite = CardSprite(player.holecards[0], self.DECK_POSITION, (POS_LEFT - 85, POS_TOP + (bottomMultiply) * 30), PLAYER_CARD, self.playerSprites)
            newSprite = CardSprite(player.holecards[1], self.DECK_POSITION, (POS_LEFT + 14, POS_TOP + (bottomMultiply) * 30), PLAYER_CARD, self.playerSprites)
            newSprite = TextSprite(player.name, (POS_LEFT - 20, POS_TOP - (bottomMultiply) * 40), 30, (150, 150, 150), self.playerSprites)

    def InitializeFrontSprites(self):
        for cardSprite in self.communitySprites:
            cardSprite.kill()

        for cardSprite in self.playerSprites:
            cardSprite.kill()

        for textSprite in self.communitySprites:
            textSprite.kill()

        for textSprite in self.playerSprites:
            textSprite.kill()


    def ShowTable(self):
        newSprite = TableSprite(self.backSprites)

    def ShowInitGame(self):
        pass
        #self.background = pygame.Surface(self.window.get_size())
        #self.background.fill((25, 65, 25))
        #self.window.blit(self.background, (0, 0))

    # ----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance(event, TickEvent):
            # Draw Everything
            self.backSprites.clear(self.window, self.background)
            self.playerSprites.clear(self.window, self.background)
            self.communitySprites.clear(self.window, self.background)

            seconds = 60

            self.backSprites.update(seconds)
            self.playerSprites.update(seconds)
            self.communitySprites.update(seconds)

            dirtyRects1 = self.backSprites.draw(self.window)
            dirtyRects2 = self.playerSprites.draw(self.window)
            dirtyRects3 = self.communitySprites.draw(self.window)

            dirtyRects = dirtyRects1 + dirtyRects2 + dirtyRects3
            pygame.display.update(dirtyRects)

        if isinstance(event, GameStartRequest):
            #self.ShowInitGame()
            self.ShowTable()

        if isinstance(event, PreFlopEvent):
            self.ShowPreFlopCards(event.players)

        if isinstance(event, FlopEvent):
            self.ShowCommunityCards(event.card_list)

        if isinstance(event, TurnEvent):
            self.ShowTurnCard(event.card)

        if isinstance(event, RiverEvent):
            self.ShowRiverCard(event.card)

        if isinstance(event, ShowDownEvent):
            self.ShowShowDownResult(event.player, event.community_cards, event.card_list)

        if isinstance(event, InitializeRoundEvent):
            self.InitializeFrontSprites()

#------------------------------------------------------
def main():
    evManager = EventManager()

    keybd = KeyboardController(evManager)
    spinner = CPUSpinnerController(evManager)
    pygameView = PygameView(evManager)

    texas_holdem = Game(evManager)

    spinner.Run()


if __name__ == "__main__":
    main()



