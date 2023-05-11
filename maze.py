from pygame import *

WIDTH,HEIGHT = 880, 525  
FPS = 60


point = 0 
mixer.init()
mixer.music.load('PacMan_musik.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()

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
        old_pos = self.rect.x, self.rect.y  
        pressed = key.get_pressed()
        if pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= 3
        if pressed[K_DOWN] and self.rect.y < HEIGHT - 70:
            self.rect.y += 3
        if pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 3
        if pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += 3
        for w in walls:
            if sprite.collide_rect(self, w):
                self.rect.x, self.rect.y = old_pos


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
        super().__init__("Wallpm.jpg", x, y, width = 35, height = 35)


bg = transform.scale(image.load("background_PM.jpg"), (WIDTH, HEIGHT))
player = Player("PacManSprite.png", x = 40, y = 350, width = 30, height = 30)

class Fruit(GameSprite):
    def __init__(self, x, y):
        super().__init__("fruit.png", x, y, width = 30, height = 30)

fruits = []

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
            elif symbol == 'o':
                fruits.append(Fruit(x,y))
                
 
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

        for fruit in fruits:
            fruit.draw()

            if sprite.collide_rect(player, fruit):
                fruits.remove(fruit)

            

        for e in enemys:
            e.update(walls)
            e.draw()
            if sprite.collide_rect(player, e):
                result = font1.render("YOU LOSE!", True, (238, 255, 148))
                window.blit(result, (250,200))
                finish = True
                

            

        player.draw()

        points_text = font1.render("Рахунок" + str(points), True,(255,255,255))

    display.update()
    clock.tick(FPS)