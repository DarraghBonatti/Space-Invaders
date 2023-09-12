import sys, pygame , math
import time
import os 



#########################--- MyGame Class / pygame init / init function   ---####################################
class MyGame():

    def __init__(self):
        
        pygame.init()


#########################--- All Game Variables   ---####################################

        self._size = self._width, self._height = 450,700
        self._background =pygame.transform.scale(pygame.image.load(os.path.join("background-black.png")), (self._width, self._height)) 
        self._screen = pygame.display.set_mode(self._size)
        self._rocketship = pygame.image.load("pixel_ship_red_small.png")
        self._enemieview = pygame.image.load("pixel_ship_blue_small.png")
        self._specialenemieview = pygame.image.load("pixel_ship_green_small.png")

        self._ship = RocketShip(self._width/2, 650, self._width, 2)
        self._enemieShip = EnemieShip(20, 20 , self._width , 1)
        self._missileList = []
        self._xPos = self._width//5
        self._yPos = 20
        self._move = False
      



#########################--- Game running function  ---####################################

    def rungame(self):
        enemies = []
        
        vel = 2
        score_font = pygame.font.SysFont("Verdana", 50)
        score = 0 
        speed = .5
        specialspeed = 1
        

        
#########################--- Application Loop, Quit Clause  ---####################################
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:

#########################--- Missile creation  ---####################################

                    if event.key == pygame.K_SPACE:
                        missile = Missile(self._ship.getXPos())
                        self._missileList.append(missile)

#########################--- Player movement ---####################################

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self._ship._xPos - vel > 0: # left
                self._ship._xPos -= vel
            if keys[pygame.K_RIGHT] and self._ship._xPos + vel + 75 < self._width: # right
                self._ship._xPos += vel
#########################--- Draw player and background---####################################
            
            self._screen.blit(self._background, (0,0))
            self._screen.blit(self._rocketship, (self._ship.getXPos(), self._ship.getYPos()))


#########################--- Draw enemies, Make enemie list---####################################
            if len(enemies) == 0:
                speed += .3
                for i in range(6):
                    x_inc = 75
                    enemy = EnemieShip(x_inc*i, 40, self._width , speed)
                    enemies.append(enemy)
#########################--- Draw Special Enemy---####################################
         
            if score ==  50 or score == 120 or score == 250:
       
                special_enemy =  EnemieShip(-100, 0, self._width , specialspeed)  
                self._move = True
            if self._move:
                special_enemy.specialdraw(self._screen)
                special_enemy.specialmove() 
                for i in self._missileList:
                
                        if i.isCollidingWith(special_enemy):
                        
                           pygame.quit()

#########################--- Draw/Move Enemies + if statement for game loss---####################################
            for enemy in enemies:
                enemy.draw(self._screen)
                enemy.moveEnemie()
                
                if enemy._yPos >= self._height:
                    pygame.quit()
                

#########################--- Draw and Move Missiles  ---####################################

            i = 0
            while i < len(self._missileList):
                self._missileList[i].moveMissile()
                self._screen.blit(self._missileList[i].getIcon(), (self._missileList[i].getXPos(), self._missileList[i].getYPos()))
                i += 1




#########################--- Collision Check / Remove Enemy if True  ---####################################
            for i in self._missileList:
                for j in enemies:
                    if i.isCollidingWith(j):
                        enemies.remove(j)
                        score +=5
                        

#########################--- Draw Scoreboard  ---####################################

            live_score = score_font.render(f"score: {score}", 1, (255,255,255))
            self._screen.blit(live_score, (10, 10))
  
            pygame.display.flip()

#########################--- Rocket Ship Class and Basic Methods  ---####################################

class RocketShip(MyGame):
    def __init__(self, xpos, ypos, maxxpos, change):
        self._xPos = xpos
        self._yPos = ypos
        self._maxXPos = maxxpos
        self._ballchange = change
    def getXPos(self):
        return self._xPos
    def getYPos(self):
        return self._yPos
    def handleMoveRight(self):
        
        if self._xPos + self._ballchange < self._maxXPos:
            self._xPos += self._ballchange
    def handleMoveLeft(self):
       
        if self._xPos - self._ballchange > 0:
            self._xPos -= self._ballchange

    

    def handleStopMove(self):
        
        self._xPos = self._xPos

    def draw(self , window):
        window.blit("pixel_ship_red_small.png", (self.x, self.y))

#########################--- Enemie Ship Class and Basic Methods  ---####################################

class EnemieShip(RocketShip):
    
    def __init__(self, xpos, ypos, maxxpos, change):
        self._xPos = xpos
        self._yPos = ypos
        self._maxXPos = maxxpos
        self._enemiechange = change
        self._view = pygame.image.load("pixel_ship_blue_small.png")
        self._specialview = pygame.image.load("pixel_ship_green_small.png")
        self._screenwidth = 450
        self._enemiewidth = 50
        self._specialenemiechange = 1

    def draw(self, window):
        window.blit(self._view, (self._xPos, self._yPos))

    def specialdraw(self, window):
        window.blit(self._specialview, (self._xPos, self._yPos))

    def specialmove(self):
        self._xPos += self._specialenemiechange
    
    def moveEnemie(self):
        self._yPos += self._enemiechange
          

    
       
#########################--- Missile Class and Basic Methods  ---####################################

class Missile(RocketShip):
    def __init__(self, xpos):
        self._xPos = xpos - 15
        self._yPos = 640
        self._icon = pygame.image.load("pixel_laser_yellow.png")
        self._ballchange = 3
    
    def moveMissile(self):
            self._yPos -= self._ballchange
    def getIcon(self):
        return self._icon

    def isCollidingWith(self, enemy):
        distance = math.sqrt((math.pow(self._xPos -  enemy._xPos, 2)) +(math.pow( self._yPos -  enemy._yPos, 2)))
        if distance < 30:
            return True
        else:
            return False 
      

#########################--- Run Game  ---#################################### 

if __name__ == "__main__":
    mygame = MyGame()
    mygame.rungame()


