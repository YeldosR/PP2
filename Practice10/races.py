import pygame
import random
import sys

# Размер окна
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60  # частота кадров

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 215, 0)
GRAY = (100, 100, 100)

# Границы дороги (по X)
ROAD_LEFT = 80
ROAD_RIGHT = 420


# машина игрока
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Создаём поверхность  машины
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)

        # Рисуем корпус машины
        pygame.draw.rect(self.image, RED, (0, 0, 40, 70), border_radius=6)

        # Рисуем "стекло"
        pygame.draw.rect(self.image, WHITE, (5, 5, 30, 20), border_radius=3)

        # Прямоугольник для позиции
        self.rect = self.image.get_rect()

        # Начальная позиция (по центру снизу)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        # Скорость движения
        self.speed = 5

    def update(self):
        # Получаем нажатые клавиши
        keys = pygame.key.get_pressed()

        # Движение влево 
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed

        # Движение вправо
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed


# машина врага
class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        # Создаём картинку машины
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)

        # Случайный цвет врага
        color = random.choice([(0, 100, 200), (0, 180, 0), (180, 0, 180)])

        # Рисуем машину
        pygame.draw.rect(self.image, color, (0, 0, 40, 70), border_radius=6)
        pygame.draw.rect(self.image, WHITE, (5, 45, 30, 20), border_radius=3)

        # Позиция
        self.rect = self.image.get_rect()

        # Случайная позиция по X в пределах дороги
        self.rect.x = random.randint(ROAD_LEFT, ROAD_RIGHT - 40)

        # Появляется сверху (за экраном)
        self.rect.y = -80

        # Скорость движения вниз
        self.speed = speed

    def update(self):
        # Двигаем вниз
        self.rect.y += self.speed

        # Если вышла за экран — удаляем
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# монетка
class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        # Создаём поверхность
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)

        # Рисуем круг (монету)
        pygame.draw.circle(self.image, YELLOW, (12, 12), 12)

        # Обводка
        pygame.draw.circle(self.image, (200, 160, 0), (12, 12), 12, 2)

        # Добавляем символ $
        font = pygame.font.SysFont("Arial", 14, bold=True)
        label = font.render("$", True, (120, 80, 0))
        self.image.blit(label, (6, 4))

        # Позиция
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(ROAD_LEFT, ROAD_RIGHT - 24)
        self.rect.y = -30

        # Скорость движения вниз
        self.speed = speed

    def update(self):
        # Двигаем вниз
        self.rect.y += self.speed

        # Удаляем если вне экрана
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# разметка дороги и полосы
class RoadStripe:
    def __init__(self):
        self.y = 0       # начальное смещение
        self.gap = 60    # расстояние между линиями

    def update(self, speed):
        # Сдвигаем линии вниз, создавая эффект движения
        self.y = (self.y + speed) % self.gap

    def draw(self, surface):
        x = SCREEN_WIDTH // 2 - 4  # центр дороги
        y = self.y - self.gap

        # Рисуем линии по всей высоте
        while y < SCREEN_HEIGHT:
            pygame.draw.rect(surface, WHITE, (x, y, 8, 30))
            y += self.gap


# дорога и фон
def draw_road(surface):
    surface.fill(GRAY)  # фон

    # сама дорога
    pygame.draw.rect(surface, (50, 50, 50),
                     (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_HEIGHT))

    # границы дороги
    pygame.draw.rect(surface, WHITE, (ROAD_LEFT - 5, 0, 5, SCREEN_HEIGHT))
    pygame.draw.rect(surface, WHITE, (ROAD_RIGHT, 0, 5, SCREEN_HEIGHT))


# монеты и счёт
def draw_hud(surface, font, score, coins_collected):
    # счёт
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))

    # монеты
    coin_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
    surface.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))


# функция основного
def main():
    pygame.init()

    # создаём окно
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Racer")

    clock = pygame.time.Clock()

    # шрифты
    font = pygame.font.SysFont("Arial", 22, bold=True)
    big_font = pygame.font.SysFont("Arial", 48, bold=True)

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    # создаём игрока
    player = PlayerCar()
    all_sprites.add(player)

    # разметка дороги
    stripe = RoadStripe()

    # игровые переменные
    score = 0
    coins_collected = 0
    scroll_speed = 4
    enemy_spawn_timer = 0
    coin_spawn_timer = 0
    game_over = False

    #  игра 
    while True:
        clock.tick(FPS)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # перезапуск
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    main()
                    return

        # логика игры
        if not game_over:
            score += 1

            # увеличение скорости со временем
            if score % 500 == 0:
                scroll_speed = min(scroll_speed + 1, 12)

            # спавн врагов
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= max(40, 80 - score // 200):
                enemy = EnemyCar(scroll_speed)
                enemy_group.add(enemy)
                all_sprites.add(enemy)
                enemy_spawn_timer = 0

            # спавн монет
            coin_spawn_timer += 1
            if coin_spawn_timer >= random.randint(90, 180):
                coin = Coin(scroll_speed)
                coin_group.add(coin)
                all_sprites.add(coin)
                coin_spawn_timer = 0

            # обновляем все объекты
            all_sprites.update()
            stripe.update(scroll_speed)

            # столкновение с врагом
            if pygame.sprite.spritecollide(player, enemy_group, False):
                game_over = True

            # сбор монет
            collected = pygame.sprite.spritecollide(player, coin_group, True)
            coins_collected += len(collected)

        # отрисовка
        draw_road(screen)
        stripe.draw(screen)
        all_sprites.draw(screen)
        draw_hud(screen, font, score // 10, coins_collected)

        # экран проигрыша
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            over_text = big_font.render("GAME OVER", True, RED)
            score_text = font.render(
                f"Score: {score // 10} | Coins: {coins_collected}", True, WHITE)
            restart = font.render("Press R to restart", True, GREEN)

            screen.blit(over_text, over_text.get_rect(center=(SCREEN_WIDTH//2, 180)))
            screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH//2, 250)))
            screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH//2, 310)))

        # обновление экрана
        pygame.display.flip()


# точка входа
if __name__ == "__main__":
    main()