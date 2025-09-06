import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Флаппи Берд')
window_size = (1200, 700)
window_surface = pygame.display.set_mode((window_size))
background = pygame.Surface((window_size))
background.fill(pygame.Color('#FFFFFF'))
cartinka = pygame.image.load("R.jpg")
cartinka = pygame.transform.scale(cartinka, window_size)
pygame.mixer.music.load('muzic_fon.mp3')
pygame.mixer.music.play(-1)  # музыка на повтор
sound = pygame.mixer.Sound('sfx_wing.mp3')
sound1 = pygame.mixer.Sound('sfx_point.mp3')
sound2 = pygame.mixer.Sound('sfx_die.mp3')


button_font = pygame.font.SysFont('Verdana', 15)
button_text_color = pygame.Color("black")
button_color = pygame.Color("gray")
button_rect = pygame.Rect(520, 275, 200, 100)
button_text = button_font.render('Играть', True, button_text_color)

button3_font = pygame.font.SysFont('Verdana', 15)
button3_text_color = pygame.Color("black")
button3_color = pygame.Color("gray")
button3_rect = pygame.Rect(520, 385, 200, 100)
button3_text = button3_font.render('Выход', True, button3_text_color)


def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    bird = Game()
                    bird.run()

                if button3_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        window_surface.blit(background, (0, 0))
        window_surface.blit(cartinka, (0, 0))
        pygame.draw.rect(window_surface, button_color, button_rect)
        button_rect_center = button_text.get_rect(center=button_rect.center)
        window_surface.blit(button_text, button_rect_center)

        pygame.draw.rect(window_surface, button3_color, button3_rect)
        button3_rect_center = button3_text.get_rect(center=button3_rect.center)
        window_surface.blit(button3_text, button3_rect_center)

        pygame.display.flip()


class Pipe:
    def __init__(self, x, gap=120, offset_range=(-110, 380)):
        self.x = x
        self.gap = gap
        self.offset_range = offset_range
        self.offset = random.randint(*offset_range)
        self.width = 80
        self.wallUp = pygame.image.load("nis_truba.png").convert_alpha()
        self.wallDown = pygame.image.load("verx_truba.png").convert_alpha()

    def update(self, speed=3):
        self.x -= speed
        if self.x < -self.width:
            sound1.play()
            self.x = 1200
            self.offset = random.randint(*self.offset_range)
            return True  # труба пройдена
        return False

    def draw(self, screen):
        screen.blit(self.wallUp, (self.x, 450 + self.gap - self.offset))
        screen.blit(self.wallDown, (self.x, 0 - self.gap - self.offset))

    def get_rects(self):
        upRect = pygame.Rect(self.x, 450 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10, self.wallUp.get_height())
        downRect = pygame.Rect(self.x, 0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10, self.wallDown.get_height())
        return upRect, downRect


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("fon.png").convert()
        self.birdSprites = [
            pygame.image.load("1.png").convert_alpha(),
            pygame.image.load("2.png").convert_alpha(),
            pygame.image.load("0.png")
        ]
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 0
        self.gravity = 0
        self.dead = False
        self.sprite = 0
        self.counter = 0

        # создаем список труб
        self.pipes = [
            Pipe(400),
            Pipe(700),
            Pipe(1000),
            Pipe(1300)
        ]

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY

        for pipe in self.pipes:
            upRect, downRect = pipe.get_rects()
            if upRect.colliderect(self.bird) or downRect.colliderect(self.bird):
                self.dead = True
                sound2.play()
                main_menu().run()

        if not 0 < self.bird[1] < 720:
            sound2.play()
            main_menu().run()
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.gravity = 5
            # Сбрасываем трубы
            x = 400
            for pipe in self.pipes:
                pipe.x = x
                pipe.offset = random.randint(*pipe.offset_range)
                x += 300

    def run(self):
        clock = pygame.time.Clock()
        score_font = pygame.font.SysFont("comicsansms", 35)
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

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            # Обновляем и рисуем трубы
            for pipe in self.pipes:
                passed = pipe.update()
                if passed:
                    self.counter += 1
                pipe.draw(self.screen)

            # Рисуем птицу
            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0

            self.birdUpdate()

            # Счет
            value = score_font.render("Ваш счет: " + str(self.counter), True, "red")
            self.screen.blit(value, (500, 0))

            pygame.display.update()


if __name__ == "__main__":
    main_menu()
