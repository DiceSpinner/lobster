import pygame
import math
import random
size=(1290,900)
#color brightness
red=[(0,0,0),(51,0,0),(102,0,0),(153,0,0),(204,0,0),(255,0,0)]
blue=[(0,0,0),(0,0,51),(0,0,102),(0,0,153),(0,0,204),(0,0,255)]
green=[(0,0,0),(0,51,0),(0,102,0),(0,153,0),(0,204,0),(0,255,0)]
white=[(0,0,0),(51,51,51),(102,102,102),(153,153,153),(204,204,204),(255,255,255)]
black=(0,0,0)
clock=pygame.time.Clock()
std = 30 #game ticks per sec
casts = [] #display message queue
casting = 0
count = 0
#init
pygame.init()
pygame.display.set_icon(pygame.image.load("Lobster_clean.png"))
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Lobster")

#sound
FireBall_launch=pygame.mixer.Sound("FireBall_launch.wav")
FireBall_explode=pygame.mixer.Sound("FireBall_explode.wav")
hurt=pygame.mixer.Sound("hurt.wav")
openDoor=pygame.mixer.Sound("open_creaky_door.wav")
openChest=pygame.mixer.Sound("open_chest.wav")
die=pygame.mixer.Sound("die.wav")
keysound=pygame.mixer.Sound("keys_drop.wav")

#images
healSign = pygame.image.load("heal.png")
meditateSign = pygame.image.load("meditate.png")

#Basic info display
def refresh():
    for a in range (40):
        for b in range (30):
            blockMap[a][b].display()

def broadCast(text,flag = True):
    eraseCast()
    global casting
    casting = text
    font=pygame.font.Font(None,50)
    textImage=font.render(text, True, (255,255,255))
    if player.y<=450:
        screen.blit(textImage, [400,800])
    else:
        screen.blit(textImage, [400,100])
    if flag:
        counter=0
def playerInfoDisplay():
    font=pygame.font.Font(None,25)
    font_2=pygame.font.Font(None,20)

    health=font.render("Health", True, green[5])
    attackAvability=font.render("Stamina",True,(255,255,0))
    sp=font.render("SpellPower",True,(0,255,255))
    s=font.render(str(player.spellPower),True,(0,0,255))
    keyNum=font.render("Keys",True,(255,255,0))
    keys=font.render(str(player.keyCount),True,(255,255,255))
    heal=font_2.render("HealPotion(1)",True,(255,255,0))
    healPotion=font.render(str(player.healPotionCount),True,(255,255,0))
    bE=font_2.render("BlueElixir(2)",True,(0,255,0))
    blueElixir=font.render(str(player.blueElixirCount),True,(0,255,255))

    pygame.draw.rect(screen,black,[1200,0,90,900])

    screen.blit(health,[1200,0])
    pygame.draw.rect(screen,red[5],[1200,20,player.health*9,10])

    screen.blit(sp,[1200,40])
    pygame.draw.rect(screen,(0,0,255),[1200,60,player.spellPower,10])

    screen.blit(attackAvability,[1200,80])
    if player.stamina<90:
        pygame.draw.rect(screen,red[4],[1200,100,player.stamina,10])
    else:
        pygame.draw.rect(screen,green[5],[1200,100,player.stamina,10])

    screen.blit(keyNum,[1200,120])
    screen.blit(keys,[1200,140])

    screen.blit(heal,[1200,160])
    screen.blit(healPotion,[1200,180])
    if player.hc != 0:
        pygame.draw.rect(screen,red[4],[1230,180,(player.healCoolDown - player.hc) * 60 // player.healCoolDown,10])
    else:
        pygame.draw.rect(screen,green[5],[1230,180,60,10])

    screen.blit(bE,[1200,200])
    screen.blit(blueElixir,[1200,220])
    if player.mc != 0:
        pygame.draw.rect(screen,red[4],[1230,220,(player.meditateCoolDown - player.mc) * 60 // player.meditateCoolDown,10])
    else:
        pygame.draw.rect(screen,green[5],[1230,220,60,10])
    if Creature.bossFight:
        for boss in Creature.allBoss:
            #print("displaying boss",boss.creatureType)
            if boss.health>0:


                if boss.creatureType==4:
                    pygame.draw.rect(screen,(0,0,0),[245,700,1000,20])
                    pygame.draw.rect(screen,(0,255,255),[245,700,boss.health*8,20])
                elif boss.creatureType==5:
                    pygame.draw.rect(screen,(0,0,0),[245,750,1000,20])
                    pygame.draw.rect(screen,(255,255,0),[245,750,boss.health*8,20])


    if Creature.bossFightEnd:
        broadCast("Last Final Door to Unlock")
        if Block.eventCount==0:
            screen.fill((0,0,0))
            Block.eventCount+=1

def eraseCast():
    #print("erase")
    if player.y <= 450:
        for a in range(13,40):
            for b in range(26,29):
                blockMap[a][b].display()
    else:
        for a in range(13,40):
            for b in range(0,5):
                blockMap[a][b].display()

#predefined map objects


class Block:
    #basic properties
    x,y=None,None
    texture=None
    #For recursion
    linked=[]
    #States
    blockType=None
    pickable=None
    openable=None
    unlockable=None
    passible=None
    breakable=None
    #Additional attributes
    lightLevel=0
    eventCount=0
    #static fields
    teleportable=[]
    teleportor = []
    zombieSpawner=[]
    receiver=[]
    bossSpawner=[]
    def __init__(self,xCor,yCor,Type,pickable=False,openable=False,unlockable=False,breakable=False):
        self.x=xCor
        self.y=yCor
        self.blockType=Type

        #load texture
        if self.blockType==0:
            self.passible=False
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Obstacle_20.png"),pygame.image.load("Obstacle_40.png"),pygame.image.load("Obstacle_60.png"),pygame.image.load("Obstacle_80.png"),pygame.image.load("Obstacle_100.png")]
        elif self.blockType==1:
            self.passible=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Path_20.png"),pygame.image.load("Path_40.png"),pygame.image.load("Path_60.png"),pygame.image.load("Path_80.png"),pygame.image.load("Path_100.png")]
        elif self.blockType==2:
            self.passible=False
            self.unlockable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Door_close_20.png"),pygame.image.load("Door_close_40.png"),pygame.image.load("Door_close_60.png"),pygame.image.load("Door_close_80.png"),pygame.image.load("Door_close_100.png")]
        elif self.blockType==3:
            self.passible=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Door_open_20.png"),pygame.image.load("Door_open_40.png"),pygame.image.load("Door_open_60.png"),pygame.image.load("Door_open_80.png"),pygame.image.load("Door_open_100.png")]
        elif self.blockType==4:
            self.passible=False
            self.openable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Chest_close_20.png"),pygame.image.load("Chest_close_40.png"),pygame.image.load("Chest_close_60.png"),pygame.image.load("Chest_close_80.png"),pygame.image.load("Chest_close_100.png")]
        elif self.blockType==5:
            self.passible=False
            self.openable=False
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Chest_open_20.png"),pygame.image.load("Chest_open_40.png"),pygame.image.load("Chest_open_60.png"),pygame.image.load("Chest_open_80.png"),pygame.image.load("Chest_open_100.png")]
        elif self.blockType==6:
            self.passible=True
            self.pickable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Key_20.png"),pygame.image.load("Key_40.png"),pygame.image.load("Key_60.png"),pygame.image.load("Key_80.png"),pygame.image.load("Key_100.png")]
        elif self.blockType==7:
            self.passible=True
            self.pickable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("HealPotion_20.png"),pygame.image.load("HealPotion_40.png"),pygame.image.load("HealPotion_60.png"),pygame.image.load("HealPotion_80.png"),pygame.image.load("HealPotion_100.png")]
        elif self.blockType==8:
            self.passible=True
            self.pickable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("SpeedPotion_20.png"),pygame.image.load("SpeedPotion_40.png"),pygame.image.load("SpeedPotion_60.png"),pygame.image.load("SpeedPotion_80.png"),pygame.image.load("SpeedPotion_100.png")]
        elif self.blockType==9:
            self.passible=True
            self.pickable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("StrengthPotion_20.png"),pygame.image.load("StrengthPotion_40.png"),pygame.image.load("StrengthPotion_60.png"),pygame.image.load("StrengthPotion_80.png"),pygame.image.load("StrengthPotion_100.png")]
        elif self.blockType==10:#Breakable wall
            self.passible=False
            self.breakable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Dirt_20.png"),pygame.image.load("Dirt_40.png"),pygame.image.load("Dirt_60.png"),pygame.image.load("Dirt_80.png"),pygame.image.load("Dirt_100.png")]
        elif self.blockType==11:#Mud
            self.passible=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Mud_20.png"),pygame.image.load("Mud_40.png"),pygame.image.load("Mud_60.png"),pygame.image.load("Mud_80.png"),pygame.image.load("Mud_100.png")]
        elif self.blockType==12:#zombieSpawmer
            self.passible=True
            Block.zombieSpawner+=[self]
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Path_20.png"),pygame.image.load("Path_40.png"),pygame.image.load("Path_60.png"),pygame.image.load("Path_80.png"),pygame.image.load("Path_100.png")]
        elif self.blockType==13:#Teleport Portal
            Block.teleportor.append(self)
            self.passible=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Portal_teleportor.jpg"),pygame.image.load("Portal_teleportor.jpg"),pygame.image.load("Portal_teleportor.jpg"),pygame.image.load("Portal_teleportor.jpg"),pygame.image.load("Portal_teleportor.jpg")]
        elif self.blockType==14:#Receive Portal
            self.passible=True
            Block.receiver+=[self]
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Portal_receiver.jpg"),pygame.image.load("Portal_receiver.jpg"),pygame.image.load("Portal_receiver.jpg"),pygame.image.load("Portal_receiver.jpg"),pygame.image.load("Portal_receiver.jpg")]
        elif self.blockType==15:
            self.passible=True
            self.pickable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("BlueElixir_20.png"),pygame.image.load("BlueElixir_40.png"),pygame.image.load("BlueElixir_60.png"),pygame.image.load("BlueElixir_80.png"),pygame.image.load("BlueElixir_100.png")]

        elif self.blockType==16:
            self.passible=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Path_20.png"),pygame.image.load("Path_40.png"),pygame.image.load("Path_60.png"),pygame.image.load("Path_80.png"),pygame.image.load("Path_100.png")]
            Block.bossSpawner+=[self]

        elif self.blockType==17:
            self.passible=True
            self.pickable=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("SpellBook.png"),pygame.image.load("SpellBook.png"),pygame.image.load("SpellBook.png"),pygame.image.load("SpellBook.png"),pygame.image.load("SpellBook.png")]

        elif self.blockType==18:
            self.passible=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Portal_teleportor.jpg"),pygame.image.load("Portal_teleportor.jpg"),pygame.image.load("Portal_teleportor.jpg"),pygame.image.load("Portal_teleportor.jpg"),pygame.image.load("Portal_teleportor.jpg")]

        elif self.blockType==19:
            self.passible=True
            self.texture=[pygame.image.load("dark.png"),pygame.image.load("Path_20.png"),pygame.image.load("Path_40.png"),pygame.image.load("Path_60.png"),pygame.image.load("Path_80.png"),pygame.image.load("Path_100.png")]
            Block.teleportable.append(self)

    #Unused method

    def collide(self,p):#Only for obstacle blocks and special interactions
        if abs(self.x-p.x)<=15+p.collisionRadius and abs(self.y-p.y)<=15+p.collisionRadius:
            return True
        else:
            return False

    #detection methods
    def getAdjacent(self):
        block_left=blockMap[self.x//30-1][self.y//30]
        block_leftup=blockMap[self.x//30-1][self.y//30-1]
        block_up=blockMap[self.x//30][self.y//30-1]
        block_rightup=blockMap[self.x//30+1][self.y//30-1]
        block_right=blockMap[self.x//30+1][self.y//30]
        block_rightdown=blockMap[self.x//30+1][self.y//30+1]
        block_down=blockMap[self.x//30][self.y//30+1]
        block_leftdown=blockMap[self.x//30-1][self.y//30+1]
        blockList=[block_left,block_leftup,block_up,block_rightup,block_right,block_rightdown,block_down,block_leftdown]
        return blockList

    def getBesides(self):
        blockList_1=self.getAdjacent()
        blockList=[blockList_1[0],blockList_1[2],blockList_1[4],blockList_1[6]]
        return blockList

    #Test method

    def displayInfo(self):
        print("Centre cord:",self.x,self.y)
        print("Passible=",self.passible)

    def display(self):
        if self.lightLevel>5:
            self.lightLevel=5
        screen.blit(self.texture[self.lightLevel],[self.x-15,self.y-15])

    #Lighting methods

    def enlighten(self,brightness):
        if self.lightLevel<brightness:
            self.lightLevel=brightness
        self.display()
        if brightness>0 and self.passible:
            for block in self.getBesides():
                if block.lightLevel<=brightness-1 and block.passible:
                    block.enlighten(brightness-1)
                elif block.lightLevel<=brightness-1 and not block.passible:
                    block.lightLevel=brightness-1
                block.display()

    def refreshLight(self,brightness,refreshed):
        #print("Y")
        self.display()
        refreshed.append(self)
        if brightness>=0:
            for block in self.getBesides():
                if not block in refreshed and block.passible:
                    block.refreshLight(brightness-1,refreshed)
                if not block.passible:
                    block.display()
#Character class
class Creature:
    bossFightEnd=False
    bossFight=False
    started=False
    allBoss=[]
    creatureList=[]
    allFireBall=[]
    #basic properties
    x,y=None,None
    moveSpeed=1
    health=10
    stamina=100#attack per x frame
    attackDamage=2
    attackSpeed=15
    attackRange=20
    spellPower=90
    collisionRadius=None
    direction=None
    vision=5
    #Additional attributes
    collideType=[]
    attackCounter=0
    attackType=None
    creatureType=None       #0 for player, 1 for zombie
    texture=None
    keyCount=0
    healPotionCount=0
    blueElixirCount=0
    spellBookCount=0
    keyCount=0
    castCount=0
    deathCounter=0
    displayCounter=0
    stuckCounter=0
    #monster
    aggroRange=4
    #boss
    superNova=False
    powerCounter=0
    powerCoolDown = 10 * std
    fireCounter=0
    fireTime=0
    transformed=False
    #monster counter
    zombieCount=0
    #State
    attackDisplay=False
    empowered=False
    tp=False
    op=False
    ul=False
    br=False
    ca=False
    dead=False
    #changeDirection=False
    stuck=False
    #FireBall
    explode=False

    def reset(self):
        if not Creature.bossFight:
            loadMap(1)
            self.dead=False
            Creature.creatureList=[self]
            Creature.zombieCount=0
            self.x=1145
            self.y=45
            self.keyCount=0
            self.healPotionCount=0
            self.health=10
            self.attackdamage=2
            self.moveSpeed=2
            self.blueElixirCount=0
            self.spellPower=90
            self.empowered=False
            Creature.empowered=False
            self.spellBookCount=0
            self.dead=False
        if Creature.bossFight:
            Block.bossSpawner=[]
            loadMap(1)
            self.healPotionCount+=3
            self.blueElixirCount+=3
            self.health=10
            self.spellPower=90
            self.dead=False
            Creature.creatureList=[self]
            self.x=Block.receiver[0].x
            self.y=Block.receiver[0].y
            k=0
            Creature.allBoss=[]
            for spawner in Block.bossSpawner:
                #print("Respawning boss")
                boss=Creature(spawner.x,spawner.y,3,10,0,4+k,5)
                Creature.creatureList.append(boss)
                Creature.allBoss.append(boss)
                k+=1

            screen.fill((0,0,0))
            Creature.allFireBall=[]
    def die(self):
        #print("removing",self.x,self.y)
        self.displayUpdate()
        if self in Creature.creatureList:
            Creature.creatureList.remove(self)

        if self.creatureType==1:
            Creature.zombieCount-=1
        elif self.creatureType==0:
            broadCast("You died")
            self.dead=True

    def __init__(self,xCor,yCor,ms,collisionRad=10,direct=0,Type=0,vision=0,attackType=None):
        self.x=xCor
        self.y=yCor
        self.moveSpeed=ms
        self.collisionRadius=collisionRad
        self.direction=direct
        self.creatureType=Type
        self.vision=vision
        if self.creatureType==0:
            self.texture=[pygame.image.load("Lobster_0.png"),pygame.image.load("Lobster_1.png"),pygame.image.load("Lobster_2.png"),pygame.image.load("Lobster_3.png"),pygame.image.load("Lobster_4.png"),pygame.image.load("Lobster_5.png"),pygame.image.load("Lobster_6.png"),pygame.image.load("Lobster_7.png")]
            print("Texture loadded")
            self.attackRange=35
            self.attackSpeed=15
            self.stamina=90
            self.staminaMax = 90
            self.staminaCost = [30,20]
            self.staminaRegen = 1
            self.spellPower = 90
            self.spellPowerMax = 90
            self.vision=5
            self.attackType=[1,4,5]
            self.healCounter = 0
            self.meditateCounter = 0
            self.healthMax = 10
            self.healCoolDown = 10 * std
            self.meditateCoolDown = 5 * std
            self.healPower = 1
            self.meditatePower = 10
            self.hc = 0
            self.mc = 0
        elif self.creatureType==1:
            self.healthMax = 10
            self.texture=[pygame.image.load("Lobster_0.png"),pygame.image.load("Lobster_1.png"),pygame.image.load("Lobster_2.png"),pygame.image.load("Lobster_3.png"),pygame.image.load("Lobster_4.png"),pygame.image.load("Lobster_5.png"),pygame.image.load("Lobster_6.png"),pygame.image.load("Lobster_7.png")]
            print("Texture loadded")
            self.stamina=90
            self.staminaMax = 90
            self.staminaCost = [30,20]
            self.staminaRegen = 1
            self.attackDamage=1
            self.attackSpeed=45
            self.attackRange=25
            self.spellPower = 90
            self.spellPowerMax = 90
            self.attackType=[0]
            if Creature.empowered:
                self.empowered=True
            self.healCounter = 0
            self.meditateCounter = 0
            self.healCoolDown = 10 * std
            self.meditateCoolDown = 5 * std
            self.healPower = 1
            self.meditatePower = 10
            self.hc = 0
            self.mc = 0
        elif self.creatureType==3:
            self.vision=3
            self.texture=[pygame.image.load("FireBall.png"),pygame.image.load("FireBall.png"),pygame.image.load("FireBall.png"),pygame.image.load("FireBall.png"),pygame.image.load("FireBall.png"),pygame.image.load("FireBall.png"),pygame.image.load("FireBall.png"),pygame.image.load("FireBall.png")]

        elif self.creatureType==4:#melee
            self.healthMax = 100
            self.vision=5
            self.aggroRange=20
            self.texture=[pygame.image.load("Lobster_0.png"),pygame.image.load("Lobster_1.png"),pygame.image.load("Lobster_2.png"),pygame.image.load("Lobster_3.png"),pygame.image.load("Lobster_4.png"),pygame.image.load("Lobster_5.png"),pygame.image.load("Lobster_6.png"),pygame.image.load("Lobster_7.png")]
            self.health = 100
            self.stamina=120
            self.staminaMax = 120
            self.staminaCost = [30,20]
            self.staminaRegen = 1
            self.spellPower=0
            self.spellPowerMax = 0
            self.attackSpeed=30
            self.moveSpeed=3
            self.empowered=False
            self.attackDamage=4
            self.attackRange=25
            self.attackType=[0]
            self.healCoolDown = 25 * std
            self.meditateCoolDown = 5 * std
            self.healPower = 2
            self.meditatePower = 10
            self.hc = 0
            self.mc = 0
            self.healCounter = 0
            self.meditateCounter = 0
        elif self.creatureType==5:
            self.healthMax = 100
            self.vision=5
            self.aggroRange=20
            self.texture=[pygame.image.load("Lobster_0.png"),pygame.image.load("Lobster_1.png"),pygame.image.load("Lobster_2.png"),pygame.image.load("Lobster_3.png"),pygame.image.load("Lobster_4.png"),pygame.image.load("Lobster_5.png"),pygame.image.load("Lobster_6.png"),pygame.image.load("Lobster_7.png")]
            self.health=100
            self.stamina=120
            self.staminaMax = 120
            self.staminaCost = [30,20]
            self.staminaRegen = 1
            self.spellPower = 200
            self.spellPowerMax = 200
            self.attackSpeed=45
            self.moveSpeed=2
            self.attackDamage=3
            self.empowered=False
            self.attackType=[0]
            self.healCoolDown = 25 * std
            self.meditateCoolDown = 5 * std
            self.healPower = 1
            self.meditatePower = 20
            self.hc = 0
            self.mc = 0
            self.healCounter = 0
            self.meditateCounter = 0

    def getBlockInContact(self):
        return blockMap[self.x//30][self.y//30]

    #shared behavior.................................................................................................
    def teleport(self):
        self.tp=False
        if self.x<600:
            self.x=Block.receiver[0].x
            self.y=Block.receiver[0].y
            Creature.bossFight=True
        else:
            self.x=Block.receiver[1].x
            self.y=Block.receiver[1].y
        for a in range(40):
            for b in range(30):
                blockMap[a][b].lightLevel=0
                blockMap[a][b].display()



    def move(self):
        if self.getBlockInContact().blockType==11 and self.creatureType==0:
            move=self.moveSpeed//2
        else:
            move=self.moveSpeed
        originX=self.x
        originY=self.y
        if self.direction==0:
            self.x-=move
        elif self.direction==1:
            self.x-=move
            self.y-=move
        elif self.direction==2:
            self.y-=move
        elif self.direction==3:
            self.x+=move
            self.y-=move
        elif self.direction==4:
            self.x+=move
        elif self.direction==5:
            self.x+=move
            self.y+=move
        elif self.direction==6:
            self.y+=move
        elif self.direction==7:
            self.x-=move
            self.y+=move
        if self.collide():
            if self.creatureType==3:
                self.explode=True

            if 0 in self.collideType and self.x<originX:
                self.x=originX
            if 1 in self.collideType and self.y<originY:
                self.y=originY
            if 2 in self.collideType and self.x>originX:
                self.x=originX
            if 3 in self.collideType and self.y>originY:
                self.y=originY


    def fire(self):
        if self.stamina>=self.staminaCost[1] and self.spellPower>=10:
            if self.creatureType==5:
                self.attackCounter=0
            self.stamina-=self.staminaCost[1]
            self.spellPower-=10
            pygame.mixer.Sound.play(FireBall_launch)
            if not self.empowered:
                fireBall=Creature(self.x,self.y,4,7,self.direction,3)
                Creature.allFireBall+=[fireBall]
                fireBall.attackDamage=self.attackDamage
                fireBall.attackType=self.attackType
                fireBall.explode=False
            else:
                #print("Fire")
                fireBall=Creature(self.x,self.y,5,7,self.direction,3)
                Creature.allFireBall+=[fireBall]
                fireBall.empowered=True
                fireBall.attackDamage=self.attackDamage+1
                fireBall.explode=False
                fireBall.attackType=self.attackType
        else:
            print("Launch Failed:",self.creatureType)
            if self.stamina < self.staminaCost[1]:
                print(" Not Enough Stamina")
            else:
                print("Attack still on CoolDown:",self.attackCounter,"/",self.attackSpeed)
    def cleave(self):
        if self.stamina>=self.staminaCost[0] and self.attackCounter >= self.attackSpeed:
            self.stamina-=self.staminaCost[0]
            self.attackCounter=0
            if self.getBlockInContact().lightLevel > 0:
                self.displayCounter=0
                self.attackDisplay=True
            #print("Attempting to attack",self.getBlockInContact().lightLevel)
            for creature in Creature.creatureList:

                if creature.creatureType in self.attackType:

                    if (creature.x-self.x)**2+(creature.y-self.y)**2<=(self.attackRange+creature.collisionRadius)**2:
                        creature.health-=self.attackDamage
                        pygame.mixer.Sound.play(hurt)
                        #print("AttackDamage:",self.attackDamage)
                        #print("Dealing damage to",creature.x,creature.y)
                        #print("remaining health",creature.health)
                    else:
                        #print("Target not in range")
                        pass
        else:
            print("Attack Failed:",self.creatureType)
            if self.stamina < self.staminaCost[0]:
                print(" Not Enough Stamina")
            else:
                print("Attack still on CoolDown:",self.attackCounter,"/",self.attackSpeed)



    def pick(self):
        item=player.getBlockInContact().blockType
        if item==6:
            self.keyCount+=1
            casts.append("Key + 1")
            pygame.mixer.Sound.play(keysound)
        elif item==7:
            self.healPotionCount+=1
            casts.append("HealPotion + 1")
        elif item==8:
            self.moveSpeed+=1
            casts.append("SpeedUp")
        elif  item==9:
            self.attackDamage+=1
            casts.append("Strength increased")
        elif item==15:
            self.blueElixirCount+=1
            casts.append("BlueElixir + 1")
        elif item==17:
            self.spellBookCount+=1
            casts.append(str(self.spellBookCount)+" out of 2 spell books picked up")
            if self.spellBookCount==2:
                casts.append("FireBall Empowered!")
                for creature in Creature.creatureList:
                    creature.empowered=True
                Creature.empowered=True

        player.getBlockInContact().blockType=1
        player.getBlockInContact().texture=[pygame.image.load("dark.png"),pygame.image.load("Path_20.png"),pygame.image.load("Path_40.png"),pygame.image.load("Path_60.png"),pygame.image.load("Path_80.png"),pygame.image.load("Path_100.png")]


    def open(self,c,d):
        pygame.mixer.Sound.play(openChest)
        item=random.randint(0,9)
        if item==0 or item==1 or item==2:
            self.keyCount+=1
            casts.append("Key + 1")
            print("Key + 1")
        elif item==3 or item==4 or item==5:
            self.healPotionCount+=1
            casts.append("HealPotion + 1")
            print("Healpotion + 1")
        elif item==6 or item==7 or item==8:
            self.blueElixirCount+=1
            casts.append("BlueElixir + 1")
        elif item==9:
            self.vision+=1
            casts.append("Vision strengthened")
        if c!=None and d!=None:
            blockMap[c][d].blockType=5
            blockMap[c][d].openable=False
            blockMap[c][d].texture=[pygame.image.load("dark.png"),pygame.image.load("Chest_open_20.png"),pygame.image.load("Chest_open_40.png"),pygame.image.load("Chest_open_60.png"),pygame.image.load("Chest_open_80.png"),pygame.image.load("Chest_open_100.png")]
            blockMap[c][d].display()

    def heal(self):
        if self.health < self.healthMax:
            self.healCounter += 5
            self.hc = self.healCoolDown

    def meditate(self):
        if self.spellPower < self.spellPowerMax:
            self.meditateCounter += 3
            self.mc = self.meditateCoolDown

    def unlock(self,c,d):
        print("unlocked door")
        pygame.mixer.Sound.play(openDoor)
        blockMap[c][d].blockType=3
        blockMap[c][d].unlockable=False
        blockMap[c][d].passible=True
        blockMap[c][d].texture=[pygame.image.load("dark.png"),pygame.image.load("Door_open_20.png"),pygame.image.load("Door_open_40.png"),pygame.image.load("Door_open_60.png"),pygame.image.load("Door_open_80.png"),pygame.image.load("Door_open_100.png")]
        self.keyCount-=1

    def brek(self,c,d):
        blockMap[c][d].blockType=1
        blockMap[c][d].breakable=False
        blockMap[c][d].passible=True
        blockMap[c][d].texture=[pygame.image.load("dark.png"),pygame.image.load("Path_20.png"),pygame.image.load("Path_40.png"),pygame.image.load("Path_60.png"),pygame.image.load("Path_80.png"),pygame.image.load("Path_100.png")]
        blockMap[c][d].display()

    def displayInfo(self):
        print(self.x,self.y)
        print("MoveSpeed=",self.moveSpeed)
        print("CollisionRadius=",self.collisionRadius)
        print("Direction=",self.direction)

    def display(self):
        if self.creatureType != 3:
            if self.direction==0 or self.direction==2 or self.direction==4 or self.direction==6:
                screen.blit(self.texture[self.direction],[self.x-15,self.y-15])
            else:
                screen.blit(self.texture[self.direction],[self.x-22,self.y-22])
        else:
            screen.blit(self.texture[self.direction],[self.x-14,self.y-14])
        if self.creatureType==0:
            pygame.draw.circle(screen,green[5],(self.x,self.y),self.collisionRadius)
        elif self.creatureType==1:
            pygame.draw.circle(screen,(255,128,0),(self.x,self.y),self.collisionRadius)
        elif self.creatureType==4:
            pygame.draw.circle(screen,(0,255,255),(self.x,self.y),self.collisionRadius)
            if self.transformed:
                pygame.draw.circle(screen,(255,0,0),(self.x,self.y),self.collisionRadius-4)
        elif self.creatureType==5:
            pygame.draw.circle(screen,(255,255,0),(self.x,self.y),self.collisionRadius)
            if self.transformed:
                pygame.draw.circle(screen,(255,0,0),(self.x,self.y),self.collisionRadius-4)

        if not self.creatureType == 3:
            if self.health > 0:
                pygame.draw.rect(screen,(255,0,0),[self.x - 15,self.y - 15,(self.health * 30 // self.healthMax),5])

            if self.spellPower > 0:
                pygame.draw.rect(screen,(0,170,255),[self.x - 15,self.y - 10,(self.spellPower * 30 // self.spellPowerMax ),3])

            if self.meditateCounter > 0:
                screen.blit(meditateSign,[self.x + 10,self.y-10])

            if self.healCounter > 0:
                screen.blit(healSign,[self.x + 13,self.y-16])

    def displayUpdate(self):
        currentBlock=self.getBlockInContact()
        for a in range(-1,2):
            for b in range(-1,2):
                blockMap[currentBlock.x//30+b][currentBlock.y//30+a].display()

    #collision detection
    def collide(self):
        checkList=[0,1,2,3,4,5,6,7]
        currentBlock=self.getBlockInContact()
        #print("currentBlock:",currentBlock.x,currentBlock.y)
        surroundings=currentBlock.getAdjacent()
        if self.creatureType==3:
            #print("currentBlock",currentBlock.x,currentBlock.y)
            surroundings.append(currentBlock)
            checkList.append(8)
        overAllFlag=False

        for direction in checkList:
            directionFlag=False
            xDifference=abs(self.x-surroundings[direction].x)
            yDifference=abs(self.y-surroundings[direction].y)
            #print("Direction:",direction)
            #print("Block:",surroundings[direction].displayInfo())
            if not surroundings[direction].passible:
                if direction==1 or direction==3 or direction==5 or direction==7:
                    #print("2nd checking block:")
                    #print(surroundings[direction].x,surroundings[direction].y)
                    if direction==1:
                        detectX=surroundings[direction].x+15
                        detectY=surroundings[direction].y+15
                        if (detectX-self.x)**2+(detectY-self.y)**2<(self.collisionRadius-1)**2:
                            overAllFlag=True
                            directionFlag=True
                            if not 0 in self.collideType:
                               self.collideType+=[0]
                            if not 1 in self.collideType:
                               self.collideType+=[1]

                    elif direction==7:
                        detectX=surroundings[direction].x+15
                        detectY=surroundings[direction].y-15
                        if (detectX-self.x)**2+(self.y-detectY)**2<(self.collisionRadius-1)**2:
                            overAllFlag=True
                            directionFlag=True
                            if not 0 in self.collideType:
                               self.collideType+=[0]
                            if not 3 in self.collideType:
                               self.collideType+=[3]

                    elif direction==3:
                        detectX=surroundings[direction].x-15
                        detectY=surroundings[direction].y+15
                        if (detectX-self.x)**2+(self.y-detectY)**2<(self.collisionRadius-1)**2:
                            overAllFlag=True
                            directionFlag=True
                            if not 2 in self.collideType:
                                self.collideType+=[2]
                            if not 1 in self.collideType:
                                self.collideType+=[1]

                    elif direction==5:
                        detectX=surroundings[direction].x-15
                        detectY=surroundings[direction].y-15
                        if math.sqrt((detectX-self.x)**2+(self.y-detectY)**2)<self.collisionRadius-1:
                            overAllFlag=True
                            directionFlag=True
                            if not 2 in self.collideType:
                               self.collideType+=[2]
                            if not 3 in self.collideType:
                               self.collideType+=[3]
                else:
                    if xDifference<self.collisionRadius+15 and yDifference<self.collisionRadius+15:
                        #print("Collide with Block at",surroundings[direction].x,surroundings[direction].y)
                        overAllFlag=True
                        directionFlag=True
                        #print("Player pos:",player.x,player.y)
                        #surroundings[direction].displayInfo()
                        if direction==0:
                            if not 0 in self.collideType:
                                self.collideType+=[0]
                        elif direction==2:
                            if not 1 in self.collideType:
                                self.collideType+=[1]
                        elif direction==4:
                            if not 2 in self.collideType:
                                self.collideType+=[2]
                        elif direction==6:
                            if not 3 in self.collideType:
                                self.collideType+=[3]


                if directionFlag:
                    #print("colliding with direction",direction)
                    if self.creatureType==0:
                        if blockMap[surroundings[direction].x//30][surroundings[direction].y//30].openable:
                            casts.append("Press f to open the chest.")
                            self.op=True

                        elif blockMap[surroundings[direction].x//30][surroundings[direction].y//30].unlockable:
                            if self.keyCount>0:
                                casts.append("Press r to unlock the door.")
                                self.ul=True
                if not overAllFlag:
                    self.collideType=[]
        return overAllFlag


    #Zombie behavior
    def adjustPos(self):
        currentBlock=self.getBlockInContact()

    def searchForTarget(self,target):
        if (self.creatureType==4 or self.creatureType == 1 or self.creatureType == 5) and (self.attackSpeed <= self.attackCounter and math.sqrt((self.x-target.x)**2+(self.y-target.y)**2) <= self.attackRange):
            self.cleave()
        if abs(self.x-target.x)<self.aggroRange*30 and abs(self.y-target.y)<self.aggroRange*30:
            if self.stuck:

                currentBlock=self.getBlockInContact()
                if self.x!=currentBlock.x or self.y!=currentBlock.y:
                    if self.x<currentBlock.x:
                        self.x+=1
                    elif self.x>currentBlock.x:
                        self.x-=1
                    if self.y<currentBlock.y:
                        self.y+=1
                    elif self.y>currentBlock.y:
                        self.y-=1

                if abs(self.x-currentBlock.x)<5 and abs(self.y-currentBlock.y)<5:
                    self.stuck=False
                    self.stuckCounter=0


            else:
                if self.creatureType==1 or self.creatureType==4:
                    if math.sqrt((self.x-target.x)**2+(self.y-target.y)**2)>15:
                        previous=[self.x,self.y]
                        if self.x//30==target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=6

                            elif self.y//30>target.y//30:
                                self.direction=2

                        elif self.x//30>target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=7
                            elif self.y//30>target.y//30:
                                self.direction=1
                            elif self.y//30==target.y//30:
                                self.direction=0
                        elif self.x//30<target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=5
                            elif self.y//30>target.y//30:
                                self.direction=3
                            elif self.y//30==target.y//30:
                                self.direction=4
                        self.move()
                        if self.creatureType==1:
                            if self.health < self.healthMax and self.hc == 0:
                                self.heal()
                            if self.spellPower > 10:
                                if self.attackCounter==self.attackSpeed:
                                    self.attackCounter=0
                                    self.fire()
                            elif self.mc == 0:
                                self.meditate()
                        current=[self.x,self.y]

                        if previous==current:
                            self.stuckCounter+=1
                            if self.stuckCounter>=30:
                                self.stuck=True
                        else:
                            self.stuckCounter=0

                elif self.creatureType==5:
                    if math.sqrt((self.x-target.x)**2+(self.y-target.y)**2)<=60 or self.spellPower == 0:
                        previous=[self.x,self.y]
                        if self.x//30==target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=2

                            elif self.y//30>target.y//30:
                                self.direction=6

                        elif self.x//30>target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=3
                            elif self.y//30>target.y//30:
                                self.direction=5
                            elif self.y//30==target.y//30:
                                self.direction=4
                        elif self.x//30<target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=1
                            elif self.y//30>target.y//30:
                                self.direction=7
                            elif self.y//30==target.y//30:
                                self.direction=0
                        self.move()
                        current=[self.x,self.y]
                        if previous==current:
                            self.stuckCounter+=1
                            if self.stuckCounter>=30:
                                self.stuck=True
                        else:
                            self.stuckCounter=0
                    elif math.sqrt((self.x-target.x)**2+(self.y-target.y)**2)>70:

                        previous=[self.x,self.y]
                        if self.x//30==target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=6

                            elif self.y//30>target.y//30:
                                self.direction=2

                        elif self.x//30>target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=7
                            elif self.y//30>target.y//30:
                                self.direction=1
                            elif self.y//30==target.y//30:
                                self.direction=0
                        elif self.x//30<target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=5
                            elif self.y//30>target.y//30:
                                self.direction=3
                            elif self.y//30==target.y//30:
                                self.direction=4
                        self.move()
                        if self.attackCounter==self.attackSpeed:
                            self.fire()
                        #print(self.stuckCounter)
                        current=[self.x,self.y]
                        if previous==current:
                            self.stuckCounter+=1
                            if self.stuckCounter>=30:
                                self.stuck=True
                        else:
                            self.stuckCounter=0

                    else:
                        previous=[self.x,self.y]
                        if self.x//30==target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=6

                            elif self.y//30>target.y//30:
                                self.direction=2

                        elif self.x//30>target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=7
                            elif self.y//30>target.y//30:
                                self.direction=1
                            elif self.y//30==target.y//30:
                                self.direction=0
                        elif self.x//30<target.x//30:
                            if self.y//30<target.y//30:
                                self.direction=5
                            elif self.y//30>target.y//30:
                                self.direction=3
                            elif self.y//30==target.y//30:
                                self.direction=4
                        if self.attackCounter==self.attackSpeed:
                            self.fire()
                        #print(self.stuckCounter)
                        current=[self.x,self.y]
                        if previous==current:
                            self.stuckCounter+=1
                            if self.stuckCounter>=30:
                                self.stuck=True
                        else:
                            self.stuckCounter=0

    #boss
    def standardMoves(self,target):
        self.searchForTarget(target)
        self.powerCounter+=1

        if self.health < self.healthMax:
            if self.hc == 0:
                self.heal()

        if self.creatureType == 5 and self.spellPower < self.spellPowerMax:
            if self.mc == 0:
                self.meditate()

    def blink(self,target):
        for block in target.getBlockInContact().getAdjacent():
            if block in Block.teleportable:
                self.x=block.x
                self.y=block.y
                refresh()
                self.powerCounter=0
                break



    def transform(self):
        self.moveSpeed+=1
        self.attackDamage+=1
        self.attackSpeed = 20
        self.healPower += 1
        self.healCoolDown += (20*std)
        self.meditatePower += 10
        self.meditateCoolDown += (10*std)
        self.staminaMax += 60
        self.staminaRegen += 1
        self.empowered = True
        self.transformed = True

    #............................ underdeveloping functions
    def reachable(start,destination):#unused
        flag=False
        rawList=start.getAdjacent()
        trackList=[rawList[0],rawList[2],rawList[4],rawList[6]]
        for block in trackList:
            if not block.mark:
                block.mark=True
                if block.x == destination.y and block.y==destination.y:
                    flag=True
                    break
                else:
                    if block.passible:
                        if Creature.reachable(block,destination):
                            flag=True



        return flag

    def eraseMark(self):#unused
        for block in blockList in blockMap:
            block.mark=False

        #stardard AI
    def getDistance(start,destination):
        distance=0
        currentBlock=self.getBlockInContact()
        pass






"""
The window is divided into multiple blocks,each block represents a Block object, which can be a path or an obstacle
Each block is 30*30 pixels large


The bottom side of the window is used to display interaction info(or event)



"""
#character info
ms=2
direc=0
xPos=10 #collision radius=15
yPos=10




#mapSet
def loadMap(num):
    print("Loading Map")
    if num==1:
        mapString_1=open('map_1.txt','r')
        for b in range(30):
            temp=mapString_1.readline().split("	")
            for a in range(40):
                #print(a,b)
                while temp[a]!='X\n':
                    if temp[a]=='X':
                        blockMap[a][b]=Block(15+a*30,15+b*30,0)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='O':
                        blockMap[a][b]=Block(15+a*30,15+b*30,1)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='D':
                        blockMap[a][b]=Block(15+a*30,15+b*30,2)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='C':
                        blockMap[a][b]=Block(15+a*30,15+b*30,4)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='!':
                        blockMap[a][b]=Block(15+a*30,15+b*30,5)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='K':
                        blockMap[a][b]=Block(15+a*30,15+b*30,6)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='H':
                        blockMap[a][b]=Block(15+a*30,15+b*30,7)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='S':
                        blockMap[a][b]=Block(15+a*30,15+b*30,8)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='a':
                        blockMap[a][b]=Block(15+a*30,15+b*30,9)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='F':
                        blockMap[a][b]=Block(15+a*30,15+b*30,10)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='s':
                        blockMap[a][b]=Block(15+a*30,15+b*30,11)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='Z':
                        blockMap[a][b]=Block(15+a*30,15+b*30,12)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='T':
                        blockMap[a][b]=Block(15+a*30,15+b*30,13)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='R':
                        blockMap[a][b]=Block(15+a*30,15+b*30,14)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='A':
                        blockMap[a][b]=Block(15+a*30,15+b*30,15)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='M':
                        blockMap[a][b]=Block(15+a*30,15+b*30,16)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='B':
                        blockMap[a][b]=Block(15+a*30,15+b*30,17)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='E':
                        blockMap[a][b]=Block(15+a*30,15+b*30,18)
                        blockMap[a][b].display()
                        break
                    elif temp[a]=='V':
                        blockMap[a][b]=Block(15+a*30,15+b*30,19)
                        blockMap[a][b].display()

                        break
                    else:
                        blockMap[a][b]=Block(15+a*30,15+b*30,1)
                        blockMap[a][b].display()
                        break
                if temp[a]=='X\n':
                        blockMap[a][b]=Block(15+a*30,15+b*30,0)
                        blockMap[a][b].display()




#Map Load
blockMap = [[0 for x in range(30)] for y in range(40)]
loadMap(1)
blockMap[0][0].displayInfo()

#player setup
player=Creature(1155,45,2,8,1,0)
Creature.creatureList.append(player)
PX=0
PY=0
#Creature.bossFight=True
#player.x = Block.receiver[0].x
#player.y = Block.receiver[0].y
player.moveSpeed += 2
#player.attackDamage += 10
#player.x = Block.teleportor[1].x
#player.y = Block.teleportor[1].y
#Enemy setup
spawnCounter=0

#main loop............................................................................
run=True
pressList=[]
keysCount=0
castCounter=0
gameStart=False
intro=True
instruction=False
gameEnd=False
init=False
gin=False
tick = 0
while run:
    clock.tick(std)
    tick += 1
    if tick > 30:
        tick = 0
    if intro:
        if not init:
            pygame.mixer.music.load("Intro.mp3")
            pygame.mixer.music.play(-1)
            init=True
        screen.fill((0,0,0))
        screen.blit(pygame.image.load("Portal_teleportor_ori.jpg"),[0,0])
        screen.blit(pygame.image.load("Portal_receiver_ori.jpg"),[778,388])
        font=pygame.font.Font(None,50)
        text=font.render("Start the game(f)",True,(255,255,0))
        text_2=font.render("Instructions(r)",True,(0,255,0))
        screen.blit(text,[550,400])
        screen.blit(text_2,[570,460])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_f:
                    intro=False
                    gameStart=True
                    screen.fill((0,0,0))
                    pygame.display.flip()
                elif event.key==pygame.K_r:
                    print("intro disabling")
                    intro=False
                    instruction=True
                    screen.fill((0,0,0))
                    pygame.display.flip()
    elif instruction:

        font=pygame.font.Font(None,60)
        font_2=pygame.font.Font(None,30)
        text_1=font.render("Control character movements with direction keys",True,(255,255,0))
        text_2=font.render("Press d to perform a melee attack",True,(255,255,0))
        text_3=font.render("Press q to launch a fireball (SpellPower will be consumed)",True,(0,0,255))
        text_4=font.render("Your goal is to find and beat the boss",True,(255,0,0))
        text_5=font_2.render("It's highly advised to manage your rescource wisely,since the enemies will continue to respawn until you beat the boss",True,(0,255,0))
        text_6=font.render("Good Luck",True,(255,255,0))
        text_7=font.render("Back(g)",True,(255,255,0))
        text_8=font.render("Start the game(f)",True,(255,255,0))
        screen.blit(text_1,[200,100])
        screen.blit(text_2,[350,150])
        screen.blit(text_3,[100,200])
        screen.blit(text_4,[280,250])
        screen.blit(text_5,[100,350])
        screen.blit(text_6,[580,500])
        screen.blit(text_7,[620,700])
        screen.blit(text_8,[520,740])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_g:
                    intro=True
                    instruction=False
                    screen.fill((0,0,0))
                    pygame.display.flip()
                elif event.key==pygame.K_f:
                    gameStart=True
                    instruction=False
                    screen.fill((0,0,0))
                    pygame.display.flip()

    elif gameStart:
        intro=False
        #print("GameLoop")
        if not gin:
            pygame.mixer.music.load("gameStart.mp3")
            pygame.mixer.music.play(-1)
            gin=True
        if player.dead:
            player.deathCounter+=1
            broadCast("RespawnCounter:"+str(player.deathCounter)+"/100")
            if player.deathCounter>=100:
                player.reset()
                player.deathCounter=0

        #print("Firing",player.firing)
        #print("Casting=",player.casting)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            #key down
            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_LEFT:


                    pressList+=[0]
                    keysCount+=1

                if event.key==pygame.K_UP:

                    pressList+=[2]
                    keysCount+=1


                if event.key==pygame.K_RIGHT:

                    pressList+=[4]
                    keysCount+=1

                if event.key==pygame.K_DOWN:

                    pressList+=[6]

                    keysCount+=1
                #Heal
                if player.health < player.healthMax and player.hc == 0 and player.healPotionCount>0:
                    if event.key==pygame.K_1:
                        player.healPotionCount-=1
                        player.heal()
                if player.spellPower < player.spellPowerMax and player.blueElixirCount > 0 and player.mc == 0:
                    if event.key == pygame.K_2:
                        player.blueElixirCount-=1
                        player.meditate()
                #Attacking...........................................................
                if event.key==pygame.K_d:
                    player.cleave()
                if event.key==pygame.K_q:
                    player.fire()


                #opening and unlocking
                if player.op:
                    if event.key==pygame.K_f:
                        eraseCast()
                        BlockList=player.getBlockInContact().getAdjacent()
                        for block in BlockList:
                            if block.openable:
                                player.open(block.x//30,block.y//30)
                        player.op=False



                if player.ul:
                    if event.key==pygame.K_r:
                        BlockList=player.getBlockInContact().getAdjacent()
                        for block in BlockList:
                            if block.unlockable:
                                player.unlock(block.x//30,block.y//30)
                        player.ul=False
                        eraseCast()

                if player.tp:
                    if player.getBlockInContact().blockType!=13:
                        player.tp=False
                    else:
                        broadCast("Enter the portal(P)")
                        if event.key==pygame.K_p:
                            player.teleport()
                            eraseCast()
            #key up
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT:


                    pressList.remove(0)
                    keysCount-=1

                if event.key==pygame.K_UP:

                    pressList.remove(2)

                    keysCount-=1


                if event.key==pygame.K_RIGHT:


                    pressList.remove(4)
                    keysCount-=1

                if event.key==pygame.K_DOWN:


                    pressList.remove(6)
                    keysCount-=1





        #player direction
        if keysCount==1:
            player.direction=pressList[0]
        elif keysCount==2:
            if abs(pressList[0]-pressList[1])==4:
                PX=0
                PY=0
            else:
                if pressList[0]==0 and pressList[1]==6 or pressList[0]==6 and pressList[1]==0:
                    player.direction=7
                else:
                    player.direction=min(pressList[0],pressList[1])+1

        elif keysCount==3:
            if abs(pressList[0]-pressList[1])==4:
                player.direction=pressList[2]
            elif abs(pressList[0]-pressList[2])==4:
                player.direction=pressList[1]
            elif abs(pressList[2]-pressList[1])==4:
                player.direction=pressList[0]

        # direction movement:
        if keysCount!=0:
            player.move()

        """
        for a in range(30):
            for b in range(40):
                blockMap[b][a].display()
        """

        #print(zombie.health)
        for b in range(30):
            for a in range(40):
                blockMap[a][b].lightLevel=0


        player.getBlockInContact().enlighten(player.vision)

        for creature in Creature.creatureList:
            creature.displayUpdate()
        for fireBall in Creature.allFireBall:
            fireBall.move()
            for creature in Creature.creatureList:
                if creature.creatureType in fireBall.attackType:
                    if (fireBall.x-creature.x)**2+(fireBall.y-creature.y)**2<=(fireBall.collisionRadius+creature.collisionRadius)**2:
                        fireBall.explode=True
            if not fireBall.explode:
                fireBall.getBlockInContact().enlighten(fireBall.vision)
            else:
                fireBall.getBlockInContact().refreshLight(fireBall.vision,[])
            fireBall.displayUpdate()
        for creature in Creature.creatureList:
            if creature.healCounter > 0 and tick == 0:
                creature.healCounter -= 1
                creature.health += creature.healPower
                if creature.health > creature.healthMax:
                    creature.health = creature.healthMax

            if creature.meditateCounter > 0 and tick == 0:
                creature.meditateCounter -= 1
                creature.spellPower += creature.meditatePower
                if creature.spellPower > creature.spellPowerMax:
                    creature.spellPower = creature.spellPowerMax
            if creature.mc > 0:
                creature.mc -= 1
            if creature.hc > 0:
                creature.hc -= 1


            if creature.attackDisplay:
                if creature.displayCounter<8:
                    creature.displayCounter+=1
                    screen.blit(pygame.image.load("ShieldBash.png"),[creature.x-25,creature.y-25])
                else:
                    creature.attackDisplay=False
        for creature in Creature.creatureList:
            if creature.getBlockInContact().lightLevel>0:
                creature.display()

        #CreatureUpdate
        if player.getBlockInContact().pickable:
            player.pick()
        if player.getBlockInContact().blockType==13:
            player.tp=True


        #fireBall
        #print(Creature.allFireBall)
        if Creature.allFireBall!=[]:
            for fireBall in Creature.allFireBall:
                #print("FireBalls:",Creature.allFireBall)
                if not fireBall.explode:
                    fireBall.display()
                if fireBall.explode:
                    #print("Explode")
                    pygame.mixer.Sound.play(FireBall_explode)
                    Creature.allFireBall.remove(fireBall)
                    #print("Explode at",bullet.x,bullet.y)

                    for creature in Creature.creatureList:
                        if creature.creatureType in fireBall.attackType:
                            if (creature.x-fireBall.x)**2+(creature.y-fireBall.y)**2<=(fireBall.collisionRadius+15)**2:
                                creature.health-=fireBall.attackDamage
                                pygame.mixer.Sound.play(hurt)


                    if fireBall.empowered:
                        brekList=[]
                        if fireBall.getBlockInContact().breakable:
                            brekList+=[fireBall.getBlockInContact()]
                        for block in fireBall.getBlockInContact().getAdjacent():
                            if block.breakable:
                               # print("Breaking block at",block.x,block.y)
                                brekList+=[block]
                               # fireBall.brek(block.x//30,block.y//30)
                        if len(brekList)>=3:
                            for x in range(3):
                                breknum=random.randint(0,len(brekList)-1)
                                brekBlock=brekList[breknum]
                                fireBall.brek(brekBlock.x//30,brekBlock.y//30)
                        elif len(brekList)==1:
                            fireBall.brek(brekList[0].x//30,brekList[0].y//30)
                        elif len(brekList)==2:
                            fireBall.brek(brekList[0].x//30,brekList[0].y//30)
                            fireBall.brek(brekList[1].x//30,brekList[1].y//30)

                    del(fireBall)


        for creature in Creature.creatureList:
            if not creature.bossFight:
                if creature.creatureType==1:
                    creature.searchForTarget(player)
                #elif creature.creatureType!=1:
                    #if creature.getBlockInContact().lightLevel>0:




            #print("ZombieType:",creature.creatureType)
            if creature.health<=0:
                pygame.mixer.Sound.play(die)
                creature.die()

        #stamina refill
            if creature.stamina < creature.staminaMax:
                creature.stamina += creature.staminaRegen
            if creature.attackCounter < creature.attackSpeed:
                creature.attackCounter += 1


        #Monster respawn
        if not Creature.bossFight:
            if Creature.zombieCount<15:
                spawnCounter+=1

                if spawnCounter>60:
                    Creature.zombieCount+=1


                    rand=random.randint(0,len(Block.zombieSpawner)-1)
                    print("Spawner pos",rand)
                    spawner=Block.zombieSpawner[rand]
                    if spawner.lightLevel==0:
                        print("spawning zombie at",spawner.x,spawner.y)
                        Creature.creatureList.append(Creature(spawner.x,spawner.y,1,10,1,1))
                        spawnCounter=0
                #print(Creature.reachable(creature.getBlockInContact(),player.getBlockInContact()))


        #bossFight

        if Creature.bossFight:

            if not Creature.started:
                pygame.mixer.music.load("Combat.mp3")
                pygame.mixer.music.play(-1)
                player.keyCount=0
                Creature.creatureList=[player]
                #player.vision+=5
                k=0
                for spawner in Block.bossSpawner:
                    print("spawning boss")
                    boss=Creature(spawner.x,spawner.y,3,10,0,4+k,5)
                    Creature.creatureList.append(boss)
                    Creature.allBoss.append(boss)
                    print("Adding boss",boss.creatureType)
                    k+=1

                screen.fill((0,0,0))
                Creature.started=True
            if Creature.started:
                if Creature.allBoss==[]:
                    Creature.bossFight=False
                    Creature.bossFightEnd=True
                    player.keyCount+=1
                for boss in Creature.allBoss:
                    if boss.health<=0:
                        Creature.allBoss.remove(boss)
                    if boss.superNova:
                        boss.fireCounter+=1
                        if boss.fireCounter>=5:
                            boss.fire()
                            boss.direction+=1
                            boss.fireTime+=1
                            if boss.direction>7:
                                boss.direction-=8
                            boss.fireCounter=0
                            if boss.fireTime>=16:
                                boss.superNova=False
                                boss.powerCounter=0
                    else:
                        boss.standardMoves(player)
                    if not boss.transformed:
                        if boss.health<50:
                            boss.transform()

                    if boss.powerCounter>=boss.powerCoolDown:
                        if boss.creatureType==5:
                            dice=random.randint(0,1)
                            if dice==1:
                                boss.superNova=True
                            elif dice==0:
                                boss.blink(player)

                        elif boss.creatureType == 4:
                            boss.blink(player)
            # player.getBlockInContact().enlighten(player.vision)

        if Creature.bossFightEnd:

            if player.getBlockInContact().blockType==18:
                gameEnd=True
                gameStart=False

        playerInfoDisplay()

    if gameEnd:
        pygame.mixer.music.load("end.mp3")
        pygame.mixer.music.play(-1)
        screen.fill((0,0,0))
        screen.blit(pygame.image.load("Portal_teleportor_ori.jpg"),[0,0])
        screen.blit(pygame.image.load("Portal_receiver_ori.jpg"),[778,388])
        font=pygame.font.Font(None,50)
        text=font.render("You won",True,(255,255,0))
        text_2=font.render("Exit(f)",True,(0,255,0))
        screen.blit(text,[550,400])
        screen.blit(text_2,[570,460])

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_f:
                    run=False



        #print(player.collideType)
    for item in casts:
        broadCast(item)
        casts.remove(item)
    if casting != 0:
        count+=1
        if count<60:
            broadCast(casting,False)
        else:
            casting = 0
            count = 0
            eraseCast()
    pygame.display.flip()
pygame.quit()
