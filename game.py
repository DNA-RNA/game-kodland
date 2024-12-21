import random
from pgzero.rect import Rect

# Oyun ekranı boyutları
TITLE = 'Platformer Ninja'
WIDTH = 800
HEIGHT = 600

# Renkler
ground_color = (50, 50, 50)  # Koyu gri renk

# Zemin seviyesi
ground_height = 50
ground_level = HEIGHT - ground_height

# Oyun durumu
state = "menu"
score = 0
collision_counter = 0  # Çarpışma için sayaç
music_on = False  # Arka plan müziği durumu

# Sesler
jump_sound = "jump-voice"  # 'sounds/jump-voice.ogg'
run_sound = "run-voice"    # 'sounds/run-voice.ogg'
background_music = "background-music"  # 'sounds/background-music.ogg'

# Müzik kapatma düğmesi koordinatları
music_toggle_rect = Rect((WIDTH - 150, 10), (140, 30))

def draw():
    if state == "menu":
        draw_menu()
    elif state == "game":
        draw_game()
    elif state == "gameover":
        draw_gameover()

def draw_menu():
    screen.fill((135, 206, 235))  # Açık mavi arka plan
    start_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 75), (200, 50))
    sound_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2), (200, 50))
    exit_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 75), (200, 50))

    screen.draw.filled_rect(start_rect, "white")
    screen.draw.filled_rect(sound_rect, "white")
    screen.draw.filled_rect(exit_rect, "white")
    screen.draw.text("Start Game", center=start_rect.center, color="black")
    screen.draw.text("Toggle Music", center=sound_rect.center, color="black")
    screen.draw.text("Exit", center=exit_rect.center, color="black")

def draw_game():
    screen.blit('sand', (0, 0))  # Arka plan görseli
    screen.draw.filled_rect(Rect((0, ground_level), (WIDTH, ground_height)), ground_color)  # Zemin çizimi
    screen.draw.text(f'Score: {score}', color='white', topleft=(10, 10), fontsize=30)
    screen.draw.filled_rect(music_toggle_rect, "gray")
    screen.draw.text("Music: ON" if music_on else "Music: OFF", center=music_toggle_rect.center, color="white", fontsize=20)
    ninja.draw()
    enemy.draw()

def draw_gameover():
    screen.fill((135, 206, 235))
    screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=50, color="red")
    screen.draw.text("Press R to Restart", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color="white")

class Character:
    def __init__(self, x, y, images, jump_image, die_image):
        self.x = x
        self.y = y
        self.images = images
        self.jump_image = jump_image
        self.die_image = die_image
        self.current_frame = 0
        self.image = images[0]
        self.jumping = False
        self.speed = 0
        self.alive = True

    def animate(self):
        if not self.jumping and self.alive:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

    def update(self):
        if self.jumping:
            self.speed += 1
            self.y += self.speed
            if self.y >= ground_level - 60:
                self.y = ground_level - 60
                self.jumping = False

    def jump(self):
        if not self.jumping and self.alive:
            self.jumping = True
            self.speed = -20
            self.image = self.jump_image
            sounds.jump_voice.play()

    def die(self):
        self.alive = False
        self.image = self.die_image

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def update(self):
        self.x -= 5
        if self.x < -50:
            self.x = WIDTH + random.randint(50, 300)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

ninja_images = ['run_001', 'run_002', 'run_003', 'run_004', 'run_005']
ninja_jump_image = 'jump'
ninja_die_image = 'dead'
ninja = Character(100, ground_level - 60, ninja_images, ninja_jump_image, ninja_die_image)
enemy = Enemy(WIDTH, ground_level - 40, 'meteorbrown_big1')

def update():
    global state, score, collision_counter

    if state == "game":
        ninja.update()
        ninja.animate()
        enemy.update()

        if ninja.alive and Rect((ninja.x, ninja.y), (50, 50)).colliderect(Rect((enemy.x, enemy.y), (50, 50))):
            ninja.die()
            collision_counter = 60
            sounds.background.stop()

        if collision_counter > 0:
            collision_counter -= 1
            if collision_counter == 0:
                state = "gameover"

        if enemy.x < 0 and ninja.alive:
            score += 1

def on_key_down(key):
    global state, music_on
    if state == "menu":
        if key == keys.SPACE:
            state = "game"
            if not music_on:
                sounds.background.play(-1)
                music_on = True
    elif state == "game":
        if key == keys.SPACE:
            ninja.jump()
    elif state == "gameover":
        if key == keys.R:
            restart_game()

def on_mouse_down(pos, button):
    global state, music_on
    start_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 75), (200, 50))
    sound_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2), (200, 50))
    exit_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 75), (200, 50))

    if button == mouse.LEFT:
        if start_rect.collidepoint(pos):
            state = "game"
            if not music_on:
                sounds.background.play(-1)
                music_on = True
        elif sound_rect.collidepoint(pos):
            toggle_music()
        elif exit_rect.collidepoint(pos):
            exit()

    if state == "game" and music_toggle_rect.collidepoint(pos):
        toggle_music()

def toggle_music():
    global music_on
    if music_on:
        sounds.background.stop()
    else:
        sounds.background.play(-1)
    music_on = not music_on

def restart_game():
    global state, score, collision_counter
    state = "game"
    score = 0
    collision_counter = 0
    enemy.x = WIDTH
    ninja.alive = True
    ninja.image = ninja.images[0]
