import lib
import pygame
from pygame.locals import (
    K_RETURN,
    KEYDOWN,
    K_ESCAPE,
    QUIT,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_SPACE
)
defaultVisible = 30
# Set up the drawing window
gridsize = 21
SCREEN_WIDTH = defaultVisible * gridsize
SCREEN_HEIGHT = defaultVisible * gridsize
spritesize = int(gridsize)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
origin = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))


dudes = []  # list of sprite objects

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((spritesize, spritesize))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

        self.healthbar_surf = pygame.Surface((spritesize, int(0.2*spritesize)))
        self.healthbar_surf.fill((240, 33, 33)) # make the health bar red
        self.healthbar_rect = self.healthbar_surf.get_rect()
        self.max_hp = -1  # initiate w/ impossible value
        self.hp = self.max_hp
        self.info = []
        self.zcoord = 0
        self.agent = None

    def assign_Agent(self, agent):
        self.agent = agent
        self.agent.assign_Sprite(self)

    def fly(self):
        if self.zcoord > 0:
            pygame.draw.polygon(screen, (255, 255, 255), [(self.rect.left-2, self.rect.top-2), (self.rect.right, self.rect.top -2), self.rect.bottomright, (self.rect.left-2, self.rect.bottom), (self.rect.left-2, self.rect.top-2)], 2)

    def update(self, pressed_keys):

        # take in position from agent and move there
        pos = tile_to_px(self.agent.pos)
        self.rect.left = pos[0]
        self.rect.top = pos[1]
        self.zcoord = pos[2]

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, gridsize)
            self.agent.pos[1] -= 1
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1*gridsize)
            self.agent.pos[1] += 1
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1*gridsize, 0)
            self.agent.pos = lib.add(self.agent.pos, (-1, 0, 0))
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(gridsize, 0)
            self.agent.pos = lib.add(self.agent.pos, (1, 0, 0))

        # get max hp but only once
        if self.max_hp == -1:
            self.max_hp = self.agent.HP_max
        EntitySize =lib.tileSize(self.agent.Size)
        # get health from agent and update bar
        self.hp = self.agent.HP_now
        self.surf =  pygame.Surface((spritesize*EntitySize-2,spritesize*EntitySize-2))
        if self.agent.team:
            dudes[-1].surf.fill((0, 0, 255))
        else:
            dudes[-1].surf.fill((33, 240, 33))

        self.healthbar_surf = pygame.Surface((max((EntitySize * spritesize * self.hp / self.max_hp)-2, 2), int(0.2 * EntitySize *spritesize)))
        self.healthbar_surf.fill((240, 33, 33))
        self.healthbar_rect = self.healthbar_surf.get_rect()
        self.healthbar_rect.topleft = self.rect.topleft

        if self.hp < 1:
            dudes.remove(self)

def tile_to_px(tup):
    new_x = SCREEN_WIDTH + 2 + tup[0]*gridsize  - origin[0]
    new_y = SCREEN_HEIGHT + 2 - tup[1]*gridsize - origin[1]
    return [new_x, new_y, tup[2]]


def px_to_tile(tup):
    new_x = (tup[0]-SCREEN_WIDTH-2+origin[0])/gridsize
    new_y = -1*(tup[1]-SCREEN_HEIGHT-2+origin[1])/gridsize
    return [new_x, new_y, tup[2]]


def refresh():
    pressed_keys = pygame.key.get_pressed()
    for dude in dudes:
        dude.update(pressed_keys)
    screen.fill((200, 200, 200))

    # Draw gridlines
    for i in range(int(SCREEN_WIDTH / gridsize)+gridsize):
        pygame.draw.line(screen, (150, 150, 150), (i * gridsize, 0), (i * gridsize, SCREEN_HEIGHT))
        #draw darker lines every screen size to show movement
        if px_to_tile((i*gridsize+2, 0, 0))[0] % (SCREEN_WIDTH / gridsize) == 0:
            pygame.draw.line(screen, (50, 50, 50), (i*gridsize, 0), (i*gridsize, SCREEN_HEIGHT), 2)
    for i in range(int(SCREEN_HEIGHT / gridsize)+gridsize):
        pygame.draw.line(screen, (150, 150, 150), (0, i * gridsize), (SCREEN_WIDTH, i * gridsize))
        #draw darker lines every screen size to show movement
        if px_to_tile((0, i*gridsize+2, 0))[1] % (SCREEN_HEIGHT / gridsize) == 0:
            pygame.draw.line(screen, (50, 50, 50), (0, i * gridsize), (SCREEN_WIDTH, i * gridsize), 2)

    # Draw dudes
    for dude in dudes:
        screen.blit(dude.surf, dude.rect)
        screen.blit(dude.healthbar_surf, dude.healthbar_rect)
        dude.fly()
    #if pressed_keys[K_SPACE]:
     #   recenter()
      #  pygame.time.delay(200)
    recenter()
    pygame.display.flip()

    # Allow for pausing, exiting, etc.
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE or event.key == K_RETURN:
                raise customStopIteration
        elif event.type == QUIT:
            raise customStopIteration

def attacklaser(origin, target, attack):
    # Draw line from self to target
    print(f"{origin.sprite.name} attacking {target.sprite.name} with its {attack.call.__name__}.")
    print(f"\t This {attack.call.__name__} attack went from {origin.pos} to {target.pos}, a distance of {lib.dist(origin, target)}")
    refresh()
    pygame.draw.line(screen, (240, 33, 33), origin.sprite.rect.center, target.sprite.rect.center, 2)
    pygame.draw.line(screen, (240, 33, 33),
                            (target.sprite.rect.centerx - gridsize / 4,
                             target.sprite.rect.centery - gridsize / 4),
                            (target.sprite.rect.centerx + gridsize / 4,
                             target.sprite.rect.centery + gridsize / 4), 4)
    pygame.draw.line(screen, (240, 33, 33),
                            (target.sprite.rect.centerx - gridsize / 4,
                             target.sprite.rect.centery + gridsize / 4),
                            (target.sprite.rect.centerx + gridsize / 4,
                             target.sprite.rect.centery - gridsize / 4), 4)
    pygame.draw.circle(screen, (250, 33, 33), origin.sprite.rect.center, gridsize / 4, 4)
    pygame.display.flip()
    clock.tick(20*lib.SimSpeed)  # delay necessary to see the laser

class customStopIteration(Exception):
    pass

def recenter():
    global origin
    if pygame.time.get_ticks() > 10000:
        x = y = 0
        teams = lib.redTeam + lib.blueTeam
        for dude in teams:
            x += dude.sprite.rect.left - 2 
            y += dude.sprite.rect.top - 2 
        
        x = gridsize * ((x // len(teams) - SCREEN_WIDTH // 2 + origin[0]) // gridsize) if len(teams) else 0
        y = gridsize * ((y // len(teams) - SCREEN_HEIGHT // 2 + origin[1]) // gridsize) if len(teams) else 0
        origin = (x, y)
    
    
