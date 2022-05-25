import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1150, 670
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Valley Battle")

FINAL_VALLEYgame = (255,255,255)
BLACK = (0, 0, 0)
BLUE = (55, 150, 255)
RED = (255, 0, 0)
BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 5)
FPS = 60
CHARWIDTH = 80
CHARLENGTH = 80
BULLET_VEL = 15
MAX_BULLETS = 5
VEL = 15
SASUKE_HIT = pygame.USEREVENT + 1
NARUTO_HIT = pygame.USEREVENT + 2
HEALTHFONT = pygame.font.SysFont("impact", 40)
WINNERFONT = pygame.font.SysFont("impact", 90)

CHIDORI_SOUND = pygame.mixer.Sound(os.path.join("NarutoChar", "chidori_sound.mp3"))
RASENGAN_SOUND = pygame.mixer.Sound(os.path.join("NarutoChar", "rasengan_sound.mp3"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("NarutoChar", "explosion_sound.mp3"))

SASUKE_CHAR = pygame.image.load(os.path.join("NarutoChar", "kid_sasuke.png"))
SASUKE_CHAR = pygame.transform.scale(SASUKE_CHAR, (CHARWIDTH, CHARLENGTH))
NARUTO_CHAR = pygame.image.load(os.path.join("NarutoChar", "kid_naruto.png"))
NARUTO_CHAR = pygame.transform.scale(NARUTO_CHAR, (CHARWIDTH, CHARLENGTH))

FINAL_VALLEY = pygame.transform.scale(pygame.image.load(os.path.join("NarutoChar", "final_valley.png")), (WIDTH, HEIGHT))
def gameWindow(SASUKE, NARUTO, NARUTO_Bullets, SASUKE_Bullets, SASUKEHP, NARUTOHP):
    WINDOW.blit(FINAL_VALLEY, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    SASUKEHPTxt = HEALTHFONT.render("Health: " + str(SASUKEHP), 1, FINAL_VALLEYgame)
    NARUTOHPTxt = HEALTHFONT.render("Health: " + str(NARUTOHP), 1, FINAL_VALLEYgame)
    
    WINDOW.blit(NARUTOHPTxt, (WIDTH - NARUTOHPTxt.get_width()-15, 15))
    WINDOW.blit(SASUKEHPTxt, (15, HEIGHT - SASUKEHPTxt.get_height()-15))

    WINDOW.blit(SASUKE_CHAR, (SASUKE.x, SASUKE.y + 50))
    WINDOW.blit(NARUTO_CHAR, (NARUTO.x, NARUTO.y - 60))


    for Bullets in SASUKE_Bullets:
        pygame.draw.rect(WINDOW, BLUE, Bullets)
    for Bullets in NARUTO_Bullets:
        pygame.draw.rect(WINDOW, RED, Bullets)

    pygame.display.update()

def narutoMovement(KeysPressed, NARUTO):
    if KeysPressed[pygame.K_a] and NARUTO.x - VEL > 0:
        NARUTO.x -= VEL
    if KeysPressed[pygame.K_d] and NARUTO.x + VEL + NARUTO.width < WIDTH:
        NARUTO.x += VEL
    if KeysPressed[pygame.K_w] and NARUTO.y - 60 - VEL > 0:
        NARUTO.y -= VEL
    if KeysPressed[pygame.K_s] and NARUTO.y - 50 + VEL + NARUTO.height < HEIGHT / 2:
        NARUTO.y += VEL

def sasukeMovement(KeysPressed, SASUKE):
    if KeysPressed[pygame.K_LEFT] and SASUKE.x - VEL > 0:
        SASUKE.x -= VEL
    if KeysPressed[pygame.K_RIGHT] and SASUKE.x + VEL + SASUKE.width < WIDTH:
        SASUKE.x += VEL
    if KeysPressed[pygame.K_UP] and SASUKE.y + 50 - VEL > HEIGHT / 2:
        SASUKE.y -= VEL
    if KeysPressed[pygame.K_DOWN] and SASUKE.y + 50 + VEL + SASUKE.height < HEIGHT:
        SASUKE.y += VEL

def bulletsFunction(SASUKE_Bullets, NARUTO_Bullets, SASUKE, NARUTO):
    for Bullet in SASUKE_Bullets:
        Bullet.y -= BULLET_VEL
        if NARUTO.colliderect(Bullet):
            pygame.event.post(pygame.event.Event(NARUTO_HIT))
            SASUKE_Bullets.remove(Bullet)
        elif Bullet.y <= 0:
            SASUKE_Bullets.remove(Bullet)
    for Bullet in NARUTO_Bullets:
        Bullet.y += BULLET_VEL
        if SASUKE.colliderect(Bullet):
            pygame.event.post(pygame.event.Event(SASUKE_HIT))
            NARUTO_Bullets.remove(Bullet)
        elif Bullet.y >= HEIGHT:
            NARUTO_Bullets.remove(Bullet)

def winner(text):
    DrawText = WINNERFONT.render(text, 1, FINAL_VALLEYgame)
    WINDOW.blit(DrawText, (WIDTH/2 - DrawText.get_width()/2, HEIGHT/2 - DrawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1500)

def main():
    SASUKE = pygame.Rect(700, 300, CHARWIDTH, CHARLENGTH)
    NARUTO = pygame.Rect(100, 300, CHARWIDTH, CHARLENGTH)

    SASUKE_Bullets = []
    NARUTO_Bullets = []
    SASUKEHP = 20
    NARUTOHP = 20

    Clock = pygame.time.Clock()
    
    Run = True
    while Run:
        Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(SASUKE_Bullets) < MAX_BULLETS:
                    Bullet = pygame.Rect(SASUKE.x + SASUKE.width / 2, SASUKE.y + 50, 8, 18)
                    SASUKE_Bullets.append(Bullet)
                    CHIDORI_SOUND.play()
                if event.key == pygame.K_SPACE and len(NARUTO_Bullets) < MAX_BULLETS:
                    Bullet = pygame.Rect(NARUTO.x + NARUTO.width / 2, NARUTO.y, 8, 18)
                    NARUTO_Bullets.append(Bullet)
                    RASENGAN_SOUND.play()
            if event.type == SASUKE_HIT:
                SASUKEHP -= 1
                HIT_SOUND.play()
            if event.type == NARUTO_HIT:
                NARUTOHP -= 1
                HIT_SOUND.play()

        bulletsFunction(SASUKE_Bullets, NARUTO_Bullets, SASUKE, NARUTO)
        KeysPressed = pygame.key.get_pressed()
        narutoMovement(KeysPressed, NARUTO)
        sasukeMovement(KeysPressed, SASUKE)
        gameWindow(SASUKE, NARUTO, NARUTO_Bullets, SASUKE_Bullets, SASUKEHP, NARUTOHP)
        
        winnerMessage = ""
        if SASUKEHP <= 0:
            winnerMessage = "Naruto Wins: New Story!"
        if NARUTOHP <= 0:
            winnerMessage = "Sasuke Wins: That's Canon!"
        if winnerMessage != "":
            winner(winnerMessage)
            break
        
    pygame.quit()

if __name__ == "__main__":
    main()