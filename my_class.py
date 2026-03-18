import pygame
from random import randint
class Sprite:
    def __init__(self,x=10,y=10,w=50,h=50,speed=0,image=None,color=(200,0,0)):
            self.image = image
            self.color = color
            self.rect = pygame.Rect(x,y,w,h)
            self.speed = speed
            self.load_img()
    def draw(self,window):
         if self.image:
              window.blit(self.image,self.rect)
         else:
              pygame.draw.rect(window,self.color,self.rect)
    def move(self,window):
         key = pygame.key.get_pressed()
         if key[pygame.K_w] and self.rect.y >= self.speed:
              self.rect.y -= self.speed
         if key[pygame.K_s] and self.rect.bottom <= window.get_height() - self.speed:
              self.rect.y += self.speed
         if key[pygame.K_a] and self.rect.x >= self.speed:
              self.rect.x -= self.speed
         if key[pygame.K_d] and self.rect.right <= window.get_wigth() - self.speed:
              self.rect.x += self.speed
    def load_img(self):
         if self.image:
              self.image = pygame.image.load(self.image)
              self.image = pygame.transform.scale(self.image,(self.rect.w, self.rect.h))

class Circle(Sprite):
    def __init__(self, x = 100, y = 100, radius= 50, 
                 speed = 0, color = (0,0,130)):
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.radius = radius
        self.speed = speed
        self.color = color

    def draw(self, surface):
        #pygame.draw.rect(surface, (0,0,0), self.rect, width=5)
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)

class Player(Circle):
      def __init__(self, x=100, y=100, radius=50, speed=0, color=(0, 0, 130), nickname= "player"):
           super().__init__(x, y, radius, speed, color)
           self.move_x = 0
           self.move_y = 0
           self.font = pygame.font.Font(None, 16)
           self.nick = self.font.render(nickname,True,(0,0,0))
      def move(self):
           self.move_x = 0
           self.move_y = 0
           key = pygame.key.get_pressed()
           if key[pygame.K_w]:
                self.move_y = -self.speed
           if key[pygame.K_s]:
                self.move_y = self.speed
           if key[pygame.K_a]:
                self.move_x = -self.speed
           if key[pygame.K_d]:
                self.move_x = self.speed     

      def draw(self, window):
           super().draw(window)
           window.blit(self.nick,(self.rect.x, self.rect.y-8))

      def grow(self, radius):
          self.radius += radius
          self.rect.w = self.radius*2
          self.rect.h = self.radius*2
          self.rect.center = (self.rect.x + self.rect.w//2, self.rect.y + self.rect.h//2)

class Food(Circle):
     def __init__(self):
          x = randint(-5000,500)
          y = randint(-5000,500)
          radius = randint(2,5)
          speed = 0
          color = (randint(0,255),randint(0,255),randint(0,255))
          super().__init__(x, y, radius, speed, color)

     def update(self,player):
          self.rect.x -= player.move_x
          self.rect.y -= player.move_y

     def eat_me(self,player):
         if self.rect.colliderect(player.rect):
              player.grow(self.radius)
              return True
         else:
              return False
              
class Button(Sprite):  # Створюємо клас кнопки, який наслідує властивості класу Sprite
     
     def __init__(self, x, y, w, h, color, text, color_text, command):
          # Конструктор класу. Виконується при створенні об'єкта кнопки

          # Викликаємо конструктор батьківського класу Sprite і передаємо координати, розміри та колір
          super().__init__(x,y,w,h,0,None,color)
          self.color_text = color_text
          # Зберігаємо колір тексту кнопки
          self.command = command
          # Зберігаємо функцію, яка виконається при натисканні кнопки
          self.add_text(text)
          # Викликаємо метод створення тексту на кнопці
          self.was_pressed = False
          # Прапорець, що показує чи була кнопка натиснута раніше


     def add_text(self, text):  
          # Метод створення та розміщення тексту на кнопці

          # h = 0.45, w = 0.55 (коефіцієнти підбору розміру шрифту)
          size_h = self.rect.h // 0.45
          # Розраховуємо розмір шрифту від висоти кнопки
          size_w = self.rect.w // (0.55 * len(text))
          # Розраховуємо розмір шрифту від ширини кнопки та довжини тексту
          font_size = min(size_h, size_w)
          # Обираємо менше значення, щоб текст точно помістився
          font = pygame.font.Font(None, int(font_size))
          # Створюємо шрифт потрібного розміру
          self.text = font.render(text, True, self.color_text)
          # Створюємо зображення тексту
          self.text_x = (self.rect.w - self.text.get_width()) // 2 + self.rect.x
          # Обчислюємо координату X для центрування тексту по горизонталі
          self.text_y = (self.rect.h - self.text.get_height()) // 2 + self.rect.y
          # Обчислюємо координату Y для центрування тексту по вертикалі


     def draw(self, surface):  
          # Метод відмалювання кнопки на екрані
          super().draw(surface)
          # Малюємо саму кнопку через метод батьківського класу
          surface.blit(self.text, (self.text_x, self.text_y))
          # Малюємо текст поверх кнопки
          
     def is_clicked(self):  
          # Метод перевіряє чи натиснута кнопка

          if self.command:  
               # Перевіряємо чи є функція для виконання
               click = pygame.mouse.get_pressed()[0]
               # Перевіряємо чи натиснута ліва кнопка миші
               pos = pygame.mouse.get_pos()
               # Отримуємо поточну позицію курсора
               if  click and self.rect.collidepoint(pos) and not self.was_pressed:
                    # Якщо кнопка миші натиснута, курсор знаходиться на кнопці
                    # і попередній стан не був натисканням
                    self.command()
                    # Виконуємо функцію кнопки
               self.was_pressed = click
               # Запам’ятовуємо стан кнопки миші, щоб не викликати функцію багато разів



# клас пташки, наслідується від Sprite
class Bird():
     # конструктор (створення об'єкта) - замість картинки додаємо аргументи кадри frame - для анімації
     def __init__
          # викликаємо конструктор батьківського класу Sprite
          # None - замість картинки (бо будемо міняти кадри)
          # None - замість - коліру 
          s
          # список картинок для анімації (наприклад ["bird1.png", "bird2.png"])
          self.f
          # таймер для перемикання кадрів
          self.timer_anime = 0
          # індекс поточного кадру (яка картинка зараз)
          self.i_frame = 0
          # одразу запускаємо анімацію
          self.anime()
     

     # функція анімації пташки
     def anime(self):
          # беремо поточну картинку 
          # зі списку self.frame зі списку за індексом  self.i_frame
          self.image = 
          # завантажуємо картинку
          self.load_img()

          # збільшуємо таймер
          self.timer_anime 
          # якщо пройшло 10 кадрів
          if s
               self.       # обнуляємо таймер
               self.       # переходимо до наступного кадру

               # якщо кадри закінчились
               # (self.i_frame більше дорівнює довжині списку кадрів self.frame) — 
               # починаємо спочатку
               if s
                    se

     # оновлення пташки (викликається кожен кадр)
     def update(self, window):
          self.   # намалювати пташку
          self.        # змінити кадр (анімація)
          self.   # рух


     # рух пташки(аналогічний руху в класі Sprite - лише вгору та вниз)
     def move(self, window):
         # отримуємо натиснуті клавіші
         key = pygame.key.get_pressed()
         # якщо натиснута W і пташка не вилітає за верх
         if key[pygame.K_w] and self.rect.y >= self.speed:
              self.rect.y -= self.speed   # рух вгору
         # якщо натиснута S і не виходимо за низ екрану
         if key[pygame.K_s] and self.rect.bottom <= window.get_height() - self.speed:
              self.rect.y += self.speed   # рух вниз



# клас труб
class Pipes:
     # створення труб - висота, ширина, швидкість, картинки для труб
     def 
          # список верхніх труб
          self.pipes_up = []
          # список нижніх труб
          self.pipes_down = []
          # швидкість руху труб
          self.speed = speed
          # висота труби (300 px)
          self.h = h
          # початкова позиція X
          x = 150
          # створюємо 10 пар труб
          for i in range(10):
               # випадкова висота верхньої труби (-300 до 0)
               y = 
               # додаємо верхню трубу - об'єкт класу Sprite
               self.pipes_up.
               # створюємо нижню трубу (з відступом 100 px)
               y = 
               self.pipes_down.
               # зміщуємо наступну пару труб вправо
               x   # відстань між трубами 200 px


     # малювання труб
     def draw(self, window):
          for i in range(10):
               self.     # верхня труба
               self.   # нижня труба


     # рух труб
     def move(self):
          for i in range(10):
               # рух вліво врехніьої та нижньої труби
               self.pipes_up[i].rect.x 
               self.
               # якщо труба повністю вийшла за екран (ліворуч)
               #  первіряємо праву координату ректа верхньої труби 
               if self.
                    # знаходимо координату  самої правої трубу
                    max_x = max(pipe.rect.x for pipe in self.pipes_up)
                    # переносимо поточну верхню  трубу вправо + відступ між трубами 200
                    self.pipes_up
                    # нова випадкова висота для верхньої труби
                    y = 
                    self.
                    # синхронно переносимо нижню трубу - відступ по вретикалі 100
                    self.p
                    self.p


     # оновлення труб
     def update(self, window):
          self.  # намалювати
          self.       # рух


          
