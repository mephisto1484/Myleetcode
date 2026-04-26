"""
无尽奔跑游戏 (Endless Runner)
操作说明：按空格键跳跃，躲避障碍物
"""
import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
GROUND_HEIGHT = 50

class Player:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = 100
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.vy = 0
        self.jumping = False
        self.color = BLUE

    def jump(self):
        if not self.jumping:
            self.vy = JUMP_STRENGTH
            self.jumping = True

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy

        # 地面碰撞
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.vy = 0
            self.jumping = False

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        # 画眼睛
        pygame.draw.circle(surface, WHITE, (self.x + 25, self.y + 15), 8)
        pygame.draw.circle(surface, BLACK, (self.x + 27, self.y + 15), 4)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    def __init__(self, x, width, height, speed):
        self.x = x
        self.width = width
        self.height = height
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.speed = speed
        self.color = RED

    def update(self):
        self.x -= self.speed

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.x + self.width < 0

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.speed = 5
        self.color = YELLOW
        self.collected = False
        self.bob_offset = 0
        self.bob_direction = 1

    def update(self):
        self.x -= self.speed
        # 上下浮动
        self.bob_offset += 0.1 * self.bob_direction
        if abs(self.bob_offset) > 10:
            self.bob_direction *= -1

    def render(self, surface):
        if not self.collected:
            pygame.draw.circle(surface, self.color, 
                             (int(self.x), int(self.y + self.bob_offset)), self.radius)
            pygame.draw.circle(surface, ORANGE, 
                             (int(self.x), int(self.y + self.bob_offset)), self.radius, 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y + self.bob_offset - self.radius, 
                          self.radius * 2, self.radius * 2)

    def is_off_screen(self):
        return self.x + self.radius < 0

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('无尽奔跑游戏')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)

    player = Player()
    obstacles = []
    coins = []
    
    score = 0
    coin_count = 0
    speed = 5
    obstacle_timer = 0
    coin_timer = 0
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # 重新开始
                        player = Player()
                        obstacles = []
                        coins = []
                        score = 0
                        coin_count = 0
                        speed = 5
                        game_over = False
                    else:
                        player.jump()

        if not game_over:
            # 更新玩家
            player.update()

            # 生成障碍物
            obstacle_timer += 1
            if obstacle_timer >= random.randint(60, 120) and len(obstacles) < 3:
                width = random.randint(30, 60)
                height = random.randint(40, 80)
                obstacles.append(Obstacle(SCREEN_WIDTH + 50, width, height, speed))
                obstacle_timer = 0

            # 生成金币
            coin_timer += 1
            if coin_timer >= random.randint(80, 150):
                x = SCREEN_WIDTH + 50
                y = random.randint(SCREEN_HEIGHT - GROUND_HEIGHT - 200, 
                                  SCREEN_HEIGHT - GROUND_HEIGHT - 50)
                coins.append(Coin(x, y))
                coin_timer = 0

            # 更新障碍物
            for obstacle in obstacles[:]:
                obstacle.speed = speed
                obstacle.update()
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                    score += 1
                if obstacle.get_rect().colliderect(player.get_rect()):
                    game_over = True

            # 更新金币
            for coin in coins[:]:
                coin.speed = speed
                coin.update()
                if coin.is_off_screen():
                    coins.remove(coin)
                if not coin.collected and coin.get_rect().colliderect(player.get_rect()):
                    coin.collected = True
                    coin_count += 1
                    score += 50
                    coins.remove(coin)

            # 增加难度
            speed += 0.001

        # 渲染
        screen.fill(BLACK)

        # 画地面
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, 
                                         SCREEN_WIDTH, GROUND_HEIGHT))
        pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT - GROUND_HEIGHT), 
                        (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 2)

        player.render(screen)

        for obstacle in obstacles:
            obstacle.render(screen)

        for coin in coins:
            coin.render(screen)

        # 显示信息
        score_text = font.render(f'分数: {score}', True, WHITE)
        coin_text = small_font.render(f'金币: {coin_count}', True, YELLOW)
        speed_text = small_font.render(f'速度: {speed:.1f}', True, ORANGE)
        screen.blit(score_text, (10, 10))
        screen.blit(coin_text, (10, 50))
        screen.blit(speed_text, (SCREEN_WIDTH - 150, 10))

        if game_over:
            game_over_text = font.render('游戏结束!', True, RED)
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            restart_text = small_font.render('按空格键重新开始', True, WHITE)
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        # 操作提示
        hint_text = small_font.render('按空格键跳跃', True, (150, 150, 150))
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 30))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
