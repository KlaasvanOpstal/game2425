#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32

ball_x = 0
ball_speed_x = 10
ball_y = 0
ball_speed_y = 6
paddle_x = ((SCREEN_WIDTH / 2) - (PADDLE_WIDTH / 2))
paddle_y = SCREEN_HEIGHT - 100
game_status_msg = ''
game_status = 'start'

# lijsten met coordinaten van bricks
bricks_x = [200, 296, 392, 484, 200, 296, 392, 484, 200, 296, 392, 484, 696, 792, 888, 984, 696, 792, 888, 984, 696, 792, 888, 984]
bricks_y = [100, 100, 100, 100, 132, 132, 132, 132, 164, 164, 164, 164, 100, 100, 100, 100, 132, 132, 132, 132, 164, 164, 164, 164]

# variabele voor score-display
score = 0
nr_blocks = len(bricks_x)
score_msg = ''

#
# init game
#

pygame.init()
font = pygame.font.SysFont('default', 32)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

# plaatje ball inladen
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

#plaatje paddle inladen
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) 

#plaatje blok inladen
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  
brick_img.blit(spritesheet, (0, 0), (0, 130, 384, 128))   
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) 

#
# game loop
#

print('mygame is running')
running = True
while running:
    # clear screen
    screen.fill('black') 
    
    #
    # read events
    # 
    for event in pygame.event.get(): 
      if event.type == pygame.QUIT:  
        running = False 
    keys = pygame.key.get_pressed() 

    if game_status == 'start':
      game_status_msg = 'Start het spel met [S]. Bestuur de paddle met [A] en [D]'

      if keys[pygame.K_s]:
        game_status = 'game'
        game_status_msg = ''

    if game_status == 'game':
      # 
      # move everything
      #

      # move ball
      ball_x = ball_x + ball_speed_x
      ball_y = ball_y + ball_speed_y
    
      # ball stuitert tegen randen scherm
      if ball_x < 0: 
        ball_speed_x = abs(ball_speed_x) 
      if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1
      if ball_y < 0:
        ball_speed_y = abs(ball_speed_y)
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        ball_speed_y = abs(ball_speed_y) * -1   

      # ball stuitert tegen plank
      if (ball_x + BALL_WIDTH  > paddle_x and
          ball_x < paddle_x + PADDLE_WIDTH and
          ball_y + BALL_HEIGHT > paddle_y and
          ball_y < paddle_y + PADDLE_HEIGHT):
        ball_speed_y = abs(ball_speed_y) * -1

      # paddle bewegen
      if keys[pygame.K_d]:
        paddle_x = paddle_x + 10
      if keys[pygame.K_a]:
        paddle_x = paddle_x -10

      # paddle binnen scherm houden
      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
      if paddle_x < 0:
        paddle_x = 0

      # 
      # handle collisions
      #

      # ball raakt brick
      for i in range(len(bricks_x)):
        if (ball_x + BALL_WIDTH  > bricks_x[i] and # check of ball brick raakt.
            ball_x < bricks_x[i] + BRICK_WIDTH and
            ball_y + BALL_HEIGHT > bricks_y[i] and
            ball_y < bricks_y[i] + BRICK_HEIGHT):
          print('raak blok')
          if (ball_speed_y > 0 and ball_y < bricks_y[i]): # ball komt van boven, want bovenkant ball is nog boven bovenkant brick en bal omlaag
            print('boven')
            ball_speed_y = abs(ball_speed_y) * -1
          elif (ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT): # ball komt van onder, want onderkant bal is onder onderkant brick en bal omhoog
            print('onder')
            ball_speed_y = abs(ball_speed_y)
          elif (ball_speed_x > 0 and ball_x < bricks_x[i]): # ball komt van links, want linkerkant bal is links van linkerkant brick en bal gaat naar rechts
            print('links')
            ball_speed_x = abs(ball_speed_x) * -1
          elif (ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH): # ball komt van rechts, wwant rechterkant bal is rechts van rechterkant brick
            print('rechts')
            ball_speed_x = abs(ball_speed_x)
          # geraakte brick weghalen
          bricks_x.pop(i)
          bricks_y.pop(i)
          score += 1
          nr_blocks -= 1
          break

      # botsing onderkant scherm
      if ball_y + BALL_HEIGHT >= SCREEN_HEIGHT:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status = 'lost'

      # winnen
      if len(bricks_x) == 0:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status = 'won'

      # teken ball
      screen.blit(ball_img, (ball_x, ball_y))
      screen.blit(paddle_img, (paddle_x, paddle_y))
      for i in range(len(bricks_x)):
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))  

    if game_status == 'won':
      game_status_message = 'Je hebt gewonnen!'

    if game_status == 'lost':
      game_status_msg = 'Je hebt verloren'  

    # teken bericht
    game_status_img = font.render(game_status_msg, True, 'green')
    game_status_img.get_width()
    screen.blit(game_status_img, ((SCREEN_WIDTH / 2 - game_status_img.get_width()/2), 100)) 

    # teken score
    score_msg = f'Score: {score}  Blokken over: {nr_blocks}'
    score_img = font.render(score_msg, True, 'white')
    screen.blit(score_img, (10, 10))

    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
