import pygame
from pygame.locals import *

class Player():
    def __init__(self, pos=(0,0), size=50):
        self.pos = pos
        self.size = size
        '''
        Directions
            1
        4       2
            3
        '''
        self.direction = 1
        self.vertical_movement = True
        self.last_shot_time = 0
        self.shoot_cooldown_time = 1

        

        # TODO Temp DELETE LATER
        self.color = pygame.Color(255,0,255)
        self.surface = self.update_surface()

    def move(self, dir):
        speed = 5
        self.direction = dir
        match dir:
            case 1:
                self.pos = (self.pos[0], self.pos[1] - speed)
            case 2:
                self.pos = (self.pos[0] + speed, self.pos[1])
            case 3:
                self.pos = (self.pos[0], self.pos[1] + speed)
            case 4:
                self.pos = (self.pos[0] - speed, self.pos[1])
    
    def update_surface(self):
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.color)
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, self.pos)
        
class Projectile():
    def __init__(self, source):
        self.source = source
        self.long_side_size = 20
        self.speed = 15
        self.is_active = True

        '''
        Directions
            1
        4       2
            3
        '''
        self.direction = source.direction
        match self.direction:
            case 1:
                self.size = (self.long_side_size / 2, self.long_side_size)
                self.pos = (source.pos[0] + source.size / 2 - self.long_side_size / 4, source.pos[1] - self.long_side_size - 1)
            case 2:
                self.size = (self.long_side_size, self.long_side_size / 2)
                self.pos = (source.pos[0] + source.size + 1, source.pos[1] + source.size / 2 - self.long_side_size / 4)
            case 3:
                self.size = (self.long_side_size / 2, self.long_side_size)
                self.pos = (source.pos[0] + source.size / 2 - self.long_side_size / 4, source.pos[1] + source.size + 1)
            case 4:
                self.size = (self.long_side_size, self.long_side_size / 2)
                self.pos = (source.pos[0] - self.long_side_size - 1, source.pos[1] + source.size / 2 - self.long_side_size / 4)

        self.color = pygame.Color(255,255,255)
        self.surface = self.update_surface()

    def move(self):
        match self.direction:
            case 1:
                self.pos = (self.pos[0], self.pos[1] - self.speed)
            case 2:
                self.pos = (self.pos[0] + self.speed, self.pos[1])
            case 3:
                self.pos = (self.pos[0], self.pos[1] + self.speed)
            case 4:
                self.pos = (self.pos[0] - self.speed, self.pos[1])

    
    def update_surface(self):
        surf = pygame.Surface(self.size)
        surf.fill(self.color)
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, self.pos)

class Wall():
    def __init__(self, pos=(0,0), size=50):
        self.pos = pos
        self.size = (size, size)
        self.is_active = True
        
        self.color = pygame.Color(120,0,0)
        self.surface = self.update_surface()
    
    def update_surface(self):
        surf = pygame.Surface(self.size)
        surf.fill(self.color)
        return surf
    
    def get_hit(self, direction):
        match direction:
            case 1:
                self.size = (self.size[0], self.size[1] - 10)
            case 2:
                self.size = (self.size[0] - 10, self.size[1])
                self.pos = (self.pos[0] + 10, self.pos[1])
            case 3:
                self.size = (self.size[0], self.size[1] - 10)
                self.pos = (self.pos[0], self.pos[1] + 10)
            case 4:
                self.size = (self.size[0] - 10, self.size[1])
        if self.size[0] == 0 or self.size[1] == 0:
            self.is_active = False
        self.surface = self.update_surface()
        
            
    def draw(self, surface):
        surface.blit(self.surface, self.pos)

def check_collission_wall(proj, wall):
    # left wall
    if (proj.pos[0] < wall.pos[0] + wall.size[0]) and (proj.pos[0] + proj.size[0] > wall.pos[0]) and (proj.pos[1] < wall.pos[1] + wall.size[1]) and (proj.pos[1] + proj.size[1] > wall.pos[1]):
        proj.is_active = False
        wall.get_hit(proj.direction)
    #    pass

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
    resolution = (750, 750)
    screen = pygame.display.set_mode(resolution)
    screen.fill(pygame.Color(0, 0, 0))

    clock = pygame.time.Clock()
    dt = 0
    
    player = Player()
    

    projectile_list = []
    wall_list = []
    wall_list.append(Wall(pos=(200,200)))

    running = True

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (K_UP, K_DOWN):
                    player.vertical_movement = True
                elif event.key in (K_LEFT, K_RIGHT):
                    player.vertical_movement = False
                elif event.key == K_SPACE:
                    current_time = pygame.time.get_ticks() / 1000
                    if current_time >= player.last_shot_time + player.shoot_cooldown_time:
                        player.last_shot_time = current_time
                        projectile_list.append(Projectile(player))
            
        # TODO: Some game logic
        handle_movement(player, player.vertical_movement)
        for idp, projectile in enumerate(projectile_list):
            for idw, wall in enumerate(wall_list):
                check_collission_wall(projectile, wall)
                if not wall.is_active:
                    del wall_list[idw]
            if not projectile.is_active:
                del projectile_list[idp]
        for projectile in projectile_list:
            projectile.move()
        
        
        
        # Render & Display
        screen.fill(pygame.Color(0,0,0))
        player.draw(screen)
        for wall in wall_list:
            wall.draw(screen)
        for projectile in projectile_list:
            projectile.draw(screen)

        pygame.display.flip()
        dt = clock.tick(24)
    pygame.quit()


if __name__ == "__main__":
    main()