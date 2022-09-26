import pygame
from pygame.locals import *
from sys import exit
from random import randint

'''COLORS SETUP'''

WHITE             = Color(255, 255, 255)
TRANSPARENT_WHITE = Color(255, 255, 255, 10)
BLACK             = Color(0, 0, 0)
GREY              = Color(19, 19, 19)
PINK              = Color(255 ,80, 140)
TRANSPARENT_PINK  = Color(255 ,80 ,140, 10)
BLUE              = Color(0, 96, 255)
TRANSPARENT_BLUE  = Color(0, 96, 255, 10)

'''SCREEN SETUP'''

pygame.init()

display_width  = 1600
display_height = 900

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

'''SOUND FX'''

collision_sound = pygame.mixer.Sound("smw_swimming.wav")
collision_sound.set_volume(0.4)
point_increase_sound = pygame.mixer.Sound("smw_stomp.wav")
point_increase_sound.set_volume(0.4)

'''ENTITY SETUP'''

std_paddle_width  = 25
std_paddle_height = 160
paddle_vel        = 30

paddle_1_xpos = 2*std_paddle_width
paddle_2_xpos = display_width - 3*std_paddle_width
paddle_1_ypos = display_height/2-std_paddle_height/2
paddle_2_ypos = display_height/2-std_paddle_height/2

ball_xpos         = display_width/2
ball_ypos         = display_height/2
std_ball_radius   = 10
ball_vel          = 35
ball_xvel         = ball_vel
ball_yvel         = 0

'''DEFINING THE PLAYERS POINTS'''

player_1_points = 0
player_2_points = 0

points_config = pygame.font.SysFont("LCDMono2", 100, True, False)

'''ENTITY CLASSES'''

class Paddle:
    def __init__(self, initial_x, initial_y, width, height, color):
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.width = width
        self.height = height
        self.color = color
    
    def createPaddle(self):
        pygame.draw.rect(screen, self.color, (self.initial_x, self.initial_y, self.width, self.height))

class Ball:
    def __init__(self, initial_x, initial_y, radius, color):
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.radius = radius
        self.color = color

    def createBall(self):
        pygame.draw.circle(screen, self.color, (self.initial_x, self.initial_y), self.radius)

while True:

    '''SCREEN SETUP'''

    clock.tick(30)
    screen.fill(GREY)

    '''MIDFIELD LINE'''

    pygame.draw.line(screen, TRANSPARENT_WHITE, (display_width/2, 0), (display_width/2, display_height), 3)

    '''MAIN EVENTS LOOP'''

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    '''PADDLES MOVEMENT'''

    if pygame.key.get_pressed()[K_w]:
        paddle_1_ypos -= paddle_vel
        paddle_1_yvel = -20
    if pygame.key.get_pressed()[K_s]:
        paddle_1_ypos += paddle_vel
        paddle_1_yvel = 20
    if pygame.key.get_pressed()[K_i]:
        paddle_2_ypos -= paddle_vel
        paddle_2_yvel = -20
    if pygame.key.get_pressed()[K_k]:
        paddle_2_ypos += paddle_vel
        paddle_2_yvel = 20

    '''INSTANTIATING THE ENTITIES'''

    paddle_1 = Paddle(paddle_1_xpos, paddle_1_ypos, std_paddle_width, std_paddle_height, PINK)
    paddle_2 = Paddle(paddle_2_xpos, paddle_2_ypos, std_paddle_width, std_paddle_height, BLUE)
    ball = Ball(ball_xpos, ball_ypos, std_ball_radius, WHITE)

    paddle_1.createPaddle()
    paddle_2.createPaddle()
    ball.createBall()

    '''BALL COLLISION WITH THE BORDERS'''

    if (ball_ypos <= 0) or (ball_ypos >= display_height):
        ball_yvel*= -1
        collision_sound.play()
    if ball_xpos >= display_width:
        ball_xpos = display_width/2
        ball_ypos = display_height/2
        ball_xvel *= -1
        ball_yvel = 0
        player_1_points += 1
        point_increase_sound.play()
    if ball_xpos <= 0:
        ball_xpos = display_width/2
        ball_ypos = display_height/2
        ball_xvel *= -1
        ball_yvel = 0
        player_2_points += 1
        point_increase_sound.play()

    '''PADDLES COLLISION WITH THE BORDERS'''

    if (paddle_1_ypos + std_paddle_height <= 0) and (paddle_1_yvel < 0):
        paddle_1_ypos = display_height
    if (paddle_1_ypos >= display_height) and (paddle_1_yvel > 0):
        paddle_1_ypos = -std_paddle_height
    if (paddle_2_ypos + std_paddle_height <= 0) and (paddle_2_yvel < 0):
        paddle_2_ypos = display_height
    if (paddle_2_ypos >= display_height) and (paddle_2_yvel > 0):
        paddle_2_ypos = -std_paddle_height


    '''BALL COLLISION WITH THE PADDLES'''

    if (ball_xpos >= paddle_1_xpos) and (ball_xpos <= paddle_1_xpos + std_paddle_width) and (ball_ypos >= paddle_1_ypos) and (ball_ypos <= paddle_1_ypos + std_paddle_height):
        ball_xvel *= -1
        ball_yvel = randint(-ball_vel, ball_vel)
        collision_sound.play()
    if (ball_xpos >= paddle_2_xpos) and (ball_xpos <= paddle_2_xpos + std_paddle_width) and (ball_ypos >= paddle_2_ypos) and (ball_ypos <= paddle_2_ypos + std_paddle_height):
        ball_xvel *= -1
        ball_yvel = randint(-ball_vel, ball_vel)
        collision_sound.play()
    
    '''UPDATING THE PLAYERS POINTS'''

    player_1_points_message = f"{player_1_points}"
    player_2_points_message = f"{player_2_points}"
    format_player_1_points = points_config.render(player_1_points_message, True, TRANSPARENT_PINK)
    format_player_2_points = points_config.render(player_2_points_message, True, TRANSPARENT_BLUE)
    points_1_text_rect = format_player_1_points.get_rect()
    points_2_text_rect = format_player_2_points.get_rect()

    points_1_text_rect.center = (display_width//3, display_height//2)
    points_2_text_rect.center = (2*display_width//3, display_height//2)

    screen.blit(format_player_1_points, points_1_text_rect)
    screen.blit(format_player_2_points, points_2_text_rect)

    '''UPDATING THE BALL POSITION'''

    ball_xpos += ball_xvel
    ball_ypos += ball_yvel

    pygame.display.flip()