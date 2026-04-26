"""
接球游戏
操作说明：使用鼠标左右移动挡板接住下落的球，避免让球掉落
"""
import pygame
import random
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
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# 游戏配置
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
FPS = 60

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 50
        self.color = BLUE

    def update(self, mouse_x):
        self.x = mouse_x - self.width // 2
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class FallingBall:
    def __init__(self):
        self.radius = 12
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = -self.radius
        self.speed = random.uniform(3, 6)
        self.colors = [RED, GREEN, YELLOW, CYAN, MAGENTA, WHITE]
        self.color = random.choice(self.colors)
        self.caught = False

    def update(self):
        self.y += self.speed

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.radius

class ParticleEffect:
    def __init__(self, x, y, color):
        self.particles = []
        for _ in range(15):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 6)
            vx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
            vy = speed * pygame.math.Vector2(1, 0).rotate(angle).y
            self.particles.append({
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'life': 30,
                'color': color
            })

    def update(self):
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # 重力
            particle['life'] -= 1
        self.particles = [p for p in self.particles if p['life'] > 0]

    def render(self, surface):
        for particle in self.particles:
            alpha = int(255 * particle['life'] / 30)
            size = int(4 * particle['life'] / 30)
            if size > 0:
                pygame.draw.circle(surface, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), size)

    def is_finished(self):
        return len(self.particles) == 0

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('接球游戏')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 28)
    small_font = pygame.font.SysFont('Arial', 20)

    paddle = Paddle()
    balls = []
    particle_effects = []
    
    score = 0
    missed = 0
    max_missed = 5
    spawn_timer = 0
    spawn_delay = 60  # 初始生成延迟
    difficulty = 1
    
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    # 重新开始
                    balls = []
                    particle_effects = []
                    score = 0
                    missed = 0
                    spawn_delay = 60
                    difficulty = 1
                    game_over = False

        if not game_over:
            # 鼠标控制
            mouse_x, _ = pygame.mouse.get_pos()
            paddle.update(mouse_x)

            # 生成新球
            spawn_timer += 1
            if spawn_timer >= spawn_delay:
                balls.append(FallingBall())
                spawn_timer = 0
                # 难度递增
                if spawn_delay > 20:
                    spawn_delay -= 0.5

            # 更新球
            for ball in balls[:]:
                ball.update()

                # 检测碰撞
                if not ball.caught and ball.get_rect().colliderect(paddle.get_rect()):
                    ball.caught = True
                    score += 1
                    particle_effects.append(ParticleEffect(ball.x, ball.y, ball.color))
                    balls.remove(ball)
                    
                    # 每10分增加难度
                    if score % 10 == 0:
                        difficulty += 1
                
                # 球掉出屏幕
                elif ball.is_off_screen():
                    if not ball.caught:
                        missed += 1
                    balls.remove(ball)

            # 更新粒子效果
            for effect in particle_effects[:]:
                effect.update()
                if effect.is_finished():
                    particle_effects.remove(effect)

            # 检查游戏结束
            if missed >= max_missed:
                game_over = True

        # 渲染
        screen.fill(BLACK)
        
        # 画背景网格
        for i in range(0, SCREEN_HEIGHT, 30):
            pygame.draw.line(screen, (30, 30, 30), (0, i), (SCREEN_WIDTH, i), 1)
        for i in range(0, SCREEN_WIDTH, 30):
            pygame.draw.line(screen, (30, 30, 30), (i, 0), (i, SCREEN_HEIGHT), 1)
        
        # 渲染游戏对象
        paddle.render(screen)
        
        for ball in balls:
            ball.render(screen)
        
        for effect in particle_effects:
            effect.render(screen)

        # 显示信息
        score_text = font.render(f'分数: {score}', True, GREEN)
        missed_text = font.render(f'失误: {missed}/{max_missed}', True, RED)
        difficulty_text = small_font.render(f'难度: {difficulty}', True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(missed_text, (10, 50))
        screen.blit(difficulty_text, (SCREEN_WIDTH - 100, 10))

        # 提示信息
        hint_text = small_font.render('使用鼠标移动挡板', True, (150, 150, 150))
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 25))

        if game_over:
            # 半透明遮罩
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            game_over_text = font.render('游戏结束!', True, RED)
            final_score_text = font.render(f'最终分数: {score}', True, WHITE)
            restart_text = small_font.render('按空格键重新开始', True, GREEN)
            
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(final_score_text, 
                       (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 10))
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
