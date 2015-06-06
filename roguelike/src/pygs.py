# -*- coding: utf-8 -*-
"""
main app
"""

import pygame
import pygame.locals as LOC
import os
import math
from characters import *
from maps import Map
from aux1 import Aux
from music import Music


class App(object):
    """ doc """
    def execute(self):
        """ s """
        self.init()

        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.turn()
            self.render()
        # self.cleanup()

    def __init__(self):
        """ s """
        self._running = True
        self._surface = None
        self._size = self.weight, self.height = 810, 650
        self._map = Map(50, (10, 10))  #rmnum, rsize
        self._player_turn = True
        self._hero = None
        # self._active_enemy = []
        self._display_surf = None
        self._image_library = None
        self._action = None
        self._marked = (None, None)

        self.aux = Aux()
        self.mus = Music()

    def init(self):
        """ s """
        pygame.init()
        pygame.display.set_caption('Rogal')
        self._surface = pygame.display.set_mode(self._size)
        self._running = True
        self._display_surf = pygame.display.set_mode(self._size,
                                                     pygame.HWSURFACE)
        self.load_images()
        self.mus.load_music()
        self.mus.play_music()

        _map_size = self._map.get_size()

        #może jakiś inny sposób ustalania współrzędnych?!

        pos_x = _map_size[0]/2
        pos_y = _map_size[1]/2
        #Create Hero
        self._hero = Hero(0, 0, 1, 1,
                          Damage(1.0, 1.0, 15, 10),
                          Armor(0.0, 0),
                          100, pos_x, pos_y)

        self.aux.do_nice_outlines(self._surface)
        pygame.key.set_repeat(5, 50)  #(delay, interval) in milisec

        self.aux.write(self._surface, "EQ", 22, 700, 0)
        self.aux.write(self._surface, "Stats:", 14, 615, 240+20)
        self.aux.write(self._surface, "HP", 14, 615, 240+35)  # +15 pix pionowo
        self.aux.write(self._surface, "Attack", 14, 615, 240+50)
        self.aux.write(self._surface, "Defense", 14, 615, 240+65)
        self.aux.write(self._surface, "Armor", 14, 615, 240+80)

    def event(self, event):
        """ to do, soon"""
        #alternative?
        # pressedkeys = pygame.key.get_pressed()
        # if pressedkeys[pygame.K_x]:

        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if self._player_turn:
                if event.key == LOC.K_UP or event.key == LOC.K_w:
                    if self._hero.get_y() > 0\
                            and self._map[self._hero.get_x(), self._hero.get_y()-1][0] != '_'\
                            and self._map[self._hero.get_x(), self._hero.get_y()-1][0] != 'w':
                        self._action ='w'
                        self._player_turn = False
                if event.key == LOC.K_DOWN or event.key == LOC.K_s:
                    if self._hero.get_y() < self._map.size[1]-1\
                            and self._map[self._hero.get_x(), self._hero.get_y()+1][0] != '_'\
                            and self._map[self._hero.get_x(), self._hero.get_y()+1][0] != 'w':
                        self._action = 's'
                        self._player_turn = False
                if event.key == LOC.K_LEFT or event.key == LOC.K_a:
                    if self._hero.get_x() > 0\
                            and self._map[self._hero.get_x()-1, self._hero.get_y()][0] != '_'\
                            and self._map[self._hero.get_x()-1, self._hero.get_y()][0] != 'w':
                        self._action = 'a'
                        self._player_turn = False
                if event.key == LOC.K_RIGHT or event.key == LOC.K_d:
                    if self._hero.get_x() < self._map.size[0]-1\
                            and self._map[self._hero.get_x()+1, self._hero.get_y()][0] != '_'\
                            and self._map[self._hero.get_x()+1, self._hero.get_y()][0] != 'w':
                        self._action = 'd'
                        self._player_turn = False

            if event.key == LOC.K_ESCAPE:  #quit
                self._running = False
            if event.key == LOC.K_m:  #volume up
                if self.mus.volume <= 1:
                    self.mus.volume += 0.05
                    pygame.mixer.music.set_volume(self.mus.volume)
            if event.key == LOC.K_n:  #volume down
                if self.mus.volume >= 0:
                    self.mus.volume -= 0.05
                    pygame.mixer.music.set_volume(self.mus.volume)

        if event.type == pygame.USEREVENT + 1:
            print(self.aux.song_num, "song ended")
            self.aux.play_music()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                (po_x, po_y) = pygame.mouse.get_pos()
                #mouse pointer in the equipment zone
                if po_x >= 610 and po_y >= 20 and po_y <= 20+6*40:
                    (square_x, square_y) = ((po_x-610)/40, (po_y-20)/40)
                    if not self._marked == (square_x, square_y): 
                        # if not already marked
                        self._marked = (square_x, square_y)
                    else:
                        #swap item with wearing
                        pass

    def render(self):
        """ in prog """
        _boczne_pola = (19-1)/2  # powinno byc 9
        if self._hero.get_x() < _boczne_pola:
            x_o = 0
        elif self._hero.get_x() > self._map.size[0]-_boczne_pola-1:
            x_o = self._map.size[0] - (2*_boczne_pola+1)  #2*_boczne_pola+1 = 19
        else:
            x_o = self._hero.get_x() - _boczne_pola
        if self._hero.get_y() < _boczne_pola:
            y_o = 0
        elif self._hero.get_y() > self._map.size[1]-_boczne_pola-1:
            y_o = self._map.size[1] - (2*_boczne_pola+1)
        else:
            y_o = self._hero.get_y() - _boczne_pola
        for y in xrange(19):
            for x in xrange(19):
                if self._map[(x_o+x), (y_o+y)][0] == 'w': #ściana
                    self._display_surf.blit(self._image_library["texture17.png"],
                                            (x * 32, y * 32))
                elif self._map[(x_o+x), (y_o+y)][0] != '_':  # podloga
                    pygame.draw.rect(self._surface, ((self._map[(x_o+x),(y_o+y)][0]*64)%256, 100, (self._map[(x_o+x),(y_o+y)][0]*32)%256), 
                    (x * 32, y * 32, 32, 32))
                    #self._display_surf.blit(self._image_library["texture18.png"],
                    #                        (x * 32, y * 32))
                else:  # pustka - nie sciana
                    # self._display_surf.blit(self.wall, (x * 32, y * 32))
                    pygame.draw.rect(self._surface, (0, 0, 0),
                                     (x * 32, y * 32, 32, 32))
                #hero
                if (x_o+x, y_o+y) == self._hero.get_position():
                    self._display_surf.blit(self._image_library["photo.jpg"],
                                            (x * 32, y * 32))
                #enemy
                if self._map[(x_o+x), (y_o+y)][2] is not None:
                    self._display_surf.blit(self._image_library["enemy1.png"],
                                            (x * 32, y * 32))

                #vision
                if not self.check_horizon(x_o+x, y_o+y):
                    # (abs(x_o+x - self._posx) <= self._horizon
                    # and abs(y_o+y - self._posy) <= self._horizon):
                    self._display_surf.blit(self._image_library["black.png"],
                                            (x * 32, y * 32))

        #volume visual
        self._display_surf.blit(self._image_library["speaker.png"], (0, 612))
        light_straps = (0, 96, 0)
        dark_straps = (0, 32, 0)
        wid = 5

        for strap in xrange(20):
            if strap < self.mus.volume*20:
                pygame.draw.rect(self._surface, light_straps,
                                 (20+strap*wid, 650-strap*2, wid-1, strap*2))
            else:
                pygame.draw.rect(self._surface, dark_straps,
                                 (20+strap*wid, 650-strap*2, wid-1, strap*2))
        pygame.display.update()

        # napisy
        self.aux.write(self._surface, str(self._hero._hp), 14, 675, 240+35)
        self.aux.write(self._surface, str(self._hero._attack), 14, 675, 240+50)
        self.aux.write(self._surface, str(self._hero._defense), 14, 675, 240+65)
        self.aux.write(self._surface, str(self._hero._armor), 14, 675, 240+80)

    def check_horizon(self, polex, poley):  # ceil(sqrt(Dx^2+Dy^2))
        horizon = 4
        d = math.ceil(math.sqrt((self._hero.get_x()-polex)**2 + (self._hero.get_y()-poley)**2))
        return d <= horizon

    def load_images(self):
        """ load images from /items """
        path = r"./items/"
        item_list = self.aux.files("items")
        self._image_library = {}

        for item in item_list:
            uni_path = path.replace('/', os.sep).replace('\\', os.sep)
            #universal path, also works: os.path.join('','')
            self._image_library[item] = pygame.image.load(uni_path + item)\
                .convert_alpha()

    def turn(self):
        """
        who moves 
        -and what the hell is with that if? I dont understand it @SMN
        """
        if self._player_turn:
            #przechwyc event
            pass
        else:
            #wykonaj przechwycona akcje
            self.player_action()
            self.enemy_turn()

    def player_action(self):
        """ execute what player did in his turn """
        if self._action == 'w':
            if self._map[self._hero.get_x(), self._hero.get_y()-1][2] is None: #brak wroga
                self._hero.change_y(-1)
            else:    
                self._hero.attack(self._map[self._hero.get_x(), self._hero.get_y()-1][2]) #atak
        if self._action == 's':
            if self._map[self._hero.get_x(), self._hero.get_y()+1][2] is None:
                self._hero.change_y(1)
            else:    
                self._hero.attack(self._map[self._hero.get_x(), self._hero.get_y()+1][2])
        if self._action == 'a':
            if self._map[self._hero.get_x()-1, self._hero.get_y()][2] is None:
                self._hero.change_x(-1)
            else:    
                self._hero.attack(self._map[self._hero.get_x()-1, self._hero.get_y()][2])
        if self._action == 'd':
            if self._map[self._hero.get_x()+1, self._hero.get_y()][2] is None:
                self._hero.change_x(1)
            else:    
                self._hero.attack(self._map[self._hero.get_x()+1, self._hero.get_y()][2])

    def enemy_turn(self):
        """ move enemies """
        #przeciwnicy w zasiegu wzroku
        horizon = 4
        enemy_list = []
        for i in xrange(-horizon, horizon):  #from -3 to 3
        #no nie, nie sprawdzałeś czy nie jestesś za blisko krawędzi mapy @SMN
        #dodalem sprawdzanie
            for j in xrange(-horizon, horizon):
                # nie puste pole
                if not (not (self._hero.get_x() + i >= 0) or not (self._hero.get_x() + j >= 0) or not (
                        self._hero.get_x() + i < self._map.size[0]) or not (self._hero.get_y() + j < self._map.size[1])
                        or not (self._map[(self._hero.get_x() + i), (self._hero.get_y() + j)][2] is not None)):
                    enemy_list.append(self._map[(self._hero.get_x()+i),
                                                 (self._hero.get_y()+j)][2])
        print "w poblizu mamy: ", enemy_list

        for enemy in enemy_list:
            x_enemy, y_enemy = enemy.get_position()
            # będziemy poruszać się po współrzędnych,
            # na których jest większa odległość póki co...
            x_distance = self._hero.get_x() - x_enemy
            y_distance = self._hero.get_y() - y_enemy
            if abs(x_distance) > abs(y_distance):
                if x_distance > 1:
                    enemy.change_position((x_enemy+1, y_enemy))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy+1, y_enemy][2] = enemy
                elif x_distance < -1:
                    enemy.change_position((x_enemy-1, y_enemy))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy-1, y_enemy][2] = enemy
            else:
                if y_distance > 1:
                    enemy.change_position((x_enemy, y_enemy+1))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy, y_enemy+1][2] = enemy
                elif y_distance < -1:
                    enemy.change_position((x_enemy, y_enemy-1))
                    self._map[x_enemy, y_enemy][2] = None
                    self._map[x_enemy, y_enemy-1][2] = enemy

        self._player_turn = True


if __name__ == '__main__':
    __TheApp__ = App()
    __TheApp__.execute()