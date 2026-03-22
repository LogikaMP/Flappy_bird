# імпортуємо бібліотеку pygame (для створення гри)
import pygame
# імпортуємо наші класи (пташка, труби, кнопка)
from my_class import*


# запускаємо pygame (обов'язково перед використанням)
pygame.init()


# ---------------- НАЛАШТУВАННЯ ГРИ ----------------

# розмір ігрового вікна:
# WIDTH = ширина (600 пікселів)
# HEIGHT = висота (400 пікселів)
WIDTH = 600
HEIGHT = 400
# розмір пташки:
# ширина 50 px, висота 50 px
SIZE = 50

# розмір труби:
# ширина 50 px, висота 300 px
WIDTH_PIPES = 50
HEIGHT_PIPES = 300
# швидкість руху труб:
# 2 пікселя за кадр (чим більше число — тим швидше)
SPEED = 2


# ---------------- ФУНКЦІЇ ----------------

# функція старту гри (натиснули кнопку → почалась гра)
def start_game():
    # беремо глобальну змінну
    # змінюємо стан гри на "game"
    global game_part
    game_part = "game"

# ---------------- СТВОРЕННЯ ВІКНА ----------------

# створюємо вікно гри з розміром 600x400
window = pygame.display.set_mode((WIDTH, HEIGHT))
# встановлюємо назву вікна
pygame.display.set_caption("Flappy bird")


# ---------------- ЗАВАНТАЖЕННЯ КАРТИНОК ----------------

# фон стартового екрану fon_start.png
fon_start = pygame.image.load("fon_start.png")
# фон гри fon_game.png
fon_game = pygame.image.load("fon_game.png")


# ---------------- ЧАС ----------------
# створюємо таймер (щоб гра працювала з FPS)
clock = pygame.time.Clock()

# ---------------- ОБ'ЄКТИ ----------------

# створюємо кнопку "Start" викоритовуємо клас Button
# x=200, y=150 (позиція)
# ширина=200, висота=100
# колір кнопки зелений "#00FF00"
# текст "Start"
# колір тексту білий "#FFFFFF"
# функція при натисканні → start_game
btn_start = Button(x=200, y=150, w=200, h=100,
                   color="#00FF00",text="Start",
                   color_text="#FFFFFF",command=start_game)


# створюємо пташку:- використовує клас(треба його написати )Bird
# x=100, y=200 (позиція)
# ширина=50, висота=50
# швидкість падіння = 5
# список картинок (анімація) ["bird1.png", "bird2.png"]
# None — звук або додатковий параметр (не використовується)
bird = Bird(x = 100, y = 200, s = 50,
            speed = 5, frames = ["bird1.png", "bird2.png"])


# створюємо труби:використовує клас(треба його написати ) Pipes(
# ширина=50, висота=300
# швидкість руху=2
# картинки труб (верхня і нижня)
pipes = Pipes(w = 50, h = 300,
              speed=2, img_1="pipe_down.png", img_2="pipe_up.png")


# ---------------- ЗМІННІ ГРИ ----------------

# змінна для роботи циклу гри (True = гра працює)
run = True
# стан гри:
# "start" — стартовий екран
# "game" — сама гра
game_part = "start"


# ---------------- ГОЛОВНИЙ ЦИКЛ ----------------

while run:

    # перевіряємо всі події (натискання, закриття)
    for event in pygame.event.get():
        # якщо натиснули на хрестик — виходимо з гри
        if event.type == pygame.QUIT:
            run = False


    # ---------------- ЕКРАН СТАРТУ ----------------
    if game_part == "start":

        # малюємо фон старту (позиція 0,0)
        window.blit(fon_start,(0,0))

        # малюємо кнопку
        btn_start.draw(window)
        # перевіряємо натискання кнопки
        btn_start.is_clicked()


    # ---------------- ОСНОВНА ГРА ----------------
    elif game_part == "game":

        # малюємо фон гри
        window.blit(fon_game,(0,0))
        # оновлюємо пташку (рух, гравітація, малювання)
        bird.update(window)
        # оновлюємо труби (рух, генерація, малювання)
        pipes.update(window)

        for i in range(10):
            if bird.rect.colliderect(pipes.pipes_up[i].rect):
                game_part = "restart"
            if bird.rect.colliderect(pipes.pipes_down[i].rect):
                game_part = "restart"
    elif game_part == "restart":
        window.blit(fon_start,(0,0))
    # встановлюємо FPS (60 кадрів в секунду)
    clock.tick(60)
    # оновлюємо екран (показує всі зміни)
    pygame.display.flip()