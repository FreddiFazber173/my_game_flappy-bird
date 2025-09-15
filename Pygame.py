import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Флаппи Берд')
window_size = (1200, 700)
window_surface = pygame.display.set_mode((window_size))
screen = window_surface  # для удобства в функциях
background = pygame.Surface((window_size))
background.fill(pygame.Color('#FFFFFF'))


cartinka = pygame.image.load("R.jpg")
cartinka = pygame.transform.scale(cartinka, window_size)

pygame.mixer.music.load('muzic_fon.mp3')
pygame.mixer.music.play(-1)
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

death_bg = pygame.image.load("ekrancmerti_.jpg")
death_bg = pygame.transform.scale(death_bg, window_size)

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.Font(None, 40)
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x + w/2, y + h/2))
    screen.blit(text_surf, text_rect)
    return False

def game_over_screen(score, best_score, game_instance):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(death_bg, (0, 0))
        font = pygame.font.Font(None, 70)
        text = font.render("Ты сдох как и твоя мама в канаве хахахаха", True, (255, 255, 255))
        screen.blit(text, (window_size[0]//2 - 500, 150))

        font2 = pygame.font.Font(None, 50)
        score_text = font2.render(f"Твой счёт: {score}", True, (255, 255, 255))
        best_text = font2.render(f"Рекорд: {best_score}", True, (255, 255, 0))
        screen.blit(score_text, (window_size[0]//2 - 130, 250))
        screen.blit(best_text, (window_size[0]//2 - 130, 300))

        if draw_button("играть", 450, 400, 300, 60, (200, 200, 200), (170, 170, 170)):
            waiting = False
            game_instance.reset_game()

        if draw_button("изыде нахуй", 450, 500, 300, 60, (200, 200, 200), (170, 170, 170)):
            pygame.quit()
            sys.exit()

        pygame.display.flip()

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
        window_surface.blit(button_text, button_text.get_rect(center=button_rect.center))
        pygame.draw.rect(window_surface, button3_color, button3_rect)
        window_surface.blit(button3_text, button3_text.get_rect(center=button3_rect.center))
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
            return True
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
        self.screen = pygame.display.set_mode(window_size)
        self.bird = pygame.Rect(60, 30, 45, 30)
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

        self.pipes = [Pipe(400), Pipe(700), Pipe(1000), Pipe(1300)]

        if os.path.exists("best_score.txt"):
            with open("best_score.txt", "r") as f:
                self.best_score = int(f.read())
        else:
            self.best_score = 0

    def reset_game(self):
        self.birdY = 350
        self.bird[1] = 350
        self.gravity = 0
        self.jump = 0
        self.counter = 0
        self.dead = False
        x = 400
        for pipe in self.pipes:
            pipe.x = x
            pipe.offset = random.randint(*pipe.offset_range)
            x += 300

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
            if upRect.colliderect(self.bird) or downRect.colliderect(self.bird) or not (0 < self.bird[1] < 720):
                self.dead = True
                sound2.play()
                self.death_handler()

    def death_handler(self):
        if self.counter > self.best_score:
            self.best_score = self.counter
            with open("best_score.txt", "w") as f:
                f.write(str(self.best_score))


        game_over_screen(self.counter, self.best_score, self)

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
            value = score_font.render("Твой счет: " + str(self.counter), True, "red")
            best_text = score_font.render("Рекорд: " + str(self.best_score), True, "blue")
            self.screen.blit(value, (500, 0))
            self.screen.blit(best_text, (500, 40))

            pygame.display.update()


if __name__ == "__main__":
    main_menu()
