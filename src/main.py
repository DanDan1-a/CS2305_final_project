import pygame
from pygame.locals import *

class Player():
    def __init__(self, pos=(0,0), size=15):
        self.pos = pos
        self.size = size
        '''
        Directions
            1
        4       2
            3
        '''
        self.direction = 1

        # TODO Temp DELETE LATER
        self.color = pygame.Color(255,255,255)
        self.surface = self.update_surface()

    def move(self, dir):
        speed = 5
        self.set_direction(dir)
        match dir:
            case 1:
                self.pos = (self.pos[0], self.pos[1] - speed)
            case 2:
                self.pos = (self.pos[0] + speed, self.pos[1])
            case 3:
                self.pos = (self.pos[0], self.pos[1] + speed)
            case 4:
                self.pos = (self.pos[0] - speed, self.pos[1])
        
    def set_direction(self, dir):
        self.direction = dir
    
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.color)
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, self.pos)


def handle_movement(player, vertical_movement):
    key_pressed = pygame.key.get_pressed()
    if vertical_movement:
        if key_pressed[K_UP]:
            player.move(1)
        if key_pressed[K_DOWN]:
            player.move(3)
    else:
        if key_pressed[K_RIGHT]:
            player.move(2)
        if key_pressed[K_LEFT]:
            player.move(4)





def main():
    pygame.init()
    pygame.display.set_caption("Tank Game")
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    screen.fill(pygame.Color(0, 0, 0))

    clock = pygame.time.Clock()
    dt = 0
    
    player = Player()
    vertical_movement = True
    
    running = True
    new_direction = 1

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (K_UP, K_DOWN):
                    vertical_movement = True
                elif event.key in (K_LEFT, K_RIGHT):
                    vertical_movement = False
            

        

        # TODO: Some game logic
        handle_movement(player, vertical_movement)

        # Render & Display
        screen.fill(pygame.Color(0, 0, 0))
        player.draw(screen)

        pygame.display.flip()
        dt = clock.tick(24)
    pygame.quit()


if __name__ == "__main__":
    main()