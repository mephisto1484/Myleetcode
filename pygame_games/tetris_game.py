"""
俄罗斯方块游戏
操作说明：
- 左右方向键移动方块
- 上方向键旋转方块
- 下方向键加速下落
"""
import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (255, 50, 50),   # 红
    (50, 255, 50),   # 绿
    (50, 100, 255),  # 蓝
    (255, 255, 50),  # 黄
    (255, 165, 0),   # 橙
    (160, 32, 240),  # 紫
    (0, 255, 255)    # 青
]

# 游戏配置
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 30

# 方块形状定义
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

class Piece:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.color = COLORS[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation = 0

    def rotate(self):
        # 转置矩阵实现旋转
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[self.shape[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]
        return rotated

    def get_blocks(self):
        blocks = []
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + j, self.y + i))
        return blocks

class Tetris:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.fall_timer = 0
        self.fall_speed = 30  # 帧数

    def valid_position(self, piece, x=None, y=None, shape=None):
        if x is None:
            x = piece.x
        if y is None:
            y = piece.y
        if shape is None:
            shape = piece.shape

        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= GRID_WIDTH:
                        return False
                    if new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] is not None:
                        return False
        return True

    def lock_piece(self):
        for x, y in self.current_piece.get_blocks():
            if y >= 0:
                self.grid[y][x] = self.current_piece.color

        # 检查并清除满行
        lines_to_clear = []
        for i in range(GRID_HEIGHT):
            if all(self.grid[i][j] is not None for j in range(GRID_WIDTH)):
                lines_to_clear.append(i)

        if lines_to_clear:
            # 清除满行
            for line in sorted(lines_to_clear, reverse=True):
                del self.grid[line]
                self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
            
            # 计分
            self.lines_cleared += len(lines_to_clear)
            self.score += len(lines_to_clear) * 100
            self.fall_speed = max(5, 30 - self.lines_cleared)

        # 生成新方块
        self.current_piece = self.next_piece
        self.next_piece = Piece()

        # 检查游戏结束
        if not self.valid_position(self.current_piece):
            self.game_over = True

    def move(self, dx, dy):
        if not self.game_over:
            if self.valid_position(self.current_piece, 
                                 self.current_piece.x + dx, 
                                 self.current_piece.y + dy):
                self.current_piece.x += dx
                self.current_piece.y += dy
                return True
        return False

    def rotate_piece(self):
        if not self.game_over:
            rotated = self.current_piece.rotate()
            if self.valid_position(self.current_piece, 
                                 self.current_piece.x, 
                                 self.current_piece.y, 
                                 rotated):
                self.current_piece.shape = rotated

    def drop(self):
        while self.move(0, 1):
            pass
        self.lock_piece()

    def update(self):
        if not self.game_over:
            self.fall_timer += 1
            if self.fall_timer >= self.fall_speed:
                if not self.move(0, 1):
                    self.lock_piece()
                self.fall_timer = 0

    def render(self, surface):
        # 画网格背景
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(surface, (30, 30, 30), 
                               (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.line(surface, (50, 50, 50), 
                               (j * GRID_SIZE, i * GRID_SIZE), 
                               (j * GRID_SIZE, (i + 1) * GRID_SIZE), 1)
                pygame.draw.line(surface, (50, 50, 50), 
                               (j * GRID_SIZE, i * GRID_SIZE), 
                               ((j + 1) * GRID_SIZE, i * GRID_SIZE), 1)

        # 画已固定的方块
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j] is not None:
                    pygame.draw.rect(surface, self.grid[i][j], 
                                   (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        # 画当前方块
        for x, y in self.current_piece.get_blocks():
            if y >= 0:
                pygame.draw.rect(surface, self.current_piece.color, 
                               (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        # 画下一个方块预览
        preview_x = GRID_WIDTH * GRID_SIZE + 20
        preview_y = 50
        font = pygame.font.SysFont('Arial', 20)
        next_text = font.render('下一个:', True, WHITE)
        surface.blit(next_text, (preview_x, preview_y - 30))
        
        for i, row in enumerate(self.next_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.next_piece.color, 
                                   (preview_x + j * GRID_SIZE, 
                                    preview_y + i * GRID_SIZE, 
                                    GRID_SIZE - 1, GRID_SIZE - 1))

def main():
    # 创建更大的窗口以容纳预览区
    preview_width = 150
    total_width = SCREEN_WIDTH + preview_width
    screen = pygame.display.set_mode((total_width, SCREEN_HEIGHT))
    pygame.display.set_caption('俄罗斯方块')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 28)
    small_font = pygame.font.SysFont('Arial', 20)

    game = Tetris()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_SPACE:
                    if game.game_over:
                        game = Tetris()
                    else:
                        game.drop()

        game.update()

        # 渲染
        screen.fill(BLACK)
        game.render(screen)

        # 显示分数
        score_text = font.render(f'分数: {game.score}', True, WHITE)
        lines_text = small_font.render(f'行数: {game.lines_cleared}', True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH + 20, SCREEN_HEIGHT - 150))
        screen.blit(lines_text, (SCREEN_WIDTH + 20, SCREEN_HEIGHT - 110))

        # 游戏结束
        if game.game_over:
            game_over_text = font.render('游戏结束!', True, (255, 50, 50))
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            restart_text = small_font.render('按空格键重新开始', True, WHITE)
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        # 操作提示
        hint1 = small_font.render('← → 移动', True, (150, 150, 150))
        hint2 = small_font.render('↑ 旋转', True, (150, 150, 150))
        hint3 = small_font.render('↓ 加速', True, (150, 150, 150))
        hint4 = small_font.render('空格 直接落下', True, (150, 150, 150))
        screen.blit(hint1, (SCREEN_WIDTH + 20, SCREEN_HEIGHT - 80))
        screen.blit(hint2, (SCREEN_WIDTH + 20, SCREEN_HEIGHT - 60))
        screen.blit(hint3, (SCREEN_WIDTH + 20, SCREEN_HEIGHT - 40))
        screen.blit(hint4, (SCREEN_WIDTH + 20, SCREEN_HEIGHT - 20))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
