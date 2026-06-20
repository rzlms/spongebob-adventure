import pygame
import random
import sys
import math

# تهيئة Pygame
pygame.init()
pygame.mixer.init()

# إعدادات الشاشة
WIDTH = 800
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧽 SpongeBob Adventure")

# الألوان
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (255, 240, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BRIGHT_RED = (255, 50, 50)
DARK_RED = (180, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 100, 255)
PURPLE = (180, 50, 255)
PINK = (255, 105, 180)
BRIGHT_PINK = (255, 150, 200)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (80, 80, 80)
WATER_BLUE = (30, 144, 255)
DEEP_WATER = (10, 50, 150)
BROWN = (139, 69, 19)

# المتغيرات العامة
clock = pygame.time.Clock()
FPS = 60

# ============================================
# الأصوات
# ============================================
def create_sound(freq, dur, vol=0.2):
    try:
        import array
        sample_rate = 22050
        frames = int(dur * sample_rate)
        arr = []
        for i in range(frames):
            t = i / sample_rate
            val = int(vol * 32767 * math.sin(2 * math.pi * freq * t))
            arr.append([val, val])
        flat = []
        for v in arr:
            flat.append(v[0])
            flat.append(v[1])
        return pygame.mixer.Sound(buffer=array.array('h', flat).tobytes())
    except:
        return None

eat_sound = create_sound(800, 0.06, 0.3)
death_sound = create_sound(150, 0.3, 0.3)
win_sound = create_sound(600, 0.08, 0.2)
level_sound = create_sound(700, 0.05, 0.2)
explode_sound = create_sound(100, 0.5, 0.5)
laugh_sound = create_sound(400, 0.2, 0.2)

# ============================================
# بيئات المراحل
# ============================================
LEVEL_ENVIRONMENTS = [
    {"name": "Bikini Bottom", "water": WATER_BLUE},
    {"name": "Jellyfish Fields", "water": (50, 200, 150)},
    {"name": "Deep Sea", "water": DEEP_WATER},
    {"name": "Coral Reef", "water": (100, 200, 255)},
    {"name": "Goo Lagoon", "water": (100, 200, 200)},
    {"name": "Rock Bottom", "water": (60, 80, 120)},
    {"name": "Krusty Krab", "water": (200, 180, 100)},
    {"name": "Glove World", "water": (255, 150, 200)},
    {"name": "Mermaid Kingdom", "water": (150, 100, 200)},
    {"name": "The Surface", "water": (135, 206, 235)},
]

# ============================================
# رسم سبونج بوب
# ============================================
def draw_spongebob(surface, x, y, direction, frame, size_mult=1.0, rage=False):
    base = 28
    s = int(base * size_mult)
    
    # ظل
    pygame.draw.ellipse(surface, (0, 0, 0, 50), (x-s-5, y+int(s*0.8), s*2+10, 8))
    
    body_size = int(s * 1.2)
    # الجسم
    pygame.draw.rect(surface, BRIGHT_YELLOW, (x-body_size, y-body_size, body_size*2, body_size*2))
    pygame.draw.rect(surface, (200, 180, 0), (x-body_size, y-body_size, body_size*2, body_size*2), 2)
    
    # ثقوب
    for i in range(12):
        angle = i * 0.8 + frame * 0.01
        dist = 0.3 + i * 0.05
        hx = x + dist * body_size * math.cos(angle)
        hy = y + dist * body_size * math.sin(angle)
        hr = int(2 + (i % 3) * size_mult)
        if abs(hx - x) < body_size - 5 and abs(hy - y) < body_size - 5:
            pygame.draw.circle(surface, (180, 150, 50), (int(hx), int(hy)), hr)
    
    # عيون
    eye_size = int(9 * size_mult)
    eye_off = int(22 * size_mult)
    eye_y = y - body_size + int(10 * size_mult)
    
    if rage:
        eye_color = (255, 200, 200)
        pupil_color = RED
    else:
        eye_color = WHITE
        pupil_color = BLUE
    
    pygame.draw.rect(surface, eye_color, (x-eye_off, eye_y, eye_size+8, eye_size+10))
    pygame.draw.rect(surface, eye_color, (x+eye_off-18, eye_y, eye_size+8, eye_size+10))
    pygame.draw.rect(surface, BLACK, (x-eye_off, eye_y, eye_size+8, eye_size+10), 2)
    pygame.draw.rect(surface, BLACK, (x+eye_off-18, eye_y, eye_size+8, eye_size+10), 2)
    
    if direction == 1:
        pygame.draw.circle(surface, pupil_color, (x-eye_off+4, eye_y+5), eye_size)
        pygame.draw.circle(surface, pupil_color, (x+eye_off-12, eye_y+5), eye_size)
        pygame.draw.circle(surface, BLACK, (x-eye_off+6, eye_y+5), eye_size//2)
        pygame.draw.circle(surface, BLACK, (x+eye_off-10, eye_y+5), eye_size//2)
    else:
        pygame.draw.circle(surface, pupil_color, (x-eye_off+12, eye_y+5), eye_size)
        pygame.draw.circle(surface, pupil_color, (x+eye_off-4, eye_y+5), eye_size)
        pygame.draw.circle(surface, BLACK, (x-eye_off+14, eye_y+5), eye_size//2)
        pygame.draw.circle(surface, BLACK, (x+eye_off-2, eye_y+5), eye_size//2)
    
    # فم
    mouth_s = int(15 * size_mult)
    mouth_y = eye_y + eye_size + int(5 * size_mult)
    if rage:
        pygame.draw.arc(surface, RED, (x-mouth_s, mouth_y, mouth_s*2, int(15*size_mult)), math.pi+0.2, 2*math.pi-0.2, 3)
    else:
        pygame.draw.arc(surface, RED, (x-mouth_s, mouth_y, mouth_s*2, int(15*size_mult)), 0.1, math.pi-0.1, 3)
        pygame.draw.rect(surface, WHITE, (x-mouth_s//2, mouth_y, int(8*size_mult), int(8*size_mult)))
        pygame.draw.rect(surface, WHITE, (x+mouth_s//2-6, mouth_y, int(8*size_mult), int(8*size_mult)))
    
    # أذرع
    arm_angle = math.sin(frame * 0.08) * 15
    arm_len = int(25 * size_mult)
    pygame.draw.line(surface, BRIGHT_YELLOW, (x-body_size, y+int(body_size*0.3)), 
                     (x-body_size-arm_len+int(arm_angle*0.5), y+int(body_size*0.7)+int(arm_angle*0.5)), int(6*size_mult))
    pygame.draw.line(surface, BRIGHT_YELLOW, (x+body_size, y+int(body_size*0.3)), 
                     (x+body_size+arm_len-int(arm_angle*0.5), y+int(body_size*0.7)+int(arm_angle*0.5)), int(6*size_mult))
    
    # رجلين
    leg_offset = math.sin(frame * 0.08) * 4
    leg_len = int(20 * size_mult)
    leg_y = y + body_size - int(5 * size_mult)
    pygame.draw.line(surface, BRIGHT_YELLOW, (x-int(body_size*0.3), leg_y), 
                     (x-int(body_size*0.3)-int(leg_offset*0.3), leg_y+leg_len), int(8*size_mult))
    pygame.draw.line(surface, BRIGHT_YELLOW, (x+int(body_size*0.3), leg_y), 
                     (x+int(body_size*0.3)+int(leg_offset*0.3), leg_y+leg_len), int(8*size_mult))
    
    # حذاء
    shoe_s = int(12 * size_mult)
    pygame.draw.ellipse(surface, BROWN, (x-int(body_size*0.3)-int(leg_offset*0.3)-shoe_s, leg_y+leg_len-int(4*size_mult), shoe_s*2, int(8*size_mult)))
    pygame.draw.ellipse(surface, BROWN, (x+int(body_size*0.3)+int(leg_offset*0.3)-shoe_s, leg_y+leg_len-int(4*size_mult), shoe_s*2, int(8*size_mult)))
    
    if rage:
        glow = abs(math.sin(frame * 0.2)) * 20
        pygame.draw.circle(surface, (255, 100, 0, 30), (x, y), int(40*size_mult) + glow, 3)

def draw_patrick(surface, x, y, frame):
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        if i % 2 == 0:
            r = 30
        else:
            r = 18 + math.sin(frame * 0.03 + i) * 3
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, BRIGHT_PINK, points)
    pygame.draw.polygon(surface, (200, 50, 150), points, 2)
    pygame.draw.circle(surface, WHITE, (x-12, y-6), 12)
    pygame.draw.circle(surface, WHITE, (x+12, y-6), 12)
    pygame.draw.circle(surface, BLACK, (x-8, y-6), 3)
    pygame.draw.circle(surface, BLACK, (x+16, y-6), 3)

def draw_mr_krabs(surface, x, y, frame):
    pygame.draw.ellipse(surface, BRIGHT_RED, (x-25, y-15, 50, 35))
    pygame.draw.circle(surface, BRIGHT_RED, (x, y-15), 20)
    pygame.draw.line(surface, BRIGHT_RED, (x-10, y-25), (x-15, y-45), 4)
    pygame.draw.line(surface, BRIGHT_RED, (x+10, y-25), (x+15, y-45), 4)
    pygame.draw.circle(surface, WHITE, (x-15, y-45), 8)
    pygame.draw.circle(surface, WHITE, (x+15, y-45), 8)
    pygame.draw.circle(surface, BLACK, (x-13, y-45), 4)
    pygame.draw.circle(surface, BLACK, (x+17, y-45), 4)

def draw_octopus(surface, x, y, frame):
    s = 30
    pygame.draw.ellipse(surface, GRAY, (x-s, y-int(s*0.5), s*2, s))
    pygame.draw.circle(surface, GRAY, (x, y-int(s*0.3)), s)
    pygame.draw.circle(surface, WHITE, (x-10, y-int(s*0.4)), 8)
    pygame.draw.circle(surface, WHITE, (x+10, y-int(s*0.4)), 8)
    pygame.draw.circle(surface, BLACK, (x-8, y-int(s*0.4)), 4)
    pygame.draw.circle(surface, BLACK, (x+12, y-int(s*0.4)), 4)
    for i in range(4):
        angle = i * math.pi / 2 + math.sin(frame * 0.04 + i) * 0.2
        leg_len = int(25)
        leg_x = x + leg_len * math.cos(angle) * 0.8
        leg_y = y + int(s*0.3) + leg_len * 0.5 * math.sin(angle + frame * 0.03)
        pygame.draw.line(surface, GRAY, (x + int(s*0.4) * math.cos(angle), y + int(s*0.2)), (leg_x, leg_y), 5)

def draw_jellyfish(surface, x, y, color, frame):
    pygame.draw.ellipse(surface, color, (x-18, y-10, 36, 20))
    for i in range(6):
        angle = frame * 0.05 + i * 0.8
        xp = x - 12 + i * 5
        yp = y + 8 + math.sin(angle) * 10
        pygame.draw.line(surface, color, (xp, y+8), (xp, yp), 2)
    pygame.draw.circle(surface, WHITE, (x-6, y-6), 5)
    pygame.draw.circle(surface, WHITE, (x+6, y-6), 5)
    pygame.draw.circle(surface, BLACK, (x-4, y-6), 2)
    pygame.draw.circle(surface, BLACK, (x+8, y-6), 2)

def draw_krabby_patty(surface, x, y, frame):
    pygame.draw.ellipse(surface, (210, 180, 140), (x-15, y-10, 30, 12))
    pygame.draw.ellipse(surface, (210, 180, 140), (x-15, y+2, 30, 12))
    pygame.draw.ellipse(surface, (139, 69, 19), (x-12, y-4, 24, 8))
    pygame.draw.ellipse(surface, (255, 215, 0), (x-10, y-6, 20, 4))
    pygame.draw.ellipse(surface, (255, 215, 0), (x-10, y+2, 20, 4))

# ============================================
# جزيئات الانفجار
# ============================================
class ExplosionParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-10, 10)
        self.vy = random.uniform(-10, 10)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.size = random.randint(5, 15)
        self.color = random.choice([BRIGHT_YELLOW, ORANGE, RED, GOLD, WHITE])
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1
        
    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        color = (*self.color, alpha)
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (self.size, self.size), self.size)
        surface.blit(s, (int(self.x-self.size), int(self.y-self.size)))

class SpongePiece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-8, 8)
        self.vy = random.uniform(-10, 5)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-5, 5)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.size = random.randint(8, 20)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.rotation += self.rot_speed
        self.life -= 1
        
    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        pygame.draw.rect(s, (BRIGHT_YELLOW[0], BRIGHT_YELLOW[1], BRIGHT_YELLOW[2], alpha), 
                       (self.size//2, self.size//2, self.size, self.size))
        rotated = pygame.transform.rotate(s, self.rotation)
        surface.blit(rotated, (int(self.x-rotated.get_width()//2), int(self.y-rotated.get_height()//2)))

# ============================================
# فقاعات
# ============================================
class Bubble:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = random.randint(5, 15)
        self.speed = random.uniform(0.5, 2)
        self.alpha = random.randint(50, 150)
        
    def update(self):
        self.y -= self.speed
        self.x += math.sin(self.y * 0.01) * 0.5
        if self.y < -20:
            self.y = HEIGHT + 20
            self.x = random.randint(0, WIDTH)
    
    def draw(self, surface):
        bubble = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(bubble, (255, 255, 255, self.alpha), (self.radius, self.radius), self.radius, 2)
        pygame.draw.circle(bubble, (255, 255, 255, int(self.alpha*0.3)), (self.radius-3, self.radius-3), 4)
        surface.blit(bubble, (int(self.x-self.radius), int(self.y-self.radius)))

# ============================================
# اللاعب
# ============================================
class SpongeBob:
    def __init__(self):
        self.x = 400
        self.y = 350
        self.speed = 5
        self.direction = 1
        self.frame = 0
        self.score = 0
        self.lives = 5
        self.level = 1
        self.coins = 0
        self.size = 1.0
        self.max_size = 2.5
        self.rage = False
        self.rage_timer = 0
        self.exploding = False
        self.explode_timer = 0
        self.particles = []
        self.sponge_pieces = []
        
    def update(self):
        self.frame += 1
        if self.rage:
            self.rage_timer -= 1
            if self.rage_timer <= 0:
                self.rage = False
        
        if self.exploding:
            self.explode_timer -= 1
            self.size = self.max_size + math.sin(self.explode_timer * 0.5) * 0.3
            
            if self.explode_timer % 2 == 0:
                self.particles.append(ExplosionParticle(self.x, self.y))
                self.sponge_pieces.append(SpongePiece(self.x, self.y))
            
            if self.explode_timer <= 0:
                self.exploding = False
                self.size = 1.0
                self.particles.clear()
                self.sponge_pieces.clear()
                return True
        return False
    
    def update_particles(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
        for p in self.sponge_pieces[:]:
            p.update()
            if p.life <= 0:
                self.sponge_pieces.remove(p)
    
    def draw_particles(self, surface):
        for p in self.particles:
            p.draw(surface)
        for p in self.sponge_pieces:
            p.draw(surface)
    
    def eat(self):
        self.coins += 1
        self.score += 10
        self.size = min(self.max_size, self.size + 0.07)
        if eat_sound:
            eat_sound.play()
        if self.coins >= 30:
            self.exploding = True
            self.explode_timer = 40
            if explode_sound:
                explode_sound.play()
            if laugh_sound:
                laugh_sound.play()
            return True
        return False
    
    def shrink(self):
        self.size = max(0.5, self.size - 0.3)
        self.lives -= 1
        if death_sound:
            death_sound.play()
    
    def draw(self, surface):
        if not self.exploding:
            draw_spongebob(surface, self.x, self.y, self.direction, self.frame, self.size, self.rage)
        else:
            self.draw_particles(surface)

# ============================================
# نظام اللعبة
# ============================================
def draw_text(text, color, x, y, size=36):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    if x == 'center':
        rect = text_surface.get_rect()
        rect.center = (WIDTH//2, y)
        screen.blit(text_surface, rect)
    else:
        screen.blit(text_surface, (x, y))

def show_start_screen():
    screen.fill(WATER_BLUE)
    draw_spongebob(screen, 200, 350, 1, 0, 1.5)
    draw_text("🧽 SpongeBob Adventure", YELLOW, 'center', 100, 45)
    draw_text("Eat 30 Krabby Patties to EXPLODE!", WHITE, 'center', 170, 25)
    draw_text("Press SPACE to Start", GREEN, 'center', 400, 35)
    draw_text("Press ESC to Quit", GRAY, 'center', 450, 28)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_level_screen(level, env):
    screen.fill(env["water"])
    draw_text(f"Level {level}", YELLOW, 'center', 250, 60)
    draw_text(f"🌊 {env['name']}", WHITE, 'center', 320, 35)
    draw_text("Eat 30 Krabby Patties to EXPLODE!", ORANGE, 'center', 380, 25)
    pygame.display.flip()
    pygame.time.wait(1500)

def show_end_screen(message, color):
    screen.fill(WATER_BLUE)
    draw_text(message, color, 'center', 250, 60)
    draw_text(f"Score: {player.score}", WHITE, 'center', 330, 35)
    draw_text("Press SPACE to Restart", GREEN, 'center', 420, 35)
    draw_text("Press ESC to Quit", GRAY, 'center', 470, 28)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# ============================================
# الأعداء
# ============================================
class Enemy:
    def __init__(self, x, y, speed, draw_func):
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.frame = 0
        self.draw_func = draw_func
        
    def update(self):
        self.frame += 1
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy
        if self.x < 40 or self.x > WIDTH-40:
            self.dx *= -1
        if self.y < 40 or self.y > HEIGHT-40:
            self.dy *= -1
    
    def draw(self, surface):
        self.draw_func(surface, self.x, self.y, self.frame)

# ============================================
# العملات
# ============================================
class KrabbyPatty:
    def __init__(self):
        self.x = random.randint(30, WIDTH-30)
        self.y = random.randint(30, HEIGHT-30)
        self.frame = 0
        
    def update(self):
        self.frame += 1
    
    def draw(self, surface):
        draw_krabby_patty(surface, self.x, self.y, self.frame)

# ============================================
# اللعبة الرئيسية
# ============================================
def game_loop():
    global player
    player = SpongeBob()
    enemies = []
    coins = []
    bubbles = [Bubble() for _ in range(25)]
    
    level = 1
    max_level = len(LEVEL_ENVIRONMENTS)
    running = True
    level_complete = False
    
    def setup_level(lvl):
        enemies.clear()
        coins.clear()
        
        num_enemies = max(2, lvl)
        
        for _ in range(num_enemies):
            etype = random.choice(["jellyfish", "patrick", "krabs", "octopus"])
            x = random.randint(50, WIDTH-50)
            y = random.randint(50, HEIGHT-50)
            speed = random.uniform(1, 2)
            if etype == "jellyfish":
                color = random.choice([PINK, PURPLE, CYAN, ORANGE])
                enemies.append(Enemy(x, y, speed, lambda s, x, y, f: draw_jellyfish(s, x, y, color, f)))
            elif etype == "patrick":
                enemies.append(Enemy(x, y, speed, draw_patrick))
            elif etype == "krabs":
                enemies.append(Enemy(x, y, speed, draw_mr_krabs))
            elif etype == "octopus":
                enemies.append(Enemy(x, y, speed, draw_octopus))
        
        for _ in range(30):
            coins.append(KrabbyPatty())
    
    setup_level(level)
    show_level_screen(level, LEVEL_ENVIRONMENTS[level-1])
    player.coins = 0
    player.size = 1.0
    level_complete = False
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and not player.exploding:
                    player.rage = True
                    player.rage_timer = 60
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= player.speed
            player.direction = -1
        if keys[pygame.K_RIGHT]:
            player.x += player.speed
            player.direction = 1
        if keys[pygame.K_UP]:
            player.y -= player.speed
        if keys[pygame.K_DOWN]:
            player.y += player.speed
        
        size_offset = int(20 * player.size)
        player.x = max(25 + size_offset, min(player.x, WIDTH-25-size_offset))
        player.y = max(25 + size_offset, min(player.y, HEIGHT-25-size_offset))
        
        if player.update():
            level_complete = True
        
        player.update_particles()
        
        for enemy in enemies:
            enemy.update()
        for coin in coins:
            coin.update()
        for bubble in bubbles:
            bubble.update()
        
        # جمع العملات
        for coin in coins[:]:
            dx = player.x - coin.x
            dy = player.y - coin.y
            if dx*dx + dy*dy < 600:
                coins.remove(coin)
                if player.eat():
                    level_complete = True
                if len(coins) < 30:
                    coins.append(KrabbyPatty())
        
        # التصادم مع الأعداء
        for enemy in enemies[:]:
            dx = player.x - enemy.x
            dy = player.y - enemy.y
            if dx*dx + dy*dy < 900:
                if player.rage:
                    player.score += 20
                else:
                    player.shrink()
                    if player.lives <= 0:
                        return show_end_screen("💀 Game Over!", RED)
                    else:
                        player.x = 400
                        player.y = 350
        
        # الرسم
        env = LEVEL_ENVIRONMENTS[level-1]
        screen.fill(env["water"])
        
        # أمواج
        for i in range(10):
            wx = i * 80 + level * 20
            wy = 680 + math.sin(i * 0.5 + level * 0.1) * 20
            pygame.draw.arc(screen, (min(255, env["water"][0]+50), min(255, env["water"][1]+50), min(255, env["water"][2]+50)), (wx, wy, 70, 30), 0, math.pi, 3)
        
        for bubble in bubbles:
            bubble.draw(screen)
        
        for coin in coins:
            coin.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)
        
        # شريط التقدم
        progress = player.coins / 30
        pygame.draw.rect(screen, (50, 50, 50), (WIDTH//2-150, 10, 300, 20))
        pygame.draw.rect(screen, (255, 215, 0), (WIDTH//2-150, 10, int(300 * progress), 20))
        draw_text(f"🍔 {player.coins}/30", WHITE, WIDTH//2-60, 8, 20)
        
        draw_text(f"Score: {player.score}", WHITE, 10, 10, 25)
        draw_text(f"Lives: {player.lives}", WHITE, 10, 40, 25)
        draw_text(f"Level: {level}/{max_level}", WHITE, 10, 70, 25)
        draw_text(f"🌊 {env['name']}", CYAN, WIDTH-150, 10, 20)
        
        if player.rage:
            draw_text("🔥 RAGE!", RED, 'center', 30, 45)
        
        if player.exploding:
            draw_text("💥 EXPLODING!", RED, 'center', 60, 50)
        
        pygame.display.flip()
        
        if level_complete and not player.exploding:
            if level < max_level:
                level += 1
                if level_sound:
                    level_sound.play()
                setup_level(level)
                show_level_screen(level, LEVEL_ENVIRONMENTS[level-1])
                player.coins = 0
                player.size = 1.0
                player.lives = min(player.lives + 1, 5)
                level_complete = False
            else:
                if win_sound:
                    win_sound.play()
                return show_end_screen("🎉 You Win!", GREEN)
    
    pygame.quit()
    return False

# ============================================
# تشغيل اللعبة
# ============================================
if __name__ == "__main__":
    while True:
        show_start_screen()
        if not game_loop():
            break
