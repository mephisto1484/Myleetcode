"""
打砖块游戏
操作说明：使用左右方向键或A/D键移动挡板，清除所有砖块获胜
"""
import pygame
import sys

# 初始化pygame
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 40
        self.speed = 8
        self.color = BLUE

    def move_left(self):
        self.x = max(0, self.x - self.speed)

    def move_right(self):
        self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self):
        self.radius = 8
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 5
        self.speed_y = -5
        self.color = WHITE

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # 墙壁碰撞
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x *= -1
        if self.y <= self.radius:
            self.speed_y *= -1

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 5
        self.speed_y = -5

class Brick:
    def __init__(self, x, y, color):
        self.width = 75
        self.height = 25
        self.x = x
        self.y = y
        self.color = color
        self.alive = True

    def render(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def create_bricks():
    bricks = []
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    for row in range(6):
        for col in range(10):
            x = col * 80 + 5
            y = row * 30 + 50
            brick = Brick(x, y, colors[row])
            bricks.append(brick)
    return bricks

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('打砖块游戏')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24)

    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    
    score = 0
    lives = 3
    running = True
    game_over = False
    win = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (game_over or win) and event.key == pygame.K_SPACE:
                    # 重新开始
                    ball.reset()
                    bricks = create_bricks()
                    score = 0
                    lives = 3
                    game_over = False
                    win = False

        if not game_over and not win:
            # 键盘控制
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                paddle.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                paddle.move_right()

            # 更新球
            ball.update()

            # 球与挡板碰撞
            if ball.get_rect().colliderect(paddle.get_rect()):
                ball.speed_y *= -1
                # 根据撞击位置调整角度
                offset = (ball.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2)
                ball.speed_x = offset * 5

            # 球与砖块碰撞
            for brick in bricks[:]:  # 使用切片避免迭代时修改列表
                if brick.alive and ball.get_rect().colliderect(brick.get_rect()):
                    brick.alive = False
                    ball.speed_y *= -1
                    score += 10
                    break

            # 球掉落
            if ball.y > SCREEN_HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    ball.reset()

            # 检查是否获胜
            if all(not brick.alive for brick in bricks):
                win = True

        # 渲染
        screen.fill(BLACK)
        
        paddle.render(screen)
        ball.render(screen)
        
        for brick in bricks:
            brick.render(screen)

        # 显示信息
        score_text = font.render(f'分数: {score}', True, WHITE)
        lives_text = font.render(f'生命: {lives}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

        if game_over:
            game_over_text = font.render('游戏结束! 按空格键重新开始', True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

        if win:
            win_text = font.render('恭喜获胜! 按空格键重新开始', True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_text, text_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
