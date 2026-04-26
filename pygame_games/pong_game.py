"""
乒乓球游戏 (Pong) - 单人模式
玩家与AI对战，使用W/S键或上下方向键控制挡板
"""
import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (50, 255, 50)
RED = (255, 50, 50)

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
WIN_SCORE = 7

class Paddle:
    def __init__(self, x, is_ai=False):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = x
        self.y = SCREEN_HEIGHT // 2 - self.height // 2
        self.speed = 8
        self.is_ai = is_ai
        self.ai_speed = 5  # AI速度
        self.ai_reaction_delay = 0  # AI反应延迟

    def update(self, ball=None):
        if self.is_ai and ball:
            # AI逻辑：跟踪球的y坐标
            center_y = self.y + self.height // 2
            
            # 只有当球向AI方向移动时才反应
            if ball.speed_x > 0:
                # 添加一些随机性，使AI不是完美的
                if random.random() > 0.05:  # 95%的概率正确反应
                    if center_y < ball.y - 10:
                        self.y += self.ai_speed
                    elif center_y > ball.y + 10:
                        self.y -= self.ai_speed
            
            # 限制在屏幕范围内
            self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        else:
            # 玩家控制由外部处理
            pass

    def move_up(self):
        if not self.is_ai:
            self.y = max(0, self.y - self.speed)

    def move_down(self):
        if not self.is_ai:
            self.y = min(SCREEN_HEIGHT - self.height, self.y + self.speed)

    def render(self, surface):
        color = RED if self.is_ai else GREEN
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self):
        self.size = BALL_SIZE
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        # 随机发球方向
        direction = random.choice([-1, 1])
        self.speed_x = 5 * direction
        self.speed_y = random.uniform(-5, 5)
        # 确保球不会水平移动
        if abs(self.speed_y) < 2:
            self.speed_y = 2 if self.speed_y >= 0 else -2

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # 上下墙壁碰撞
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - self.size:
            self.speed_y *= -1
            # 确保球不会卡在墙上
            if self.y <= 0:
                self.y = 0
            else:
                self.y = SCREEN_HEIGHT - self.size

    def render(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.size, self.size))
        # 画个边框让球更明显
        pygame.draw.rect(surface, GRAY, (self.x, self.y, self.size, self.size), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('乒乓球游戏 - 单人对战AI')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 48)
    small_font = pygame.font.SysFont('Arial', 24)

    # 创建游戏对象
    player_paddle = Paddle(20, is_ai=False)
    ai_paddle = Paddle(SCREEN_WIDTH - 20 - PADDLE_WIDTH, is_ai=True)
    ball = Ball()

    player_score = 0
    ai_score = 0
    running = True
    game_over = False
    difficulty = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    # 重新开始
                    ball.reset()
                    player_score = 0
                    ai_score = 0
                    difficulty = 1
                    ai_paddle.ai_speed = 5
                    game_over = False

        if not game_over:
            # 玩家控制
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_paddle.move_up()
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_paddle.move_down()

            # AI更新
            ai_paddle.update(ball)

            # 球更新
            ball.update()

            # 球与挡板碰撞
            if ball.get_rect().colliderect(player_paddle.get_rect()):
                # 计算碰撞位置来调整反弹角度
                offset = (ball.y + ball.size/2) - (player_paddle.y + player_paddle.height/2)
                offset = offset / (player_paddle.height/2)  # 归一化到-1到1
                ball.speed_x = abs(ball.speed_x) * 1.05  # 稍微加速
                ball.speed_y = offset * 8
                ball.x = player_paddle.x + player_paddle.width

            elif ball.get_rect().colliderect(ai_paddle.get_rect()):
                offset = (ball.y + ball.size/2) - (ai_paddle.y + ai_paddle.height/2)
                offset = offset / (ai_paddle.height/2)
                ball.speed_x = -abs(ball.speed_x) * 1.05
                ball.speed_y = offset * 8
                ball.x = ai_paddle.x - ball.size

            # 限制球的最大速度
            max_speed = 15
            ball.speed_x = max(-max_speed, min(max_speed, ball.speed_x))
            ball.speed_y = max(-max_speed, min(max_speed, ball.speed_y))

            # 得分检测
            if ball.x < 0:
                ai_score += 1
                difficulty += 0.5
                ai_paddle.ai_speed = min(12, 5 + difficulty)
                ball.reset()
            elif ball.x > SCREEN_WIDTH:
                player_score += 1
                ball.reset()

            # 检查游戏结束
            if player_score >= WIN_SCORE or ai_score >= WIN_SCORE:
                game_over = True

        # 渲染
        screen.fill(BLACK)

        # 画中线
        for i in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 2, i, 4, 10))

        player_paddle.render(screen)
        ai_paddle.render(screen)
        ball.render(screen)

        # 显示分数
        player_text = font.render(str(player_score), True, GREEN)
        ai_text = font.render(str(ai_score), True, RED)
        screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
        screen.blit(ai_text, (3 * SCREEN_WIDTH // 4, 20))

        # 难度显示
        diff_text = small_font.render(f'难度: {difficulty:.1f}', True, GRAY)
        screen.blit(diff_text, (SCREEN_WIDTH // 2 - 50, 20))

        # 游戏结束提示
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            if player_score >= WIN_SCORE:
                result_text = font.render('你赢了!', True, GREEN)
            else:
                result_text = font.render('AI获胜!', True, RED)
            screen.blit(result_text, 
                       (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            
            final_score_text = small_font.render(f'最终比分: {player_score} - {ai_score}', True, WHITE)
            screen.blit(final_score_text, 
                       (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            
            restart_text = small_font.render('按空格键重新开始', True, GRAY)
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

        # 操作提示
        hint_text = small_font.render('W/S 或 ↑/↓ 控制挡板', True, GRAY)
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 30))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
