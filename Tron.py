import pygame
pygame.init()


screenWidth = 500
screenHeight = 500
clock = pygame.time.Clock()
win = pygame.display.set_mode((screenWidth,screenHeight))
radius = 5
vel = 5
painted = set()
chars = None
keys = None
run = None

pygame.display.set_caption("Tron")



class character(object):
    def __init__(self, x, y, color, direction, keyBinds, name):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.keyBinds = keyBinds
        self.name = name #DEBUG#
        self.rect = None
        self.dead = False
        self.reward = 0
        
    def changeDirection(self, keys):
        if keys[self.keyBinds[0]] and self.direction != 'r': 
            self.direction = 'l'
        elif keys[self.keyBinds[1]] and self.direction != 'l':
            self.direction = 'r'
        elif keys[self.keyBinds[2]] and self.direction != 'd':
            self.direction = 'u'
        elif keys[self.keyBinds[3]] and self.direction != 'u':
            self.direction = 'd'

    def move(self, vel):
        if self.direction == 'l':
            self.x -= vel
        elif self.direction == 'r':
            self.x += vel
        elif self.direction == 'u':
            self.y -= vel
        elif self.direction == 'd':
            self.y += vel

    def checkDead(self, radius, screenWidth, screenHeight, chars, painted):
        if (self.x < 0) or (self.x + radius > screenWidth) or (self.y < 0) or (self.y + radius > screenWidth):
            self.dead = True
        
        for char in chars:
            if self != char:
                if self.rect.colliderect(char.rect):
                    self.dead = True
                    
        for point in painted:
            if point == (self.x / radius, self.y / radius):
                self.dead = True



                    
chars = [
    character(480, 250, (255,0,0), 'l', (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN), 'Red'),
    character(20, 250, (0,255,0), 'r', (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s), 'Green'),
    #character(250, 20, (0,0,255), 'd', (pygame.K_g, pygame.K_j, pygame.K_y, pygame.K_h), 'Blue')
    ]
run = True

#main loop
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()



    for char in chars:
        painted.add((char.x / radius, char.y / radius))
        char.changeDirection(keys)
        char.move(vel)
        char.rect = pygame.Rect(char.x, char.y, radius, radius)
        pygame.draw.rect(win, char.color, (char.x, char.y, radius, radius))
        
    for char in chars:
        char.checkDead(radius, screenWidth, screenHeight, chars, painted)
        if char.dead:
            char.reward -= 10
            print(char.name, char.reward) #DEBUG#
    chars[:] = [char for char in chars if not char.dead]
        

    if len(chars) <= 1:
        if len(chars) == 1:
            chars[0].reward += 10
            print(chars[0].name, chars[0].reward) #DEBUG#
        run = False

    
    pygame.display.update()



pygame.quit()
