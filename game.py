import pygame
import random

# Инициализируем pygame
pygame.init()

# Настраиваем размеры окна
screen_width = 800
screen_height = 600

# Создаем экран
screen = pygame.display.set_mode((screen_width, screen_height))

# Устанавливаем заголовок окна
pygame.display.set_caption("Space Invaders")

def show_menu():
    font = pygame.font.SysFont('Arial', 50)
    play_text = font.render('Play', True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    quit_text = font.render('Quit', True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        screen.fill((0, 0, 0))
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.update()


# Создаем класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5
        self.powerup_time = 0
        self.is_invincible = False
        self.is_bullets = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

        if self.powerup_time > 0:
            self.powerup_time -= 1
            if self.powerup_time == 0:
                self.speed = 5
                self.is_invincible = False
                self.is_bullets = False


    def shoot(self):
        if self.is_bullets:
            bullet2 = Bullet(self.rect.centerx+20, self.rect.top)
            all_sprites.add(bullet2)
            bullets.add(bullet2)
            bullet1 = Bullet(self.rect.centerx-20, self.rect.top)
            all_sprites.add(bullet1)
            bullets.add(bullet1)
        else:
            bullet1 = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet1)
            bullets.add(bullet1)

    def powerup(self, powerup_type):
        # Вызывается, когда игрок сталкивается с бонусом
        # Реализуйте поведение игрока при получении бонуса
        if powerup_type == 'speed':
            self.speed = 10
            self.powerup_time = 300
        elif powerup_type == 'invincible':
            self.is_invincible = True
            self.powerup_time = 300
        elif powerup_type == 'more_bullets':
            self.is_bullets = True
            self.powerup_time=300

    def is_hit(self, enemies):
        if not self.is_invincible:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    return True
        return False

# Создаем класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Создаем класс врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy_ship.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speed = random.randint(1, 3)

class Bonus(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load('bonus.png')
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect.x = random.randint(0, self.screen_width - self.rect.width)
        self.rect.y = 0
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.screen_height:
            self.kill()

# Создаем спрайтовые группы
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bonuses = pygame.sprite.Group()

# Создаем игрока и добавляем его в группу спрайтов
player = Player()
all_sprites.add(player)

# Создаем врагов и добавляем их в группу спрайтов
for i in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Создаем счетчик убитых врагов и счетчик бонусов
score = 0
bonus_counter = 0
types = ['speed', 'invincible', 'more_bullets']

show_menu()

# Запускаем игровой цикл
running = True
while running:
    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновляем спрайты
    all_sprites.update()

    # Обрабатываем столкновения пуль с врагами
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        score += 1  # Увеличиваем счетчик убитых врагов
        bonus_counter += 1  # Увеличиваем счетчик бонусов
        if bonus_counter >= 10:
            bonus = Bonus(screen_width, screen_height)
            all_sprites.add(bonus)
            bonuses.add(bonus)
            bonus_counter = 0  # Обнуляем счетчик бонусов

    # Обрабатываем столкновения игрока с врагами
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        if not player.is_invincible:
            running = False


    # Обрабатываем столкновения пуль игрока с врагами
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        score += 1  # Увеличиваем счетчик убитых врагов

    # Обрабатываем столкновения игрока с бонусами
    hits = pygame.sprite.spritecollide(player, bonuses, True)
    for hit in hits:
        # Добавляем бонусы игроку в зависимости от типа бонуса
        player.powerup(random.choice(types))

    # Отрисовываем спрайты
    screen.fill((0, 0, 0))  # Черный цвет фона
    all_sprites.draw(screen)

    # Рисуем счетчик убитых врагов
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Рисуем счетчик бонусов
    font = pygame.font.Font(None, 36)
    text = font.render(f"Bonuses: {score//10}", True, (255, 255, 255))
    screen.blit(text, (10, 30))

    # Рисуем счетчик бонусов
    font = pygame.font.Font(None, 36)
    text = font.render(f"Bonus Last: {player.powerup_time//6}", True, (255, 255, 255))
    screen.blit(text, (10, 50))



    # Обновляем экран
    pygame.display.flip()

# Закрываем игру
pygame.quit()
