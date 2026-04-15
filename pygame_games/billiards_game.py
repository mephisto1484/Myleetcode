"""
简易台球游戏
操作说明：
- 鼠标移动瞄准方向
- 鼠标左键点击并拖动设置力度
- 释放鼠标击球
- 目标：将所有球打入袋中
"""
import pygame
import math
import sys

# 初始化pygame
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
GRAY = (128, 128, 128)

# 游戏配置
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# 台球桌配置
TABLE_LEFT = 100
TABLE_TOP = 80
TABLE_WIDTH = 800
TABLE_HEIGHT = 500
TABLE_RIGHT = TABLE_LEFT + TABLE_WIDTH
TABLE_BOTTOM = TABLE_TOP + TABLE_HEIGHT

# 球配置
BALL_RADIUS = 12
FRICTION = 0.985  # 摩擦系数
MIN_SPEED = 0.1
POCKET_RADIUS = 25

class Pocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = POCKET_RADIUS
        
    def render(self, surface):
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (40, 40, 40), (self.x, self.y), self.radius, 3)
        
    def contains_point(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.radius

class Ball:
    def __init__(self, x, y, color, number=0):
        self.x = x
        self.y = y
        self.color = color
        self.number = number
        self.radius = BALL_RADIUS
        self.speed_x = 0
        self.speed_y = 0
        self.active = True
        self.in_pocket = False
        
    def update(self):
        if not self.active:
            return
            
        self.x += self.speed_x
        self.speed_x *= FRICTION
        self.y += self.speed_y
        self.speed_y *= FRICTION
        
        # 停止条件
        if abs(self.speed_x) < MIN_SPEED:
            self.speed_x = 0
        if abs(self.speed_y) < MIN_SPEED:
            self.speed_y = 0
            
        # 边界碰撞（桌子边缘）
        if self.x - self.radius <= TABLE_LEFT:
            self.x = TABLE_LEFT + self.radius
            self.speed_x *= -0.8
        elif self.x + self.radius >= TABLE_RIGHT:
            self.x = TABLE_RIGHT - self.radius
            self.speed_x *= -0.8
            
        if self.y - self.radius <= TABLE_TOP:
            self.y = TABLE_TOP + self.radius
            self.speed_y *= -0.8
        elif self.y + self.radius >= TABLE_BOTTOM:
            self.y = TABLE_BOTTOM - self.radius
            self.speed_y *= -0.8
            
    def render(self, surface):
        if not self.active:
            return
            
        # 画球
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        
        # 画数字（白色球除外）
        if self.number > 0:
            font = pygame.font.SysFont('Arial', 14, bold=True)
            text = font.render(str(self.number), True, BLACK if self.color != YELLOW else BLACK)
            text_rect = text.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(text, text_rect)
            
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def is_moving(self):
        return abs(self.speed_x) > MIN_SPEED or abs(self.speed_y) > MIN_SPEED

class CueBall(Ball):
    def __init__(self, x, y):
        super().__init__(x, y, WHITE, 0)
        self.aim_angle = 0
        self.power = 0
        self.aiming = False
        
    def set_aim(self, mouse_x, mouse_y):
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.aim_angle = math.atan2(dy, dx)
        
    def set_power(self, power):
        self.power = min(power, 20)  # 最大力度
        
    def shoot(self):
        if self.aiming and not self.is_moving():
            self.speed_x = math.cos(self.aim_angle) * self.power
            self.speed_y = math.sin(self.aim_angle) * self.power
            self.aiming = False
            self.power = 0
            
    def render_aim_line(self, surface):
        if not self.aiming or self.is_moving():
            return
            
        # 画瞄准线
        line_length = 100 + self.power * 10
        end_x = self.x + math.cos(self.aim_angle) * line_length
        end_y = self.y + math.sin(self.aim_angle) * line_length
        
        # 虚线
        for i in range(0, int(line_length), 10):
            start_x = self.x + math.cos(self.aim_angle) * i
            start_y = self.y + math.sin(self.aim_angle) * i
            end_x = self.x + math.cos(self.aim_angle) * (i + 5)
            end_y = self.y + math.sin(self.aim_angle) * (i + 5)
            pygame.draw.line(surface, WHITE, (start_x, start_y), (end_x, end_y), 2)
            
        # 画力度指示器
        bar_width = 200
        bar_height = 10
        bar_x = self.x - bar_width // 2
        bar_y = self.y + self.radius + 20
        pygame.draw.rect(surface, GRAY, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, GRAY, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # 力度填充
        fill_width = (self.power / 20) * (bar_width - 4)
        if fill_width > 0:
            # 颜色从绿到红
            r = min(255, int(self.power / 20 * 510))
            g = min(255, int((20 - self.power) / 20 * 510))
            color = (r, g, 0)
            pygame.draw.rect(surface, color, (bar_x + 2, bar_y + 2, fill_width, bar_height - 4))

class PoolTable:
    def __init__(self):
        # 创建球袋
        self.pockets = [
            Pocket(TABLE_LEFT, TABLE_TOP),  # 左上
            Pocket(TABLE_RIGHT, TABLE_TOP),  # 右上
            Pocket(TABLE_LEFT, TABLE_BOTTOM),  # 左下
            Pocket(TABLE_RIGHT, TABLE_BOTTOM),  # 右下
            Pocket(TABLE_LEFT, TABLE_TOP + TABLE_HEIGHT // 2),  # 左中
            Pocket(TABLE_RIGHT, TABLE_TOP + TABLE_HEIGHT // 2)  # 右中
        ]
        
        # 创建球
        self.balls = []
        self.cue_ball = CueBall(TABLE_LEFT + 250, TABLE_TOP + TABLE_HEIGHT // 2)
        self.balls.append(self.cue_ball)
        
        # 创建目标球（三角形排列）
        self.create_racked_balls()
        
        self.score = 0
        self.total_balls = len([b for b in self.balls if b != self.cue_ball])
        
    def create_racked_balls(self):
        # 三角形排列的球
        colors = [YELLOW, BLUE, RED, PURPLE, ORANGE, GREEN, BROWN, 
                 YELLOW, BLUE, RED, PURPLE, ORANGE, GREEN, BROWN, YELLOW]
        
        start_x = TABLE_LEFT + 500
        start_y = TABLE_TOP + TABLE_HEIGHT // 2
        
        ball_number = 1
        row = 0
        while ball_number <= 15:
            for i in range(row + 1):
                if ball_number > 15:
                    break
                x = start_x + row * (BALL_RADIUS * 2 + 2)
                y = start_y + (i - row / 2) * (BALL_RADIUS * 2 + 4)
                color = colors[ball_number - 1]
                ball = Ball(x, y, color, ball_number)
                self.balls.append(ball)
                ball_number += 1
            row += 1
            
    def update(self):
        # 更新所有球
        for ball in self.balls:
            ball.update()
            
        # 检测球与球之间的碰撞
        for i, ball1 in enumerate(self.balls):
            if not ball1.active:
                continue
            for j, ball2 in enumerate(self.balls[i+1:], i+1):
                if not ball2.active:
                    continue
                self.check_ball_collision(ball1, ball2)
                
        # 检测球是否入袋
        for ball in self.balls[:]:
            if not ball.active:
                continue
            for pocket in self.pockets:
                if pocket.contains_point(ball.x, ball.y):
                    ball.active = False
                    ball.in_pocket = True
                    if ball == self.cue_ball:
                        # 白球入袋，重置位置
                        ball.active = True
                        ball.x = TABLE_LEFT + 250
                        ball.y = TABLE_TOP + TABLE_HEIGHT // 2
                        ball.speed_x = 0
                        ball.speed_y = 0
                    else:
                        self.score += 1
                        
    def check_ball_collision(self, ball1, ball2):
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < ball1.radius + ball2.radius:
            # 碰撞检测
            # 计算碰撞角度
            angle = math.atan2(dy, dx)
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)
            
            # 旋转速度到碰撞坐标系
            v1x = ball1.speed_x * cos_a + ball1.speed_y * sin_a
            v1y = ball1.speed_y * cos_a - ball1.speed_x * sin_a
            v2x = ball2.speed_x * cos_a + ball2.speed_y * sin_a
            v2y = ball2.speed_y * cos_a - ball2.speed_x * sin_a
            
            # 交换x方向速度（完全弹性碰撞）
            v1x, v2x = v2x, v1x
            
            # 旋转回原坐标系
            ball1.speed_x = v1x * cos_a - v1y * sin_a
            ball1.speed_y = v1y * cos_a + v1x * sin_a
            ball2.speed_x = v2x * cos_a - v2y * sin_a
            ball2.speed_y = v2y * cos_a + v2x * sin_a
            
            # 分离球体，防止重叠
            overlap = (ball1.radius + ball2.radius - distance) / 2
            ball1.x -= overlap * cos_a
            ball1.y -= overlap * sin_a
            ball2.x += overlap * cos_a
            ball2.y += overlap * sin_a
            
    def all_balls_stopped(self):
        return not any(ball.is_moving() for ball in self.balls if ball.active)
            
    def render(self, surface):
        # 画台球桌
        pygame.draw.rect(surface, GREEN, 
                        (TABLE_LEFT - 30, TABLE_TOP - 30, 
                         TABLE_WIDTH + 60, TABLE_HEIGHT + 60))
        pygame.draw.rect(surface, BROWN, 
                        (TABLE_LEFT - 35, TABLE_TOP - 35, 
                         TABLE_WIDTH + 70, TABLE_HEIGHT + 70), 5)
        
        # 画桌面
        pygame.draw.rect(surface, DARK_GREEN, 
                        (TABLE_LEFT, TABLE_TOP, TABLE_WIDTH, TABLE_HEIGHT))
        
        # 画球袋
        for pocket in self.pockets:
            pocket.render(surface)
            
        # 画球
        for ball in self.balls:
            ball.render(surface)
            
        # 画瞄准线
        self.cue_ball.render_aim_line(surface)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('简易台球游戏')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)

    table = PoolTable()
    
    running = True
    dragging = False
    drag_start = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    if table.all_balls_stopped() and table.cue_ball.active:
                        mouse_x, mouse_y = event.pos
                        # 检查是否点击了白球附近
                        dist = math.sqrt((mouse_x - table.cue_ball.x)**2 + 
                                       (mouse_y - table.cue_ball.y)**2)
                        if dist < 50:
                            dragging = True
                            table.cue_ball.aiming = True
                            drag_start = (mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    dragging = False
                    table.cue_ball.shoot()
            elif event.type == pygame.MOUSEMOTION:
                if dragging and drag_start:
                    mouse_x, mouse_y = event.pos
                    # 计算力度（拖动距离）
                    dx = mouse_x - drag_start[0]
                    dy = mouse_y - drag_start[1]
                    power = math.sqrt(dx*dx + dy*dy) / 5
                    table.cue_ball.set_power(power)
                    # 设置瞄准方向（从球指向鼠标）
                    table.cue_ball.set_aim(mouse_x, mouse_y)
                elif not dragging and table.all_balls_stopped():
                    mouse_x, mouse_y = event.pos
                    table.cue_ball.set_aim(mouse_x, mouse_y)

        # 更新
        table.update()

        # 渲染
        screen.fill(BLACK)
        table.render(screen)

        # 显示分数
        score_text = font.render(f'进球: {table.score}/{table.total_balls}', True, WHITE)
        screen.blit(score_text, (20, 20))

        # 游戏状态提示
        if not table.all_balls_stopped():
            status_text = small_font.render('球在运动中...', True, YELLOW)
            screen.blit(status_text, (SCREEN_WIDTH // 2 - 60, 20))
        elif table.cue_ball.aiming:
            status_text = small_font.render('拖动鼠标设置力度，释放击球', True, YELLOW)
            screen.blit(status_text, (SCREEN_WIDTH // 2 - 120, 20))
        else:
            status_text = small_font.render('点击白球附近开始瞄准', True, YELLOW)
            screen.blit(status_text, (SCREEN_WIDTH // 2 - 100, 20))

        # 胜利检测
        if table.score == table.total_balls:
            win_text = font.render('恭喜！你打进了所有球！', True, GREEN)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2))
            restart_text = small_font.render('按 R 键重新开始', True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2 + 50))

        # 操作提示
        hint_text = small_font.render('鼠标瞄准 | 点击拖动设置力度 | R 重新开始', True, GRAY)
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT - 30))

        # 处理重新开始
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            table = PoolTable()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
