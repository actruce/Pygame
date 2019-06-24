import pygame
from math import *

class player(object):
    def __init__(self, x, y, name, width = 60, height = 70):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.money = 0
        self.Ismyturn = False
        self.IsVisible = False
        self.IsDealer = False
        self.IsSBlind = False
        self.IsBBlind = False
        self.vel = 5
        self.id = 0

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def set_visible(self, bVisible):
        self.IsVisible = bVisible

    def set_money(self, amount):
        self.money = amount

    def set_myturn(self):
        self.Ismyturn = True

    def set_dealer(self, bDealer):
        self.IsDealer = bDealer
    
    def set_sblind(self, bSBlind):
        self.IsSBlind = bSBlind

    def set_bblind(self, bBBlind):
        self.IsBBlind = bBBlind

    def set_name(self, name):
        self.name = name
    
    def set_player_id(self, id):
        self.id = id

    def draw(self, win):
        if self.IsVisible:
            pygame.draw.rect(win, (220, 220, 220), (self.x, self.y, self.width, self.height), 3)

            #font = pygame.font.SysFont('consolas', 16)
            font = pygame.font.SysFont('comic sans MS', 16)

            name = font.render(self.name, True, (255, 255, 255))
            pygame.draw.rect(win, (160,180,50), (self.x, self.y, self.width, 22), 0)
            win.blit(name, (self.x, self.y))

            pygame.draw.rect(win, (30,30,30), (self.x, self.y +22, self.width, 2), 0)
            
            money = font.render(str(self.money), True, (255, 255, 255))
            pygame.draw.rect(win, (250,120,250), (self.x, self.y + 24, self.width, 22), 0)
            win.blit(money, (self.x + 11, self.y + 25))

            pygame.draw.rect(win, (30,30,30), (self.x, self.y +46, self.width, 2), 0)

        if self.IsDealer or self.IsSBlind or self.IsBBlind:
            text_str = ''
            font = pygame.font.SysFont('comic sans MS', 16)

            if self.IsDealer:
                text_str = 'Dealer'
            elif self.IsSBlind:
                text_str = 'S blind'
            elif self.IsBBlind:
                text_str = 'B blind'
            
            text = font.render(text_str, True, (10, 10, 10))
            pygame.draw.rect(win, (250,250,250), (self.x, self.y + 48, self.width, 22), 0)
            win.blit(text, (self.x + 2, self.y + 48))

        if self.Ismyturn:
            # draw turn bar
            pass

class pot(object):
    def __init__(self, x, y, width = 95, height = 49):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.money = 0
        self.IsVisible = False

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def set_visible(self, bVisible):
        self.IsVisible = bVisible

    def set_money(self, amount):
        self.money = amount

    def draw(self, win):
        if self.IsVisible:
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), 3)

            #font = pygame.font.SysFont('consolas', 16)
            font = pygame.font.SysFont('comic sans MS', 20)

            pot_text = font.render('The Pot', True, (0, 0, 0))
            pygame.draw.rect(win, (216,8,8), (self.x + 1, self.y + 1, self.width-3, 26), 0)
            win.blit(pot_text, (self.x + 10, self.y-1))

            pygame.draw.rect(win, (30,30,30), (self.x, self.y +27, self.width, 2), 0)

            font = pygame.font.SysFont('comic sans MS', 18)
            
            money = font.render(str(self.money), True, (255, 255, 255))
            rect = money.get_rect()
            pygame.draw.rect(win, (130,124,102), (self.x + 1, self.y + 29, self.width-3, 20), 0)
            win.blit(money, (self.x + self.width //2 - rect[2] // 2, self.y + 26))

class card(object):
    def __init__(self, x, y, pos_x, pos_y, image):
        self.x = x
        self.y = y
        self.pos_x = pos_x
        self.pos_y = pos_y
        #self.width = 54
        #self.height = 72
        self.width = 72
        self.height = 96
        self.vel = 10
        self.IsCommunity = False
        self.IsPlayer = False
        self.IsVisible = False
        self.IsSetPos = False
        self.img = image

    def set_image(self, image):
        self.img = image

    def set_pos(self, x, y, pos_x, pos_y):
        self.x = x
        self.y = y
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_pos(self):
        return (self.x, self.y, self.pos_x, self.pos_y)

    def set_visible(self, bVisible):
        self.IsVisible = bVisible

    def set_player_card(self, bPlayer):
        self.IsPlayer = bPlayer

        if not self.IsSetPos:
            self.set_pos(self.x - 15, self.y, self.pos_x - 15, self.pos_y)

        self.IsSetPos = True

    def draw(self, win):
        if self.IsVisible:
            if self.y > self.pos_y:
                self.vel = 0
            
            self.y += self.vel

            win.blit(self.img, (self.x, self.y))

class bet_ready(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4
        self.IsVisible = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_visible(self, bVisible):
        self.IsVisible = bVisible

    def draw(self, win):
        if self.IsVisible:
            font = pygame.font.SysFont('comic sans MS', 20)
            text = font.render('Ready', True, (255, 255, 255))
            win.blit(text, (self.x, self.y))

class bet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4
        self.bet_amount = 0
        self.bet_type = ''
        self.IsVisible = False

    def set_bet(self, bet_type, bet_amount):
        self.bet_type = bet_type
        self.bet_amount = bet_amount

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_visible(self, bVisible):
        self.IsVisible = bVisible

    def draw(self, win):
        if self.IsVisible:
            bet_str = ''
            bet_color = (233, 233, 233)

            if self.bet_type == 'Raise' or self.bet_type == 'Call' or self.bet_type == 'AllIn':
                bet_str = self.bet_type + ', ' + str(self.bet_amount)
            elif self.bet_type == 'Fold':
                bet_str = self.bet_type
                bet_color = (255, 0, 0)
            elif self.bet_type == 'Check':
                bet_str = self.bet_type
                bet_color = (255, 255, 60)
            else:
                bet_str = "Wrong Bet"

            font = pygame.font.SysFont('comic sans MS', 22)
            text = font.render(bet_str, True, bet_color)
            win.blit(text, (self.x, self.y))


class text(object):
    def __init__(self, x, y, text_str, size, color = (0, 0, 0), font='consolas'):
        self.x = x
        self.y = y
        self.vel = 5
        self.size = size
        self.color = color
        self.font = font
        self.text_str = text_str
        self.IsVisible = False

    def set_visible(self, bVisible):
        self.IsVisible = bVisible

    def set_text(self, text):
        self.text_str = text

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        if self.IsVisible:
            font = pygame.font.SysFont(self.font, self.size)
            text_obj = font.render(self.text_str, True, self.color)
            win.blit(text_obj, (self.x, self.y))


class chip(object):
    def __init__(self, text, x, y, radius, arc_radius, pos_y, screen_width, screen_height, color, color_border, text_color):
        self.text = text
        self.x = x
        self.y = y
        self.radius = radius
        self.arc_radius = arc_radius
        self.circle_width = 4
        self.arc_width = 4
        self.screen_width = screen_width
        self.screen_height = screen_height        
        self.pos_y = pos_y        
        self.del_theta = 0
        self.vel = 6
        self.color = color
        self.color_border = color_border
        self.text_color = text_color
        self.IsVisible = False
        
    def rotate(self, text, rect, angle):
        """Rotate the text while keeping its center."""
        # Rotate the original image without modifying it.
        new_text = pygame.transform.rotate(text, angle)
        # Get a new rect with the center of the old rect.
        rect = new_text.get_rect(center=rect.center)
        return new_text, rect

    def set_visible(self, bIsVisible):
        self.IsVisible = bIsVisible

    def set_text(self, text):
        self.text = text
    
    def set_pos(self, x, y, pos_y):
        self.x = x
        self.y = y
        self.pos_y = pos_y
        self.vel = 6
        self.del_theta = 0
    
    def draw(self, win):
        if self.IsVisible:
            if (self.screen_height //2 > self.pos_y and self.y > self.pos_y) or (self.screen_height //2 < self.pos_y and self.y < self.pos_y):
                self.vel= 0
                
            if self.x < self.screen_width //2:
                facing_x = 1
            else:
                facing_x = -1
            
            if self.y < self.screen_height //2:
                facing_y = 1
            else:
                facing_y = -1
            
            self.x += round(facing_x * 0.45 * (self.vel ** 2))
            self.y += facing_y * self.vel
            self.del_theta += self.vel / 30
            
            #rect = [100, 100, 100, 100]
            pygame.draw.circle(win, (220, 220, 220), (self.x,self.y), self.radius+self.circle_width - 3, 0)
            pygame.draw.circle(win, self.color_border, (self.x,self.y), self.radius+self.circle_width - 3, self.circle_width//2)
            rect = pygame.draw.circle(win, self.color, (self.x,self.y), self.radius, self.circle_width)
            pygame.draw.circle(win, self.color_border, (self.x,self.y), self.radius-self.circle_width, self.circle_width//2 - 1)
            
            rect_arc = (rect[0] + self.radius - self.arc_radius,
                        rect[1] + self.radius - self.arc_radius,
                        2 * self.arc_radius,
                        2 * self.arc_radius)
            
            #pygame.draw.circle(win, self.color, (self.x,self.y), 10, self.circle_width)
            pygame.draw.arc(win, self.color, rect_arc, 0 + self.del_theta, 1/5*pi + self.del_theta, self.arc_width)
            pygame.draw.arc(win, self.color, rect_arc, 2/5*pi + self.del_theta, 3/5*pi + self.del_theta, self.arc_width)
            pygame.draw.arc(win, self.color, rect_arc, 4/5*pi + self.del_theta, 5/5*pi + self.del_theta, self.arc_width)
            pygame.draw.arc(win, self.color, rect_arc, 6/5*pi + self.del_theta, 7/5*pi + self.del_theta, self.arc_width)
            pygame.draw.arc(win, self.color, rect_arc, 8/5*pi + self.del_theta, 9/5*pi + self.del_theta, self.arc_width)
            
            # text rotation while preserving center pos
            font = pygame.font.SysFont('comic sans MS', 17, True)
            text = font.render(self.text, True, self.text_color)
            rect = text.get_rect(center=(self.x, self.y))
            text, rect = self.rotate(text, rect, self.del_theta * 90/pi)
            win.blit(text, rect)

class arrow(object):
    def __init__(self, x, y, W, direction, color):
        self.x = x
        self.y = y
        self.W = W
        self.direction = direction
        self.color = color
        self.IsVisible = False
    
    def set_visible(self, bIsVisible):
        self.IsVisible = bIsVisible

    def toggle_visible(self):
        if self.IsVisible:
            self.IsVisible = False
        else:
            self.IsVisible = True
        
    def draw(self, win):
        if self.IsVisible:
            pygame.draw.rect(win, self.color, (self.x, self.y + self.W * 0.25, self.W * 0.4, self.W * 0.5))
            pygame.draw.polygon(win, self.color, [[self.x + self.W * 0.4, self.y], 
                                                  [self.x + self.W, self.y + self.W * 0.5], 
                                                  [self.x + self.W * 0.4, self.y + self.W]], 0)

class btn(object):
    def __init__(self, text, x, y, radius, color_outer, color_inner, color_inner_mdown, text_color):
        self.text = text
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 2
        self.timer = 0
        self.color_outer = color_outer
        self.color_inner = color_inner
        self.color_inner_mdown = color_inner_mdown
        self.text_color = text_color
        self.IsVisible = False
        self.IsMouseDown = False
        self.Dir = 1
        
    def is_equal(self, text):
        return self.text == text
        
    def set_ismousedown(self, bMDown):
        self.IsMouseDown = bMDown

    def toggle_ismousedown(self):
        if self.IsMouseDown:
            self.IsMouseDown = False
        else:
            self.IsMouseDown = True

    def toggle_visible(self):
        if self.IsVisible:
            self.set_visible(False)
        else:
            self.set_visible(True)
    
    def set_visible(self, bIsVisible):
        self.IsVisible = bIsVisible

    def calc_dist(self, pos1, pos2):
        return sqrt((pos1[0] - pos2[0]) **2 + (pos1[1] - pos2[1]) **2)
        
    def inside_pos(self, pos):
        dist = self.calc_dist((self.x, self.y), pos)
        
        if dist <= self.radius:
            return True
        else:
            return False
        
        
    def draw(self, win):
        if self.IsVisible:
            # self.timer += self.vel * self.Dir
            
            # if self.timer > 50 or self.timer <= 0:
            #     self.toggle_ismousedown()
            #     self.Dir *= -1    

            pygame.draw.circle(win, (215, 215, 215), (self.x,self.y), self.radius + 2, 1)
            pygame.draw.circle(win, self.color_outer, (self.x,self.y), self.radius, 6)
            pygame.draw.circle(win, (96, 96, 96), (self.x,self.y), self.radius - 6, 1)
            
            if self.IsMouseDown:
                pygame.draw.circle(win, self.color_inner_mdown, (self.x,self.y), self.radius - 7, 0)
                
            else:
                pygame.draw.circle(win, self.color_inner, (self.x,self.y), self.radius - 7, 0)
            
            
            # text rotation while preserving center pos
            font = pygame.font.SysFont('comic sans MS', 16)
            text = font.render(self.text, True, self.text_color)
            new_rect = text.get_rect(center=(self.x, self.y))
            win.blit(text, new_rect)


class winner_result(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4
        self.result_text = ''
        self.result_card_imgs = []
        self.IsVisible = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def set_card_imgs(self, img_list):
        self.result_card_imgs = img_list

    def set_result_text(self, result_text):
        self.result_text = result_text

    def set_visible(self, bVisible):
        self.IsVisible = bVisible

    def draw(self, win):
        if self.IsVisible:
            result_color = (255, 255, 255)

            # draw rect
            pygame.draw.rect(win, (130,124,102), (self.x - 5, self.y - 3 , 340, 140), 0)

            # draw result text
            font = pygame.font.SysFont('comic sans MS', 20)
            text = font.render(self.result_text, True, result_color)
            win.blit(text, (self.x, self.y))

            # draw result cards
            for idx in range(len(self.result_card_imgs)):
                win.blit(self.result_card_imgs[idx], (self.x + 60 * (idx), self.y + 32))


class winner_quit_result(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4
        self.result_text = ''
        self.IsVisible = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def set_result_text(self, result_text):
        self.result_text = result_text

    def set_visible(self, bVisible):
        self.IsVisible = bVisible

    def draw(self, win):
        if self.IsVisible:
            result_color = (255, 255, 255)

            # draw rect
            pygame.draw.rect(win, (130,100,80), (self.x - 5, self.y - 3 , 330, 50), 0)

            # draw result text
            font = pygame.font.SysFont('comic sans MS', 20)
            text = font.render(self.result_text, True, result_color)
            win.blit(text, (self.x, self.y))


class btn2(object):
    def __init__(self, text1, text2, x, y, radius, color_outer, color_inner, color_inner_mdown, text_color):
        self.text1 = text1
        self.text2 = text2
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 2
        self.timer = 0
        self.color_outer = color_outer
        self.color_inner = color_inner
        self.color_inner_mdown = color_inner_mdown
        self.text_color = text_color
        self.IsVisible = False
        self.IsMouseDown = False
        
    def set_ismousedown(self, bMDown):
        self.IsMouseDown = bMDown
    
    def set_visible(self, bIsVisible):
        self.IsVisible = bIsVisible

    def calc_dist(self, pos1, pos2):
        return sqrt((pos1[0] - pos2[0]) **2 + (pos1[1] - pos2[1]) **2)
        
    def inside_pos(self, pos):
        dist = self.calc_dist((self.x, self.y), pos)
        
        if dist <= self.radius:
            return True
        else:
            return False
        
        
    def draw(self, win):
        if self.IsVisible:
            pygame.draw.circle(win, pygame.Color('LIGHTGRAY'), (self.x,self.y), self.radius + 2, 1)
            pygame.draw.circle(win, self.color_outer, (self.x,self.y), self.radius, 6)
            pygame.draw.circle(win, pygame.Color('DARKGRAY'), (self.x,self.y), self.radius - 6, 1)
            
            if self.IsMouseDown:
                pygame.draw.circle(win, self.color_inner_mdown, (self.x,self.y), self.radius - 7, 0)
                
            else:
                pygame.draw.circle(win, self.color_inner, (self.x,self.y), self.radius - 7, 0)
            
            
            # text rotation while preserving center pos
            font = pygame.font.SysFont('comic sans MS', 16)
            text1 = font.render(self.text1, True, self.text_color)
            text2 = font.render(self.text2, True, self.text_color)
            new_rect = text1.get_rect(center=(self.x, self.y-10))
            win.blit(text1, new_rect)
            new_rect = text2.get_rect(center=(self.x, self.y+10))
            win.blit(text2, new_rect)
