import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('флаппи берд')
window_size = (1200, 700)
window_surface = pygame.display.set_mode((window_size))
background = pygame.Surface((window_size))
background.fill(pygame.Color('#FFFFFF'))
cartinka = pygame.image.load("R.jpg")
cartinka = pygame.transform.scale(cartinka,window_size)
pygame.mixer.music.load('muzic_fon.mp3')
pygame.mixer.music.play(0)
sound = pygame.mixer.Sound('sfx_wing.mp3')
sound1 = pygame.mixer.Sound('sfx_point.mp3')
sound2 = pygame.mixer.Sound('sfx_die.mp3')


color_list = [
    pygame.Color('#FF0000'),  # красный
    pygame.Color('#00FF00'),  # зеленый
    pygame.Color('#0000FF'),  # синий
    pygame.Color('#FFFF00'),  # желтый
    pygame.Color('#00FFFF'),  # бирюзовый
    pygame.Color('#FF00FF'),  # пурпурный
    pygame.Color('#FFFFFF')   # белый
]

current_color_index = 0

button_font = pygame.font.SysFont('Verdana', 15)
button_text_color = pygame.Color("black")
button_color = pygame.Color("gray")
button_rect = pygame.Rect(520, 275, 200, 100)
button_text = button_font.render('Играть', True, button_text_color)



button3_font = pygame.font.SysFont('Verdana', 15)
button3_text_color = pygame.Color("black")
button3_color = pygame.Color("gray")
button3_rect = pygame.Rect(520, 385, 200, 100)
button3_text = button3_font.render('выход', True, button3_text_color)

def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    bird = game()
                    bird.run()


                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button3_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()


            window_surface.blit(background, (0, 0))
            window_surface.blit(cartinka, (0,0))
            pygame.draw.rect(window_surface, button_color, button_rect)
            button_rect_center = button_text.get_rect(center=button_rect.center)
            window_surface.blit(button_text, button_rect_center)
            

            pygame.draw.rect(window_surface, button3_color, button3_rect)
            button3_rect_center = button3_text.get_rect(center=button3_rect.center)
            window_surface.blit(button3_text, button3_rect_center)
        pygame.display.flip()


class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        self.bird = pygame.Rect(65, 50, 50, 50)

        self.background = pygame.image.load("fon.png").convert()
        self.birdSprites = [pygame.image.load("1.png").convert_alpha(),
                            pygame.image.load("2.png").convert_alpha(),
                            pygame.image.load("0.png")]
        self.wallUp = pygame.image.load("nis_truba.png").convert_alpha()
        self.wallDown = pygame.image.load("verx_truba.png").convert_alpha()
        self.wallUp2 = pygame.image.load("nis_truba.png").convert_alpha()
        self.wallDown2 = pygame.image.load("verx_truba.png").convert_alpha()
        self.wallUp3 = pygame.image.load("nis_truba.png").convert_alpha()
        self.wallDown3 = pygame.image.load("verx_truba.png").convert_alpha()
        self.wallUp4 = pygame.image.load("nis_truba.png").convert_alpha()
        self.wallDown4 = pygame.image.load("verx_truba.png").convert_alpha()
        self.gap = 120
        self.wallx = 400
        self.wallx2 = 700
        self.wallx3 = 1000
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 0
        self.gravity = 0
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.offset2 = random.randint(-110, 220)
        self.offset3 = random.randint(-110, 280)
        self.offset4 = random.randint(-110, 380)


        self.wallx2 = self.wallx + 300
        self.wallx3 = self.wallx2 + 300
        self.wallx4 = self.wallx3 + 300

    def updateWalls(self):
        self.wallx -= 3
        if self.wallx < -80:
            sound1.play()
            self.wallx = 1200
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def updateWalls2(self):
        self.wallx2 -= 3
        if  self.wallx2 < - 80:
            sound1.play()
            self.wallx2 = 1200
            self.counter += 1
            self.offset2 = random.randint(-110, 210)

    def updateWalls3(self):
        self.wallx3 -= 3
        if  self.wallx3 < - 80:
            sound1.play()
            self.wallx3 = 1200
            self.counter += 1
            self.offset3 = random.randint(-110, 280)
    def updatewall4(self):
        self.wallx4 -= 3
        if  self.wallx4 < - 80:
            sound1.play()
            self.wallx4 = 1200
            self.counter += 1
            self.offset4 = random.randint(-110, 330)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
            
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
    

        upRect = pygame.Rect(self.wallx,
                             450 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())

        if upRect.colliderect(self.bird):
            self.dead = True
            sound2.play()
            bird2 = main_menu()
            bird2.run()
        if downRect.colliderect(self.bird):
            self.dead = True
            sound2.play()
            bird2 = main_menu()
            bird2.run()
        if not 0 < self.bird[1] < 720:
            sound2.play()
            bird2 = main_menu()
            bird2.run()
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 500
            self.offset = random.randint(-110, 110)
            self.gravity = 5

        upRect2 = pygame.Rect(self.wallx2,
                             450 + self.gap - self.offset2 + 25,
                             self.wallUp2.get_width() - 25,
                             self.wallUp2.get_height())
        downRect2 = pygame.Rect(self.wallx2,
                               0 - self.gap - self.offset2 - 25,
                               self.wallDown2.get_width() - 25,
                               self.wallDown2.get_height())
        if upRect2.colliderect(self.bird):
            self.dead = True
            sound2.play()
            bird2 = main_menu()
            bird2.run()
        if downRect2.colliderect(self.bird):
            self.dead = True
            sound2.play()
            bird2 = main_menu()
            bird2.run()
        if not 0 < self.bird[1] < 720:
            sound2.play()
            bird2 = main_menu()
            bird2.run()
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 500
            self.offset = random.randint(-100, 100)
            self.gravity = 5

        upRect3 = pygame.Rect(self.wallx3,
                             450 + self.gap - self.offset3 + 25,
                             self.wallUp3.get_width() - 25,
                             self.wallUp3.get_height())
        downRect3 = pygame.Rect(self.wallx3,
                               0 - self.gap - self.offset3 - 25,
                               self.wallDown3.get_width() - 25,
                               self.wallDown3.get_height())
        if upRect3.colliderect(self.bird):
            self.dead = True
            sound2.play()
            bird2 = main_menu()
            bird2.run()
        if downRect3.colliderect(self.bird):
            self.dead = True
            sound2.play()
            bird2 = main_menu()
            bird2.run()
        if not 0 < self.bird[1] < 720:
            sound2.play()
            bird2 = main_menu()
            bird2.run()
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 500
            self.offset = random.randint(-100, 100)
            self.gravity = 5

        upRect4 = pygame.Rect(self.wallx4,
                             450 + self.gap - self.offset4 + 25,
                             self.wallUp4.get_width() - 25,
                             self.wallUp4.get_height())
        downRect4 = pygame.Rect(self.wallx4,
                               0 - self.gap - self.offset4 - 25,
                               self.wallDown4.get_width() - 25,
                               self.wallDown4.get_height())
        if upRect4.colliderect(self.bird):
            self.dead = True
            sound2.play()
            bird2 = main_menu()
            bird2.run()
        if downRect4.colliderect(self.bird):
            self.dead = True
            sound2.play()
            bird2 = main_menu()
            bird2.run()
        if not 0 < self.bird[1] < 720:
            sound2.play()
            bird2 = main_menu()
            bird2.run()
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 500
            self.offset = random.randint(-100, 100)
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 20
                    self.gravity = 5
                    self.jumpSpeed = 10
                    sound.play()
    
            score_font = pygame.font.SysFont("comicsansms", 35)


            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 450 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            
            self.screen.blit(self.wallUp2,
                             (self.wallx2, 450 + self.gap - self.offset2))
            self.screen.blit(self.wallDown2,
                             (self.wallx2, 0 - self.gap - self.offset2))
            
            self.screen.blit(self.wallUp3,
                             (self.wallx3, 450 + self.gap - self.offset3))
            self.screen.blit(self.wallDown3,
                             (self.wallx3, 0 - self.gap - self.offset3))
            
            self.screen.blit(self.wallUp4,
                             (self.wallx4, 450 + self.gap - self.offset4))
            self.screen.blit(self.wallDown4,
                             (self.wallx4, 0 - self.gap - self.offset4))
            
            value = score_font.render("ваш счет: " + str(self.counter), True, "red")
            self.screen.blit(value, (500, 0))
            

            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            self.updateWalls()
            self.updateWalls2()
            self.updateWalls3()
            self.updatewall4()
            self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    main_menu()