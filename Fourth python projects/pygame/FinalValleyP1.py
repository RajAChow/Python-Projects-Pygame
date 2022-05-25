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
BORDER = pygame.Rect(0, HEIGHT/2 - 5, WIDTH, 5)
FPS = 60
CHARWIDTH = 80
CHARLENGTH = 80
NARUTO_ATTACK_VELOCITY = 13
SASUKE_ATTACK_VELOCITY = 17
MAX_ATTACKS = 5 
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


def gameWindow(SASUKE, NARUTO, NARUTO_Attacks, SASUKE_Attacks, SASUKEHP, NARUTOHP):
    WINDOW.blit(FINAL_VALLEY, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    SASUKEHPTxt = HEALTHFONT.render("Health: " + str(SASUKEHP), 1, FINAL_VALLEYgame)
    NARUTOHPTxt = HEALTHFONT.render("Health: " + str(NARUTOHP), 1, FINAL_VALLEYgame)
    
    WINDOW.blit(NARUTOHPTxt, (WIDTH - NARUTOHPTxt.get_width()-15, 15))
    WINDOW.blit(SASUKEHPTxt, (15, HEIGHT - SASUKEHPTxt.get_height()-15))

    WINDOW.blit(SASUKE_CHAR, (SASUKE.x, SASUKE.y))
    WINDOW.blit(NARUTO_CHAR, (NARUTO.x, NARUTO.y))

    for Attacks in SASUKE_Attacks:
        pygame.draw.rect(WINDOW, BLUE, Attacks)
    for Attacks in NARUTO_Attacks:
        pygame.draw.rect(WINDOW, RED, Attacks)
        
    pygame.display.update()

def narutoMovement(KeysPressed, NARUTO):
    if KeysPressed[pygame.K_a] and NARUTO.x - VEL > 0:
        NARUTO.x -= VEL
    if KeysPressed[pygame.K_d] and NARUTO.x + VEL + NARUTO.width < WIDTH:
        NARUTO.x += VEL
    if KeysPressed[pygame.K_w] and NARUTO.y - VEL > 0:
        NARUTO.y -= VEL
    if KeysPressed[pygame.K_s] and NARUTO.y + VEL + NARUTO.height < HEIGHT / 2:
        NARUTO.y += VEL

def sasukeMovement(KeysPressed, SASUKE):
    if KeysPressed[pygame.K_LEFT] and SASUKE.x - VEL > 0:
        SASUKE.x -= VEL
    if KeysPressed[pygame.K_RIGHT] and SASUKE.x + VEL + SASUKE.width < WIDTH:
        SASUKE.x += VEL
    if KeysPressed[pygame.K_UP] and SASUKE.y - VEL > HEIGHT / 2:
        SASUKE.y -= VEL
    if KeysPressed[pygame.K_DOWN] and SASUKE.y + VEL + SASUKE.height < HEIGHT:
        SASUKE.y += VEL

def hitCounter(SASUKE_Attacks, NARUTO_Attacks, SASUKE, NARUTO):
    for Attack in SASUKE_Attacks:
        Attack.y -= SASUKE_ATTACK_VELOCITY
        if NARUTO.colliderect(Attack):
            pygame.event.post(pygame.event.Event(NARUTO_HIT))
            SASUKE_Attacks.remove(Attack)
        elif Attack.y <= 0:
            SASUKE_Attacks.remove(Attack)
    for Attack in NARUTO_Attacks:
        Attack.y += NARUTO_ATTACK_VELOCITY
        if SASUKE.colliderect(Attack):
            pygame.event.post(pygame.event.Event(SASUKE_HIT))
            NARUTO_Attacks.remove(Attack)
        elif Attack.y >= HEIGHT:
            NARUTO_Attacks.remove(Attack)

def winner(text):
    DrawText = WINNERFONT.render(text, 1, FINAL_VALLEYgame)
    WINDOW.blit(DrawText, (WIDTH/2 - DrawText.get_width()/2, HEIGHT/2 - DrawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1500)

def main():
    SASUKE = pygame.Rect(WIDTH / 2 - 50, HEIGHT * 0.75 - 50, CHARWIDTH, CHARLENGTH)
    NARUTO = pygame.Rect(WIDTH / 2 - 50, HEIGHT / 4 - 50, CHARWIDTH, CHARLENGTH)

    SASUKE_Attacks = []
    NARUTO_Attacks = []
    
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
                if event.key == pygame.K_RETURN and len(SASUKE_Attacks) < MAX_ATTACKS:
                    Attack = pygame.Rect(SASUKE.x + SASUKE.width / 2, SASUKE.y, 8, 30)
                    SASUKE_Attacks.append(Attack)
                    CHIDORI_SOUND.play()
                if event.key == pygame.K_SPACE and len(NARUTO_Attacks) < MAX_ATTACKS:
                    Attack = pygame.draw.circle(WINDOW, BLUE, (NARUTO.x + NARUTO.width / 2, NARUTO.y + 63), 12)
                    NARUTO_Attacks.append(Attack)
                    RASENGAN_SOUND.play()
                    
            if event.type == SASUKE_HIT:
                SASUKEHP -= 1
                HIT_SOUND.play()
            if event.type == NARUTO_HIT:
                NARUTOHP -= 1
                HIT_SOUND.play()

        hitCounter(SASUKE_Attacks, NARUTO_Attacks, SASUKE, NARUTO)
        KeysPressed = pygame.key.get_pressed()
        narutoMovement(KeysPressed, NARUTO)
        sasukeMovement(KeysPressed, SASUKE)
        gameWindow(SASUKE, NARUTO, NARUTO_Attacks, SASUKE_Attacks, SASUKEHP, NARUTOHP)
        
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
