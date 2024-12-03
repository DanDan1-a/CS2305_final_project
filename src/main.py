import pygame
import random

from pygame.locals import *
'''
        Directions
            1
        4       2
            3
'''

class Player():
    def __init__(self, pos=(0,0), size=50):
        self.pos = pos
        self.last_pos = self.pos
        self.size = (size, size)
        
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
        self.last_pos = self.pos
        match dir:
            case 1:
                self.pos = (self.pos[0], self.pos[1] - speed)
            case 2:
                self.pos = (self.pos[0] + speed, self.pos[1])
            case 3:
                self.pos = (self.pos[0], self.pos[1] + speed)
            case 4:
                self.pos = (self.pos[0] - speed, self.pos[1])
    
    def cancel_move(self):
        self.pos = self.last_pos
    
    def update_surface(self):
        surf = pygame.Surface(self.size)
        surf.fill(self.color)
        return surf
    
    def draw(self, surface):
        surface.blit(self.surface, self.pos)
        
class Projectile():
    def __init__(self, source, is_enemy_projectile = False):
        self.source = source
        self.long_side_size = 20
        self.speed = 15
        self.is_active = True
        self.is_enemy_projectile = is_enemy_projectile
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
                self.pos = (source.pos[0] + source.size[1] / 2 - self.long_side_size / 4, source.pos[1] - self.long_side_size - 1)
            case 2:
                self.size = (self.long_side_size, self.long_side_size / 2)
                self.pos = (source.pos[0] + source.size[1] + 1, source.pos[1] + source.size[1] / 2 - self.long_side_size / 4)
            case 3:
                self.size = (self.long_side_size / 2, self.long_side_size)
                self.pos = (source.pos[0] + source.size[1] / 2 - self.long_side_size / 4, source.pos[1] + source.size[1] + 1)
            case 4:
                self.size = (self.long_side_size, self.long_side_size / 2)
                self.pos = (source.pos[0] - self.long_side_size - 1, source.pos[1] + source.size[1] / 2 - self.long_side_size / 4)

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

class Scanner():
    def __init__(self, parent, scanner_is_vertical=True, scanner_is_second=False):
        self.pos = (parent.pos[0]+parent.size[0]/2-5,parent.pos[1]+parent.size[1]/2-5)
        if scanner_is_vertical:
            self.size = (10,900)
            if scanner_is_second:
                self.pos = (self.pos[0],self.pos[1] - 900)
        else:
            self.size = (900,10)
            if scanner_is_second:
                self.pos = (self.pos[0] - 900,self.pos[1])
        
        self.is_active = True
        
        # Debug color
        self.color = pygame.Color(20,20,20)
        self.surface = self.update_surface()
    
    
    
    def update_surface(self):
        surf = pygame.Surface(self.size)
        surf.fill(self.color)
        return surf

    def draw(self, surface):
        surface.blit(self.surface, self.pos)

class Enemy():
    def __init__(self, pos=(0,0), size=50):
        self.pos = pos
        self.last_pos = self.pos
        self.size = (size, size)
        self.speed = 5
        
        self.direction = 3
        self.vertical_movement = True

        self.time_last_detection = 0
        self.time_last_shot = 0

        self.time_reaction_min = 1
        self.time_reaction_max = 3
        self.time_reaction_cur = 3

        self.shoot_cooldown_time_min = 1
        self.shoot_cooldown_time_max = 3
        self.shoot_cooldown_time_cur = 1

        self.has_detected = False
        self.is_agressive = False
        self.agressive_side = 0

        self.scanner_list = []
        self.scanner_list.append(Scanner(self, True, True))     # 0 - Up
        self.scanner_list.append(Scanner(self, False, False))   # 1 - Right
        self.scanner_list.append(Scanner(self, True, False))    # 2 - Down
        self.scanner_list.append(Scanner(self, False, True))    # 3 - Left
        
        # TODO Temp DELETE LATER
        self.color = pygame.Color(255,0,0)
        self.surface = self.update_surface()

    def move(self):
        self.last_pos = self.pos
        match self.direction:
            case 1:
                self.pos = (self.pos[0], self.pos[1] - self.speed)
            case 2:
                self.pos = (self.pos[0] + self.speed, self.pos[1])
            case 3:
                self.pos = (self.pos[0], self.pos[1] + self.speed)
            case 4:
                self.pos = (self.pos[0] - self.speed, self.pos[1])
        collision_check_flag = check_collission(self, player) or not is_in_bounds(self)
        if not collision_check_flag:
            for wall in wall_list:
                if check_collission(self, wall):
                    collision_check_flag = True
                    break
        if collision_check_flag:
            self.cancel_move()
        else:
            match self.direction:
                case 1:
                    self.move_scanners(0, 0-self.speed)
                case 2:
                    self.move_scanners(self.speed, 0)
                case 3:
                    self.move_scanners(0, self.speed)
                case 4:
                    self.move_scanners(0-self.speed, 0)
        return collision_check_flag  
    
    def move_scanners(self, x_change, y_change):
        for scanner in self.scanner_list:
            scanner.pos = (scanner.pos[0] + x_change, scanner.pos[1] + y_change)

    def cancel_move(self):
        self.pos = self.last_pos
    
    def update_surface(self):
        surf = pygame.Surface(self.size)
        surf.fill(self.color)
        return surf
    
    def draw_scanners(self, surface):
        for scanner in self.scanner_list:
            scanner.draw(surface)

    def draw(self, surface):
        self.draw_scanners(surface)
        surface.blit(self.surface, self.pos)

    def roam(self):
        pass

    def shoot(self, time):
        current_time = time / 1000
        if current_time >= self.time_last_shot + self.shoot_cooldown_time_cur:
            self.time_last_shot = current_time
            self.shoot_cooldown_time_cur = random.randint(self.shoot_cooldown_time_min, self.shoot_cooldown_time_max)
            projectile_list.append(Projectile(self))

    def act(self, time):
        if self.is_agressive:
            self.direction = self.agressive_side
            self.move()
            self.shoot(time)
            if 
        has_detected_tick = False
        for id, scanner in enumerate(self.scanner_list):
            if check_collission(player, scanner):
                has_detected_tick = True
                
                if not self.has_detected:
                    self.has_detected = True
                    self.time_last_detection = time / 1000
                    self.time_reaction_cur = random.randint(self.time_reaction_min, self.time_reaction_max)
                else:
                    if time / 1000 >= self.time_last_detection + self.time_reaction_cur:
                        self.is_agressive = True
                        self.agressive_side = id + 1
                

        if not has_detected_tick:
            self.has_detected = False
            self.is_agressive = False
                    

                    

wall_list = []
player = Player()
projectile_list = []
enemy_list = []

def check_collission(object1, object2):
    return (object1.pos[0] < object2.pos[0] + object2.size[0])  and (object1.pos[0] + object1.size[0] > object2.pos[0]) and (object1.pos[1] < object2.pos[1] + object2.size[1]) and (object1.pos[1] + object1.size[1] > object2.pos[1])

def is_in_bounds(object):
    return (object.pos[0]>=0) and (object.pos[0]+object.size[0]<750) and (object.pos[1]>=0) and (object.pos[1]+object.size[1]<750)

def check_collission_wall(proj, wall):
    if (check_collission(proj, wall)):
        proj.is_active = False
        wall.get_hit(proj.direction)

def handle_movement(vertical_movement):
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
    if not is_in_bounds(player):
        player.cancel_move()

    for wall in wall_list:
        if(check_collission(player, wall)):
            player.cancel_move()

def draw_everything(screen):
    player.draw(screen)
    
    for projectile in projectile_list:
        projectile.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    for wall in wall_list:
        wall.draw(screen)
    

def setup_map():
    pass


def main():
    pygame.init()
    pygame.display.set_caption("Tank Game")
    resolution = (750, 750)
    screen = pygame.display.set_mode(resolution)
    screen.fill(pygame.Color(0, 0, 0))

    clock = pygame.time.Clock()
    dt = 0
    
    wall_list.append(Wall(pos=(200,200)))
    enemy_list.append(Enemy(pos=(350,400)))

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
                elif event.key == K_SPACE: # Player shooting
                    current_time = pygame.time.get_ticks() / 1000
                    if current_time >= player.last_shot_time + player.shoot_cooldown_time:
                        player.last_shot_time = current_time
                        projectile_list.append(Projectile(player))
            
        # Game logic
        handle_movement(player.vertical_movement)
        for idp, projectile in enumerate(projectile_list):
            for idw, wall in enumerate(wall_list):
                check_collission_wall(projectile, wall)
                if not wall.is_active:
                    del wall_list[idw]
            if not projectile.is_active:
                del projectile_list[idp]
        for projectile in projectile_list:
            projectile.move()

        for enemy in enemy_list:
            enemy.act(pygame.time.get_ticks())
        
        # Render & Display
        screen.fill(pygame.Color(0,0,0))
        draw_everything(screen)

        pygame.display.flip()
        dt = clock.tick(24)
    pygame.quit()


if __name__ == "__main__":
    main()