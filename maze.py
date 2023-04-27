from pygame import *

WIDTH,HEIGHT = 700, 525  
FPS = 60

mixer.init()
mixer.music.load('PacMan_musik.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()
kick = mixer.Sound('kick.ogg')
kick.play()

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Пакмен")

class GameSprite(sprite.Sprite):
    def __init__(self,sprite_image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        if pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= 3
        if pressed[K_DOWN] and self.rect.y < HEIGHT - 70:
            self.rect.y += 3
        if pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 3
        if pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += 3
    
class Enemy(GameSprite):
    def __init__(self, x, y, speed=3):
        super().__init__("Ghost.png", x, y, 30, 30)
        self.speed = speed

    def update(self, walls):
        for w in walls:
            if sprite.collide_rect(self, w):
                self.speed = self.speed * -1

        self.rect.x += self.speed
        
      
class Wall(GameSprite):
    def __init__(self, x, y):
        super().__init__("PacMan_map.png", x, y, width = 35, height = 35)


bg = transform.scale(image.load("bacground_PacMan.png"), (WIDTH, HEIGHT))
player = Player("PacManSprite.png", x = 40, y = 350, width = 30, height = 30)


walls = []
enemys = []

with open('map.txt', 'r') as file:
    map = file.readlines()
    x, y = 0, 0
    for line in map:
        for symbol in line:
            if symbol == 'W':
                walls.append(Wall(x,y))
            elif  symbol == "S":
                player.rect.x = x
                player.rect.y = y
                
            elif symbol == "E":
                enemys.append(Enemy(x,y))
            elif symbol == '.':
                coins.append(Coins(x,y))
                
 
            x+=35
        y += 35
        x = 0

run = True
finish = False
clock = time.Clock()

font.init()
font1 = font.SysFont("Impact", 50)
result = font1.render("YOU LOSE", True, (238, 255, 148))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        player.update()
        window.blit(bg, (0, 0))

        for wall in walls:
            wall.draw()
            if sprite.collide_rect(player, wall):
                result = font1.render("YOU LOSE!", True, (238, 255, 148))
                window.blit(result, (250,200))
                finish = True


        for e in enemys:
            e.update(walls)
            e.draw()
            if sprite.collide_rect(player, e):
                result = font1.render("YOU LOSE!", True, (238, 255, 148))
                window.blit(result, (250,200))
                finish = True
                money.play()

            

        player.draw()

    display.update()
    clock.tick(FPS)