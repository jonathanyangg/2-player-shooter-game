import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jon's Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


BORDER = pygame.Rect(WIDTH//2 - 2.5, 0, 5, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
VICTORY_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Victory.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60

#yellow stats
VEL_YELLOW = 5
BULLET_VEL_YELLOW = 20
MAX_BUL_YELLOW = 5

#red stats
VEL_RED = 5
BULLET_VEL_RED = 20
MAX_BUL_RED = 5


SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#yellow spaceship
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)



#red spaceship
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


SKY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'cloud.png')), (WIDTH, HEIGHT))

def yellow_handle_movement(keys_pressed, yellow):
    yellow.height = 55
    yellow.width = 40
    if keys_pressed[pygame.K_a] and yellow.x - VEL_YELLOW > 0: #Left
            yellow.x -= VEL_YELLOW
    if keys_pressed[pygame.K_d] and yellow.x + VEL_YELLOW + yellow.width < BORDER.x: #Right
            yellow.x += VEL_YELLOW
    if keys_pressed[pygame.K_w] and yellow.y - VEL_YELLOW > 0: #Up
            yellow.y -= VEL_YELLOW
    if keys_pressed[pygame.K_s] and yellow.y + VEL_YELLOW + yellow.height < HEIGHT: #Down
            yellow.y += VEL_YELLOW


def red_handle_movement(keys_pressed, red):
    red.height = 55
    red.width = 40
    if keys_pressed[pygame.K_LEFT] and red.x - VEL_RED > BORDER.x + BORDER.width: #Left
            red.x -= VEL_RED
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL_RED + red.width < WIDTH: #Right
            red.x += VEL_RED
    if keys_pressed[pygame.K_UP] and red.y - VEL_RED > 0: #Up
            red.y -= VEL_RED
    if keys_pressed[pygame.K_DOWN] and red.y + VEL_RED + red.height < HEIGHT: #Down
            red.y += VEL_RED



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SKY, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))




    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    

    pygame.display.update()
    
    
    

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL_YELLOW
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            if red.x < WIDTH - 50:
                for i in range(30):
                    red.x += 1
        
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL_RED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            if yellow.x > 5:
                for i in range(30):
                    yellow.x -= 1
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    if text == "Red Wins!":
        draw_text = WINNER_FONT.render(text, 1, RED)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)
    if text == "Yellow Wins!":
        draw_text = WINNER_FONT.render(text, 1, YELLOW)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)



def main():

    red = pygame.Rect(1050, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              run = False
              pygame.quit()
             
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BUL_YELLOW:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BUL_RED:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        #Winner
        

        
        
        winner_text = ""
        if red_health < 1:
            winner_text = "Yellow Wins!"
            VICTORY_SOUND.play()
            

        if yellow_health < 1:     
            winner_text = "Red Wins!"
            VICTORY_SOUND.play()
            
        
        if winner_text != "":
            WIN.blit(SKY, (0, 0))
            pygame.display.update()

            draw_winner(winner_text)
            break

        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
