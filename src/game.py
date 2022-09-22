#Jan Kopejtko, 2022

build_number = 1.0

import pygame
import sys

class GameObject: #constructor of GameObject class
    def __init__(self, Y, canMoveUp = False, canMoveDown = False, X = 0, direction = None):
        self.canMoveUp = canMoveUp
        self.canMoveDown = canMoveDown
        self.X = X
        self.Y = Y
        direction = direction
class ball: #constructor of ball class
    def __init__(self, color, speed, width, radius, X, Y, X_modulator, Y_modulator):
        self.color = color
        self.speed = speed
        self.width = width
        self.radius = radius
        self.X = X
        self.Y = Y
        self.X_modulator = X_modulator
        self.Y_modulator = Y_modulator
def drawDottedLine(surface, surface_width, color, start_pos_y, end_pos_y, width, gap_length, dot_length):
    y = start_pos_y
    x_pos = surface_width/2
    for i in range(0, end_pos_y):
        pygame.draw.line(surface, color, (x_pos, y), (x_pos, y+dot_length), width=width)
        y = y + gap_length
def main():
    #game setup dialog
    maxPoints = 0
    speed = 0
    while True:
        try:
            maxPoints = int(input("input amount of winning points in range 1-100\n"))
            ball_speed = int(input("input speed of ball in range 1-10\n"))
            speed = int(input("input player speed in range 1-30\n"))
        except:
            print("something went wrong, please try again...")
            continue
        if maxPoints > 100 or maxPoints < 1:
            print("please enter valid number of points")
            print("maximum number of points is 100")
            continue
        if ball_speed > 10 or ball_speed < 1:
            print("please enter valid speed of ball")
            print("maximum speed of ball is 10")
            continue
        if speed > 30 or speed < 1:
            print("please enter valid player speed")
            print("maximal player speed is 30")
            continue
        else:
            print("starting game...")
            break
    pygame.init()
    # game
    pygame.display.set_caption('PING PONG')
    window = pygame.display.set_mode((0, 0), pygame.WINDOWMAXIMIZED)
    width, height = window.get_size()
    backgroundColor = [50,10,50] # <-- purple
    pong = False # <-- game variable logic to count player/enemy points
    #text
    font = pygame.font.SysFont(None, 25)
    FontDescription = pygame.font.SysFont(None, 15)
    # player
    playerColor = [255,255,255] # <-- white
    playerHeigh = 100
    playerWidth = 10
    speed = speed/10
    pixel_move_count = 0.5
    player_canMoveUp = False
    player_canMoveDown = False
    player_pos_y = height/2 - playerHeigh/2 # <-- calculate player X position
    playerscore = 0
    # enemy
    pixel_move_count_enemy = 0.3
    enemy_canMoveUp = True
    enemy_canMoveDown = False
    enemy_pos_y = height/2 - playerHeigh/2 # <-- calculate enemy Y position
    enemy_pos_x = width - playerWidth
    enemy_direction = True
    enemyscore = 0
    # ball
    ballColor = playerColor # <-- set base color of game ball
    ball_speed = ball_speed/20
    ball_width = 7
    ball_radius = 5
    ball_X = width/2
    ball_Y = height/2
    ball_X_modulator = 1
    ball_Y_modulator = 1
    # setup
    window.fill(backgroundColor) # <-- background color
    while True:
        keys = pygame.key.get_pressed() # <-- get keys input from keyboard
        window.fill(backgroundColor)
    # check win
        if playerscore >= maxPoints:
            print("you win")
            break
        elif enemyscore >= maxPoints:
            print("you lose")
            break
    # check bound player
        player_canMoveDown = player_pos_y < height - playerHeigh
        player_canMoveUp = player_pos_y >= 0
    # check bound enemy
        enemy_canMoveDown = enemy_pos_y <= height - playerHeigh
        enemy_canMoveUp = enemy_pos_y >= 0
    # check bound ball
        # left
        if ball_X < 1:
            ball_X_modulator = -ball_X_modulator
            if not pong:
                enemyscore = enemyscore + 1
        # right
        if ball_X >= width - ball_width: 
            ball_X_modulator = -ball_X_modulator
            if not pong:
                playerscore = playerscore + 1
        #top
        if ball_Y <= 0: 
            ball_Y_modulator = -ball_Y_modulator
            pong = False
        #bottom
        if ball_Y >= height - ball_width: 
            ball_Y_modulator = -ball_Y_modulator
            pong = False
        #primitive "AI" logic
        if not enemy_canMoveUp:
            enemy_direction = False
            enemy_canMoveUp = False
            enemy_canMoveDown = True
        elif not enemy_canMoveDown:
            enemy_direction = True
            enemy_canMoveUp = True
            enemy_canMoveDown = False
        #player control
        if player_canMoveDown and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            player_pos_y = player_pos_y + pixel_move_count * speed
        elif player_canMoveUp and (keys[pygame.K_UP] or keys[pygame.K_w]):
            player_pos_y = player_pos_y - pixel_move_count * speed
        #enemy movment
        if enemy_canMoveUp and enemy_direction:
            enemy_pos_y = enemy_pos_y - pixel_move_count_enemy*speed
        elif enemy_canMoveDown and not enemy_direction:
            enemy_pos_y = enemy_pos_y + pixel_move_count_enemy*speed
        #
        if ball_X <= playerWidth and ball_Y > player_pos_y and ball_Y <= player_pos_y + playerHeigh and not pong:
            ball_X_modulator = -ball_X_modulator
            pong = True
        elif ball_X >= (width - playerWidth) and ball_Y > enemy_pos_y and ball_Y <= enemy_pos_y + playerHeigh and not pong:
            ball_X_modulator = -ball_X_modulator
            pong = True
        # move ball
        ball_X = ball_X + ball_X_modulator * ball_speed # move based on modulation of x axis
        ball_Y = ball_Y + ball_Y_modulator * ball_speed # move based on modulation of y axis
        # end of loop rendering
        player = pygame.draw.rect(window, playerColor,[0, player_pos_y, playerWidth, 100], 0) # <-- render player
        enemy = pygame.draw.rect(window, playerColor,[enemy_pos_x, enemy_pos_y, playerWidth, 100], 0) # <-- render enemy
        ball = pygame.draw.circle(window, ballColor,center=(ball_X,ball_Y), radius = ball_radius, width=ball_width) # <-- render ball    
        line2 = drawDottedLine(window, width, playerColor, -5 , height, 3, 20, 10) #<--render dotted line
        #show score
        playerScore = font.render('score: ' + str(playerscore), True, [255,255,255])
        enemyScore = font.render('score: ' + str(enemyscore), True, [255,255,255])
        #show credits
        credits = FontDescription.render('Jan Kopejtko, 2022', True, [255,255,255])
        build = FontDescription.render('build number ' + str(build_number), True, [255,255,255])
        window.blit(credits, (5,height - credits.get_height() - 5))
        window.blit(build, (width - build.get_width() - 5,height - build.get_height() - 5))
        window.blit(playerScore, (20, 20))
        window.blit(enemyScore, (width - enemyScore.get_width() - 20, 20))
        
        pygame.display.update() # <-- fill window with created objects
        # on exit event loops
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # <-- exit game based on pressed key
                print("shuting down...")
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
if __name__ == '__main__':
    main()