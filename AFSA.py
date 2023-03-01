import numpy as np
from random import random, uniform, randint
from math import sqrt

from Fish import Fish, FishSet
from Food import Food, FoodSet

class AFSA:
    def __init__(self, game, Nf, N, Vd=80, delta=0.5, step=7, max_step=5):
        self.game = game
        self._N  = N
        self._Nf = Nf
        self._Vd = Vd
        self._delta = delta
        self._step = step
        self._l  = max_step
        self.fish_set = FishSet(game, AFSA.generate_pop(N, game))
        self.food_set = FoodSet(game, AFSA.generate_foods(Nf, game))

    def add_food(self):
        width, height = self.game.screen.get_size()
        food = Food(randint(0, width-10), randint(0, height-10), self.game)
        self.food_set._load_pieces([food])
        return food

    def generate_pop(N, game):
        width, height = game.screen.get_size()
        return [Fish(randint(0, width-15), randint(0, height-20), game) for i in range(N)]

    def generate_foods(N, game):
        width, height = game.screen.get_size()
        return [Food(randint(0, width-10), randint(0, height-10), game) for i in range(N)]

    def euclidean(a, b, x, y):
        return sqrt((a-x)**2 + (b-y)**2)

    def get_food_concentration(self, x, y, v):
        qtd = 0
        for food in self.food_set.pieces:
            fx, fy = food.X, food.Y
            if AFSA.euclidean(x, y, fx, fy) <= v:
                qtd+=1
        return qtd/self._Nf
    
    def get_fish_concentration(self, x, y, v):
        qtd = 0
        for fish in self.fish_set.pieces:
            fx, fy = fish.S
            euclidean = AFSA.euclidean(x, y, fx, fy)
            if euclidean <= v and euclidean > 0:
                qtd+=1
        return qtd/self._N
    
    def get_ds_random_in_vision(self):
        return np.array([ int(uniform(-1, 1)*self._Vd), int(uniform(-1, 1)*self._Vd) ])

    def random_move(self, fish: Fish):
        return np.int_(np.array([uniform(-1, 1)*self._step, uniform(-1, 1)*self._step]))

    def prey(self, fish: Fish):
        dS = y = None

        alterado = False
        for _ in range(self._l):
            cf = fish.S
            Xj = cf + self.get_ds_random_in_vision()
            yj = self.get_food_concentration(Xj[0], Xj[1], self._Vd)
            yf = self.get_food_concentration(cf[0], cf[1], self._Vd)
            delta = self.get_fish_concentration(Xj[0], Xj[1], self._Vd)
            
            if yj > yf and delta <= self._delta:
                dif = Xj-cf
                mod = sqrt(dif[0]**2 + dif[1]**2)
                if mod!=0:
                    norma = dif / mod
                    dS = np.int_(norma*self._step*random())
                    alterado = True
                    y = yj
            if alterado: break
        if alterado==False:
            dS = self.random_move(fish)

        return dS, y
    
    def get_best_fish_in_vision(self, fish: Fish):
        best_fish = None
        for fish_j in self.fish_set.pieces:
            if fish_j == fish: continue

            fx, fy = fish_j.S
            x, y = fish.S
            fd_cont = self.get_food_concentration(fx, fy, self._Vd)
            fs_cont = self.get_fish_concentration(fx, fy, self._Vd)

            euclidean = AFSA.euclidean(x, y, fx, fy)
            if euclidean <= self._Vd and euclidean > 0:
                if best_fish==None or (best_fish[1] > fd_cont and fs_cont <= self._delta):
                    best_fish = (fish, fd_cont)
        return best_fish
    
    def follow(self, fish: Fish):
        dS = y = None

        alterado = False
        fd_concentration = self.get_food_concentration(fish.S[0], fish.S[1], self._Vd)
        best_fish = self.get_best_fish_in_vision(fish)
        if best_fish!=None and best_fish[1] > fd_concentration:
            dif = best_fish[0].S-fish.S
            mod = sqrt(dif[0]**2 + dif[1]**2)
            if mod!=0:
                norma = dif / mod
                dS = np.int_(norma*self._step*random())
                alterado = True
                y = best_fish[1]
        if alterado==False:
            dS, y = self.prey(fish)

        return dS, y

    def get_sc(self, fish: Fish):
        qtd=0
        xm = fish.S[0]
        ym = fish.S[1]
        for fj in self.fish_set.pieces:
            if fj==fish: continue
            if AFSA.euclidean(fj.S[0], fj.S[1], fish.S[0], fish.S[1]) < self._Vd:
                qtd+=1
                xm += fj.S[0]
                ym += fj.S[1]

        return np.array([xm, ym])/qtd if qtd>0 else np.array([])

    def swarm(self, fish: Fish):
        dS = y = None

        alterado = False
        food_concentration = self.get_food_concentration(fish.S[0], fish.S[1], self._Vd)

        sc = self.get_sc(fish)
        if sc.size:
            foodc_concentration = self.get_food_concentration(sc[0], sc[1], self._Vd)
            fishc_concentration = self.get_fish_concentration(sc[0], sc[1], self._Vd)
        if sc.size and fishc_concentration <= self._delta and foodc_concentration > food_concentration:
            dif = sc-fish.S
            mod = sqrt(dif[0]**2 + dif[1]**2)
            if mod!=0:
                norma = dif / mod
                dS = np.int_(norma*self._step*random())
                alterado = True
                y = foodc_concentration
        if alterado==False:
            dS, y = self.prey(fish)

        return dS, y

    def move(self):
        for fish in self.fish_set.pieces:
            dS = 0
            prey, y_prey = self.prey(fish)
            swarm, y_swarm = self.swarm(fish)
            follow, y_follow = self.follow(fish)

            if y_follow != None and (y_swarm==None or y_follow >= y_swarm):
                dS = follow
            elif y_swarm!=None and (y_follow==None or y_swarm >= y_follow):
                dS = swarm
            else:
                dS = prey

            fish.move(dS)
