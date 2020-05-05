# -*- coding: utf-8 -*-

import random
import datetime
import os
import time

class Player :
    
    keyboard_key = {'z':(-1,0),
                    'q':(0,-1),
                    's':(1,0),
                    'd':(0,1)}
    
    def __init__(self, name, points = 0, start = (0,0)):
        self.name = name
        self.points = points
        self.position = start
    
    def move (self) :
        global modeDeJeu, size
        self.traverse=0
        self.bloque=0
        if modeDeJeu == 'T' or modeDeJeu == 't':
            self.traverse=1
        elif modeDeJeu == 'B' or modeDeJeu == 'b':
            self.bloque=1
        #Afficher les points
        print("score =", self.points)

        key = input("Mouvement (z,q,s,d) : ")
        while key not in Player.keyboard_key.keys() :
            key = input("Mouvement (z,q,s,d) : ")

        #Nettoie l'écran powershell ou cmd
        os.system('cls')

        move = Player.keyboard_key[key]
        self.position = (self.position[0] + move[0], self.position[1] + move[1])

        
        if self.traverse:
            #Si trop à droite -> Tout à gauche
            if self.position[1] == size :
                self.position = (self.position[0],0)
            #Si trop à gauche -> Tout à droite    
            elif self.position[1] == -1:
                self.position = (self.position[0], (size-1))
            #Si trop en haut -> Tout en bas   
            elif self.position[0] == -1:
                self.position = ((size-1), self.position[1])
             #Si trop en bas -> Tout en haut    
            elif self.position[0] == size:
                self.position = (0, self.position[1])


                
        if self.bloque:
            #Si trop à droite -> reste à droite
            if self.position[1] == size :
                self.position = (self.position[0], (size-1))
            #Si trop à gauche -> reste à gauche   
            elif self.position[1] == -1:
                self.position = (self.position[0], 0)
            #Si trop en haut -> reste en haut   
            elif self.position[0] == -1:
                self.position = (0, self.position[1])
             #Si trop en bas -> reste en bas    
            elif self.position[0] == size:
                self.position = ((size-1), self.position[1])
            
        
    

class Game :
    
    def __init__(self, player):
        global size, modeDeJeu, PlayerForme, NombreCoups, nomJoueur

        
        #déterminer le nom du joueur
        nomJoueur = input("Quel est votre pseudo ? : ")

        
        #déterminer la taille
        size = 0
        while size < 5:
            size = int(input("Quelle taille de plateau désirez-vous ? 5 est le minimum : "))

        #déterminer le mode de jeu
        modeDeJeu = ''
        while modeDeJeu != 'T' and modeDeJeu != 'B' and modeDeJeu != 't' and modeDeJeu != 'b':
            modeDeJeu = input("T pour traverser les murs, B pour bloquer : ")

        #déterminer la forme du joueur
        PlayerForme = ''
        while len(PlayerForme)!=1 or PlayerForme == '*':
            PlayerForme = input("Quelle est la forme désiré du joueur ? Un seul caractère, pas de * : ")
            
        self.player = player
        self.board_size = size
        self.candies = []
        
    # Dessine le plateau
    def draw(self):
        global PlayerForme
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) in self.candies :
                    print("*",end=" ")
                elif (line,col) == self.player.position :
                    print(PlayerForme, end=" ")
                else : 
                    print(".",end=" ")
            print()
            
    # Fait apparaitre un bonbon
    def pop_candy(self):
        new_candy = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if new_candy not in self.candies :
            self.candies.append(new_candy)
            
    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self):
        if self.player.position in self.candies:
            self.player.points += 1
            self.candies.remove(self.player.position)
    
        
        
    # Joue une partie complète
    def play(self):
        global modeDeJeu, size, score, nomJoueur, PlayerForme
        
        #self.retry = ''
        #while self.retry != 'p' and self.retry != 'P':
        #   if self.retry == 'R' or self.retry == 'r':
        #        score = 0
        #        self.player
        #    self.retry =''
        print("--- Début de la partie ---")

                
        self.draw()
            
        end = Game.end_time(1,30)
        now = datetime.datetime.today()
            
        while now < end: 
            self.player.move()
            self.check_candy()
                
            if random.randint(1,3) == 1 :
                self.pop_candy()
                    
            self.draw()
                
            now = datetime.datetime.today()
        print("----- Terminé -----")
        print("Vous avez", self.player.points, "points \n" )
        print("TopScore:")


        ScoresMax = open("highScores.txt", "a")
        self.scoreText = nomJoueur + " : " + str(self.player.points) + " points, avec une grille de " + str(size) + " sur " + str(size) + " dans le mode de jeu " + modeDeJeu + ", son avatar était un " + PlayerForme + "\n"
        ScoresMax.write(self.scoreText)
        ScoresMax.close()
        
            #Pause pour voir les points
        time.sleep(2)
            
            #retry est complexe
            #while self.retry != 'r' and self.retry != 'R' and self.retry != 'P' and self.retry != 'p':
            #    self.retry = input("R pour recommencer P pour partir : ")
            
                
        os.system("pause")
  
        


    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end
        



if __name__ == "__main__" :
     
    p = Player("Moi")
    g = Game(p)
    g.play()

    
    
    
